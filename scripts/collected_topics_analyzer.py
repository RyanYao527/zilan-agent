from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CASES = ROOT / "tests" / "reasoning_cases.yaml"
MODE = "collected-topics-analyzer-v0"
OUTPUT_SCHEMA = "collected-topics-analyzer-output-v0"
LIMITATIONS = (
    "Prototype reads structured tests/reasoning_cases.yaml fixtures only.",
    "No natural-language concept parsing, provider calls, prompt changes, or doctrinal grading.",
)

RELATION_DEFINITIONS = {
    "pervasion": {
        "name": "pervasion",
        "role": "extension_inclusion_check",
        "description": "Check whether the stated reason is pervaded by the predicate.",
    },
    "total_part_distinction": {
        "name": "total-part distinction",
        "role": "total_part_boundary_check",
        "description": "Check whether a local part-case is being confused with a whole-category claim.",
    },
    "tetralemma": {
        "name": "tetralemma",
        "role": "fourfold_relation_check",
        "description": "Check the fourfold relation among the selected concepts.",
    },
}

RELATION_STATUS_LABELS = {
    "pass": "passes",
    "fail": "fails",
    "required": "required",
    "boundary": "boundary",
    "not_applicable": "not applicable",
}

DIAGNOSTIC_MESSAGES = {
    "pervasion": {
        "fail": {
            "code": "non_pervasive",
            "severity": "error",
            "message": "The fixture marks the pervasion relation as failed.",
        },
        "required": {
            "code": "pervasion_check_required",
            "severity": "info",
            "message": "The fixture requires an explicit pervasion check.",
        },
    },
    "total_part_distinction": {
        "required": {
            "code": "total_part_boundary_required",
            "severity": "info",
            "message": "The fixture requires explicit total/part distinction language.",
        },
    },
    "tetralemma": {
        "required": {
            "code": "tetralemma_check_required",
            "severity": "info",
            "message": "The fixture requires a fourfold relation check.",
        },
    },
}


class CollectedTopicsAnalyzerError(ValueError):
    """Raised when the structured Collected Topics fixture cannot be analyzed."""


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise CollectedTopicsAnalyzerError(f"Reasoning cases not found: {_display_path(path)}")

    try:
        import yaml  # type: ignore[import-not-found]
    except ModuleNotFoundError as exc:
        raise CollectedTopicsAnalyzerError("PyYAML is required to read reasoning cases.") from exc

    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001 - keep parser failures visible in CLI output.
        raise CollectedTopicsAnalyzerError(
            f"Failed to parse reasoning cases {_display_path(path)}: {exc}"
        ) from exc

    if not isinstance(data, dict):
        raise CollectedTopicsAnalyzerError(f"Reasoning cases must be a mapping: {_display_path(path)}")
    return data


def _case_list(data: dict[str, Any]) -> list[dict[str, Any]]:
    cases = data.get("cases")
    if not isinstance(cases, list) or not cases:
        raise CollectedTopicsAnalyzerError("Reasoning cases must contain a non-empty cases list.")
    if not all(isinstance(item, dict) for item in cases):
        raise CollectedTopicsAnalyzerError("Every reasoning case must be a mapping.")
    return cases


def _select_cases(cases: list[dict[str, Any]], case_id: str | None) -> list[dict[str, Any]]:
    if case_id is None:
        return [case for case in cases if "collected_topics" in case.get("contracts", [])]

    for case in cases:
        if case.get("id") == case_id:
            return [case]
    raise CollectedTopicsAnalyzerError(f"Unknown reasoning case id: {case_id}")


def _string_list(value: Any, field: str, case_id: str) -> list[str]:
    if not isinstance(value, list) or not all(isinstance(item, str) and item for item in value):
        raise CollectedTopicsAnalyzerError(f"{case_id} {field} must be a non-empty string list.")
    return list(value)


def _relation_check(check_id: str, status: Any) -> dict[str, Any]:
    status_text = status if isinstance(status, str) else "unknown"
    definition = RELATION_DEFINITIONS.get(
        check_id,
        {
            "name": check_id,
            "role": "custom_relation_check",
            "description": "Fixture-defined relation check.",
        },
    )
    return {
        "id": check_id,
        "name": definition["name"],
        "role": definition["role"],
        "status": status_text,
        "status_label": RELATION_STATUS_LABELS.get(status_text, "unknown"),
        "description": definition["description"],
    }


def _diagnostics(relation_checks: dict[str, Any], boundary_required: bool) -> list[dict[str, Any]]:
    diagnostics: list[dict[str, Any]] = []
    for check_id, status in relation_checks.items():
        status_messages = DIAGNOSTIC_MESSAGES.get(check_id, {})
        diagnostic = status_messages.get(status)
        if diagnostic is not None:
            diagnostics.append({**diagnostic, "check_id": check_id})
    if boundary_required:
        diagnostics.append(
            {
                "code": "boundary_statement_required",
                "severity": "info",
                "check_id": None,
                "message": "The fixture requires explicit boundary language.",
            }
        )
    return diagnostics


def _concept_items(terms: list[str]) -> list[dict[str, str]]:
    return [{"term": term, "role": "concept"} for term in terms]


def _analyze_case(case: dict[str, Any]) -> dict[str, Any]:
    case_id = case.get("id")
    expected = case.get("expected")
    if not isinstance(case_id, str) or not case_id:
        raise CollectedTopicsAnalyzerError("Every selected reasoning case must have a non-empty id.")
    if not isinstance(expected, dict):
        raise CollectedTopicsAnalyzerError(f"{case_id} expected must be a mapping.")

    collected_topics = expected.get("collected_topics")
    if not isinstance(collected_topics, dict):
        raise CollectedTopicsAnalyzerError(f"{case_id} expected.collected_topics must be a mapping.")

    concepts = _string_list(collected_topics.get("concepts"), "expected.collected_topics.concepts", case_id)
    relation_checks = collected_topics.get("relation_checks")
    if not isinstance(relation_checks, dict) or not relation_checks:
        raise CollectedTopicsAnalyzerError(
            f"{case_id} expected.collected_topics.relation_checks must be a non-empty mapping."
        )

    error_type = collected_topics.get("error_type")
    if not isinstance(error_type, str) or not error_type:
        raise CollectedTopicsAnalyzerError(f"{case_id} expected.collected_topics.error_type must be a string.")

    boundary_required = bool(expected.get("boundary_statement", False))

    return {
        "case_id": case_id,
        "title": case.get("title", ""),
        "prompt": case.get("prompt", ""),
        "source_regression_cases": case.get("source_regression_cases", []),
        "reference_files": case.get("reference_files", []),
        "boundary_statement_required": boundary_required,
        "structure": expected.get("structure", []),
        "collected_topics": {
            "concepts": _concept_items(concepts),
            "relation_checks": [
                _relation_check(check_id, status) for check_id, status in relation_checks.items()
            ],
            "error_type": error_type,
        },
        "diagnostics": _diagnostics(relation_checks, boundary_required),
    }


def build_collected_topics_analysis(
    cases_path: Path = DEFAULT_CASES,
    *,
    case_id: str | None = None,
) -> dict[str, Any]:
    """Return structured Collected Topics analyses from checked-in reasoning cases."""

    data = _load_yaml(cases_path)
    selected = _select_cases(_case_list(data), case_id)
    if case_id is not None and "collected_topics" not in selected[0].get("contracts", []):
        raise CollectedTopicsAnalyzerError(f"{case_id} is not a Collected Topics reasoning case.")

    analyses = [_analyze_case(case) for case in selected]

    return {
        "mode": MODE,
        "output_schema": OUTPUT_SCHEMA,
        "source": _display_path(cases_path),
        "case_id": case_id,
        "count": len(analyses),
        "analyses": analyses,
        "limitations": list(LIMITATIONS),
    }


def _render_text(result: dict[str, Any]) -> str:
    lines = [
        f"mode: {result['mode']}",
        f"source: {result['source']}",
    ]
    for item in result["analyses"]:
        collected_topics = item["collected_topics"]
        concepts = ", ".join(concept["term"] for concept in collected_topics["concepts"])
        checks = ", ".join(
            f"{check['id']}={check['status']}" for check in collected_topics["relation_checks"]
        )
        lines.extend(
            [
                "",
                f"{item['case_id']}: {item['title']}",
                f"  prompt: {item['prompt']}",
                f"  concepts: {concepts}",
                f"  relation_checks: {checks}",
                f"  error_type: {collected_topics['error_type']}",
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
        description="Analyze structured Collected Topics reasoning cases from tests/reasoning_cases.yaml."
    )
    parser.add_argument("--cases", type=Path, default=DEFAULT_CASES, help="Reasoning cases YAML path.")
    parser.add_argument("--case-id", help="Reasoning case id, such as ZR-02.")
    parser.add_argument("--json", action="store_true", dest="json_output", help="Emit machine-readable JSON.")
    args = parser.parse_args()

    try:
        result = build_collected_topics_analysis(args.cases, case_id=args.case_id)
    except CollectedTopicsAnalyzerError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    if args.json_output:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(_render_text(result), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
