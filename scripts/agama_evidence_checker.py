from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from reasoning_validator_output import build_validator_output

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CASES = ROOT / "tests" / "reasoning_cases.yaml"
VALIDATOR = "agama_evidence_checker"
CONTRACT_FAMILY = "agama_evidence"
MODE = "agama-evidence-checker-v0"
OUTPUT_SCHEMA = "agama-evidence-checker-output-v0"
LIMITATIONS = (
    "Prototype reads structured tests/reasoning_cases.yaml fixtures only.",
    "No Agama search execution, CBETA XML collation, provider calls, prompt changes, or citation grading.",
)


class AgamaEvidenceCheckerError(ValueError):
    """Raised when the structured Agama evidence fixture cannot be checked."""


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise AgamaEvidenceCheckerError(f"Reasoning cases not found: {_display_path(path)}")

    try:
        import yaml  # type: ignore[import-not-found]
    except ModuleNotFoundError as exc:
        raise AgamaEvidenceCheckerError("PyYAML is required to read reasoning cases.") from exc

    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001 - keep parser failures visible in CLI output.
        raise AgamaEvidenceCheckerError(f"Failed to parse reasoning cases {_display_path(path)}: {exc}") from exc

    if not isinstance(data, dict):
        raise AgamaEvidenceCheckerError(f"Reasoning cases must be a mapping: {_display_path(path)}")
    return data


def _case_list(data: dict[str, Any]) -> list[dict[str, Any]]:
    cases = data.get("cases")
    if not isinstance(cases, list) or not cases:
        raise AgamaEvidenceCheckerError("Reasoning cases must contain a non-empty cases list.")
    if not all(isinstance(item, dict) for item in cases):
        raise AgamaEvidenceCheckerError("Every reasoning case must be a mapping.")
    return cases


def _select_cases(cases: list[dict[str, Any]], case_id: str | None) -> list[dict[str, Any]]:
    if case_id is None:
        return [case for case in cases if "agama_evidence" in case.get("contracts", [])]

    for case in cases:
        if case.get("id") == case_id:
            return [case]
    raise AgamaEvidenceCheckerError(f"Unknown reasoning case id: {case_id}")


def _string_list(value: Any, field: str, case_id: str) -> list[str]:
    if not isinstance(value, list) or not all(isinstance(item, str) and item for item in value):
        raise AgamaEvidenceCheckerError(f"{case_id} {field} must be a non-empty string list.")
    return list(value)


def _reference_summary(reference_files: list[str]) -> dict[str, Any]:
    agama_files = [item for item in reference_files if item.startswith("context/agama/")]
    return {
        "agama_files": agama_files,
        "has_agama_index": "context/agama/agama-index.md" in reference_files,
        "has_search_helper": "scripts/search_agama.py" in reference_files,
    }


def _evidence_checks(
    *,
    citation_required: bool,
    search_scope: str,
    collation_boundary: bool,
) -> list[dict[str, Any]]:
    return [
        {
            "id": "citation_required",
            "role": "citation_anchor_requirement",
            "status": "required" if citation_required else "not_required",
            "required_fields": ["sutra_name", "cbeta_id", "local_context_anchor"] if citation_required else [],
        },
        {
            "id": "search_scope",
            "role": "search_scope_boundary",
            "status": search_scope,
            "exhaustive": search_scope == "exhaustive_search",
        },
        {
            "id": "collation_boundary",
            "role": "scholarly_collation_boundary",
            "status": "required" if collation_boundary else "not_required",
        },
    ]


def _diagnostics(
    *,
    citation_required: bool,
    search_scope: str,
    collation_boundary: bool,
    boundary_required: bool,
) -> list[dict[str, Any]]:
    diagnostics: list[dict[str, Any]] = []
    if citation_required:
        diagnostics.append(
            {
                "code": "citation_anchor_required",
                "severity": "info",
                "message": "The fixture requires sutra name, CBETA id, and local context/agama anchors.",
            }
        )
    if search_scope == "representative_search":
        diagnostics.append(
            {
                "code": "representative_search_scope",
                "severity": "info",
                "message": "The fixture marks the search as representative, not exhaustive.",
            }
        )
    if collation_boundary:
        diagnostics.append(
            {
                "code": "collation_boundary_required",
                "severity": "info",
                "message": "The fixture requires a CBETA XML or parallel-text collation boundary.",
            }
        )
    if boundary_required:
        diagnostics.append(
            {
                "code": "boundary_statement_required",
                "severity": "info",
                "message": "The fixture requires explicit boundary language.",
            }
        )
    return diagnostics


def _check_case(case: dict[str, Any]) -> dict[str, Any]:
    case_id = case.get("id")
    expected = case.get("expected")
    if not isinstance(case_id, str) or not case_id:
        raise AgamaEvidenceCheckerError("Every selected reasoning case must have a non-empty id.")
    if not isinstance(expected, dict):
        raise AgamaEvidenceCheckerError(f"{case_id} expected must be a mapping.")

    agama_evidence = expected.get("agama_evidence")
    if not isinstance(agama_evidence, dict):
        raise AgamaEvidenceCheckerError(f"{case_id} expected.agama_evidence must be a mapping.")

    citation_required = bool(agama_evidence.get("citation_required", False))
    search_scope = agama_evidence.get("search_scope")
    if not isinstance(search_scope, str) or not search_scope:
        raise AgamaEvidenceCheckerError(f"{case_id} expected.agama_evidence.search_scope must be a string.")
    collation_boundary = bool(agama_evidence.get("collation_boundary", False))
    boundary_required = bool(expected.get("boundary_statement", False))
    reference_files = _string_list(case.get("reference_files"), "reference_files", case_id)

    return {
        "case_id": case_id,
        "title": case.get("title", ""),
        "prompt": case.get("prompt", ""),
        "source_regression_cases": case.get("source_regression_cases", []),
        "reference_files": reference_files,
        "boundary_statement_required": boundary_required,
        "structure": expected.get("structure", []),
        "agama_evidence": {
            "citation_required": {
                "required": citation_required,
                "status": "required" if citation_required else "not_required",
                "required_fields": ["sutra_name", "cbeta_id", "local_context_anchor"]
                if citation_required
                else [],
            },
            "search_scope": {
                "scope": search_scope,
                "status": "representative" if search_scope == "representative_search" else search_scope,
                "exhaustive": search_scope == "exhaustive_search",
            },
            "collation_boundary": {
                "required": collation_boundary,
                "status": "required" if collation_boundary else "not_required",
            },
            "reference_summary": _reference_summary(reference_files),
            "evidence_checks": _evidence_checks(
                citation_required=citation_required,
                search_scope=search_scope,
                collation_boundary=collation_boundary,
            ),
        },
        "diagnostics": _diagnostics(
            citation_required=citation_required,
            search_scope=search_scope,
            collation_boundary=collation_boundary,
            boundary_required=boundary_required,
        ),
    }


def build_agama_evidence_check(
    cases_path: Path = DEFAULT_CASES,
    *,
    case_id: str | None = None,
) -> dict[str, Any]:
    """Return structured Agama evidence checks from checked-in reasoning cases."""

    data = _load_yaml(cases_path)
    selected = _select_cases(_case_list(data), case_id)
    if case_id is not None and "agama_evidence" not in selected[0].get("contracts", []):
        raise AgamaEvidenceCheckerError(f"{case_id} is not an Agama evidence reasoning case.")

    evidence_reviews = [_check_case(case) for case in selected]

    return build_validator_output(
        validator=VALIDATOR,
        contract_family=CONTRACT_FAMILY,
        mode=MODE,
        output_schema=OUTPUT_SCHEMA,
        source=_display_path(cases_path),
        case_id=case_id,
        payload_key="evidence_reviews",
        payload=evidence_reviews,
        limitations=LIMITATIONS,
    )


def _render_text(result: dict[str, Any]) -> str:
    lines = [
        f"mode: {result['mode']}",
        f"source: {result['source']}",
    ]
    for item in result["evidence_reviews"]:
        evidence = item["agama_evidence"]
        lines.extend(
            [
                "",
                f"{item['case_id']}: {item['title']}",
                f"  prompt: {item['prompt']}",
                f"  citation_required: {evidence['citation_required']['status']}",
                f"  search_scope: {evidence['search_scope']['scope']}",
                f"  collation_boundary: {evidence['collation_boundary']['status']}",
            ]
        )
        if item["diagnostics"]:
            lines.append("  diagnostics:")
            for diagnostic in item["diagnostics"]:
                lines.append(f"  - {diagnostic['code']}: {diagnostic['message']}")
    lines.extend(["", "limitations:"])
    for item in result["limitations"]:
        lines.append(f"- {item}")
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        description="Check structured Agama evidence reasoning cases from tests/reasoning_cases.yaml."
    )
    parser.add_argument("--cases", type=Path, default=DEFAULT_CASES, help="Reasoning cases YAML path.")
    parser.add_argument("--case-id", help="Reasoning case id, such as ZR-05.")
    parser.add_argument("--json", action="store_true", dest="json_output", help="Emit machine-readable JSON.")
    args = parser.parse_args()

    try:
        result = build_agama_evidence_check(args.cases, case_id=args.case_id)
    except AgamaEvidenceCheckerError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    if args.json_output:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(_render_text(result), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
