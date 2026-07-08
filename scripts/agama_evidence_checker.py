from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from reasoning_validator_output import build_validator_output

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CASES = ROOT / "tests" / "reasoning_cases.yaml"
DEFAULT_RETRIEVAL_FIXTURE = ROOT / "tests" / "fixtures" / "retrieval_chunks" / "semantic_chunks.yaml"
VALIDATOR = "agama_evidence_checker"
CONTRACT_FAMILY = "agama_evidence"
MODE = "agama-evidence-checker-v0.1"
OUTPUT_SCHEMA = "agama-evidence-checker-output-v0.1"
LIMITATIONS = (
    "Prototype reads structured tests/reasoning_cases.yaml fixtures only.",
    "Local evidence checks read checked-in semantic retrieval chunks and local Agama Markdown files.",
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
        raise AgamaEvidenceCheckerError(f"YAML file not found: {_display_path(path)}")

    try:
        import yaml  # type: ignore[import-not-found]
    except ModuleNotFoundError as exc:
        raise AgamaEvidenceCheckerError("PyYAML is required to read reasoning cases.") from exc

    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001 - keep parser failures visible in CLI output.
        raise AgamaEvidenceCheckerError(f"Failed to parse YAML {_display_path(path)}: {exc}") from exc

    if not isinstance(data, dict):
        raise AgamaEvidenceCheckerError(f"YAML file must be a mapping: {_display_path(path)}")
    return data


def _case_list(data: dict[str, Any]) -> list[dict[str, Any]]:
    cases = data.get("cases")
    if not isinstance(cases, list) or not cases:
        raise AgamaEvidenceCheckerError("Reasoning cases must contain a non-empty cases list.")
    if not all(isinstance(item, dict) for item in cases):
        raise AgamaEvidenceCheckerError("Every reasoning case must be a mapping.")
    return cases


def _chunk_list(data: dict[str, Any], fixture_path: Path) -> list[dict[str, Any]]:
    chunks = data.get("chunks")
    if not isinstance(chunks, list):
        raise AgamaEvidenceCheckerError(f"Retrieval fixture must contain a chunks list: {_display_path(fixture_path)}")
    if not all(isinstance(item, dict) for item in chunks):
        raise AgamaEvidenceCheckerError("Every retrieval chunk must be a mapping.")
    return chunks


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


def _file_kind(reference_file: str) -> str:
    if reference_file == "context/agama/agama-index.md":
        return "agama_index"
    if reference_file.startswith("context/agama/") and reference_file.endswith(".md"):
        return "agama_markdown"
    if reference_file == "scripts/search_agama.py":
        return "search_helper"
    return "other"


def _normalize_cbeta_id(value: str) -> str:
    return "".join(value.split()).lower()


def _source_lines(path: Path) -> list[str]:
    return path.read_text(encoding="utf-8").splitlines()


def _source_contains_text(path: Path, text: str, start_line: int, end_line: int) -> bool:
    lines = _source_lines(path)
    if start_line < 1 or end_line < start_line or end_line > len(lines):
        return False
    source_text = "\n".join(lines[start_line - 1 : end_line])
    return text.strip() in source_text


def _extract_cbeta_id(path: Path) -> str | None:
    if not path.exists():
        return None
    for line in _source_lines(path)[:20]:
        if "`T" not in line:
            continue
        start = line.find("`T")
        end = line.find("`", start + 1)
        if start != -1 and end != -1:
            return line[start + 1 : end]
    return None


def _index_text(index_path: Path) -> str:
    if not index_path.exists():
        return ""
    return index_path.read_text(encoding="utf-8")


def _reference_file_checks(reference_files: list[str], index_path: Path) -> list[dict[str, Any]]:
    index = _index_text(index_path)
    normalized_index = _normalize_cbeta_id(index)
    checks: list[dict[str, Any]] = []

    for reference_file in reference_files:
        path = ROOT / reference_file
        kind = _file_kind(reference_file)
        exists = path.exists()
        check: dict[str, Any] = {
            "path": reference_file,
            "kind": kind,
            "exists": exists,
            "status": "pass" if exists else "missing",
        }
        if kind == "agama_markdown":
            cbeta_id = _extract_cbeta_id(path)
            index_mentions_file = path.name in index
            index_mentions_cbeta = bool(cbeta_id and _normalize_cbeta_id(cbeta_id) in normalized_index)
            check.update(
                {
                    "cbeta_id": cbeta_id,
                    "index_mentions_file": index_mentions_file,
                    "index_mentions_cbeta": index_mentions_cbeta,
                    "status": "pass" if exists and index_mentions_file and index_mentions_cbeta else "fail",
                }
            )
        checks.append(check)
    return checks


def _index_check(reference_files: list[str]) -> dict[str, Any]:
    index_path = ROOT / "context" / "agama" / "agama-index.md"
    reference_checks = _reference_file_checks(reference_files, index_path)
    required_agama_files = [item for item in reference_checks if item["kind"] == "agama_markdown"]
    failures = [item["path"] for item in required_agama_files if item["status"] != "pass"]
    return {
        "path": "context/agama/agama-index.md",
        "exists": index_path.exists(),
        "required_agama_files": [item["path"] for item in required_agama_files],
        "missing_or_unindexed": failures,
        "status": "pass" if index_path.exists() and not failures else "fail",
    }


def _agama_passage_chunks(chunks: list[dict[str, Any]]) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for chunk in chunks:
        metadata = chunk.get("metadata")
        if not isinstance(metadata, dict):
            continue
        roles = metadata.get("reasoning_roles")
        if chunk.get("chunk_type") == "agama_passage" and isinstance(roles, list) and "agama_evidence" in roles:
            result.append(chunk)
    return result


def _passage_anchor_check(chunk: dict[str, Any]) -> dict[str, Any]:
    chunk_id = chunk.get("chunk_id")
    source_file = chunk.get("source_file")
    metadata = chunk.get("metadata")
    start_line = chunk.get("start_line")
    end_line = chunk.get("end_line")
    text = chunk.get("text")

    if not isinstance(chunk_id, str):
        raise AgamaEvidenceCheckerError("Agama passage chunk must have a string chunk_id.")
    if not isinstance(source_file, str):
        raise AgamaEvidenceCheckerError(f"{chunk_id} source_file must be a string.")
    if not isinstance(metadata, dict):
        raise AgamaEvidenceCheckerError(f"{chunk_id} metadata must be a mapping.")
    if not isinstance(start_line, int) or not isinstance(end_line, int):
        raise AgamaEvidenceCheckerError(f"{chunk_id} start_line and end_line must be integers.")
    if not isinstance(text, str) or not text:
        raise AgamaEvidenceCheckerError(f"{chunk_id} text must be a non-empty string.")

    path = ROOT / source_file
    exists = path.exists()
    line_range_status = "missing_file"
    cbeta_id = metadata.get("cbeta_id")
    cbeta_status = "missing_metadata"
    text_anchor_status = "missing_file"

    if exists:
        lines = _source_lines(path)
        line_range_status = "pass" if 1 <= start_line <= end_line <= len(lines) else "fail"
        extracted_cbeta = _extract_cbeta_id(path)
        cbeta_status = "pass" if isinstance(cbeta_id, str) and cbeta_id == extracted_cbeta else "fail"
        text_anchor_status = "pass" if _source_contains_text(path, text, start_line, end_line) else "fail"

    status = "pass" if exists and line_range_status == cbeta_status == text_anchor_status == "pass" else "fail"
    return {
        "chunk_id": chunk_id,
        "source_file": source_file,
        "start_line": start_line,
        "end_line": end_line,
        "cbeta_id": cbeta_id,
        "source_file_exists": exists,
        "line_range_status": line_range_status,
        "cbeta_id_status": cbeta_status,
        "text_anchor_status": text_anchor_status,
        "status": status,
    }


def _local_evidence(
    *,
    reference_files: list[str],
    retrieval_fixture_path: Path,
) -> dict[str, Any]:
    retrieval_fixture = _load_yaml(retrieval_fixture_path)
    passage_checks = [
        _passage_anchor_check(chunk)
        for chunk in _agama_passage_chunks(_chunk_list(retrieval_fixture, retrieval_fixture_path))
    ]
    reference_checks = _reference_file_checks(reference_files, ROOT / "context" / "agama" / "agama-index.md")
    index_check = _index_check(reference_files)
    failed_references = [item["path"] for item in reference_checks if item["status"] != "pass"]
    failed_passages = [item["chunk_id"] for item in passage_checks if item["status"] != "pass"]
    status = "pass" if not failed_references and not failed_passages and index_check["status"] == "pass" else "fail"
    return {
        "status": status,
        "retrieval_fixture": _display_path(retrieval_fixture_path),
        "index_check": index_check,
        "reference_file_checks": reference_checks,
        "passage_anchor_checks": passage_checks,
        "failed_references": failed_references,
        "failed_passage_anchors": failed_passages,
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
    local_evidence_status: str,
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
    if local_evidence_status == "pass":
        diagnostics.append(
            {
                "code": "local_evidence_anchors_verified",
                "severity": "info",
                "message": "Local index, file, CBETA id, line range, and fixture text anchors were found.",
            }
        )
    return diagnostics


def _check_case(case: dict[str, Any], retrieval_fixture_path: Path) -> dict[str, Any]:
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
    local_evidence = _local_evidence(reference_files=reference_files, retrieval_fixture_path=retrieval_fixture_path)

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
            "local_evidence": local_evidence,
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
            local_evidence_status=local_evidence["status"],
        ),
    }


def build_agama_evidence_check(
    cases_path: Path = DEFAULT_CASES,
    *,
    case_id: str | None = None,
    retrieval_fixture_path: Path = DEFAULT_RETRIEVAL_FIXTURE,
) -> dict[str, Any]:
    """Return structured Agama evidence checks from checked-in reasoning cases."""

    data = _load_yaml(cases_path)
    selected = _select_cases(_case_list(data), case_id)
    if case_id is not None and "agama_evidence" not in selected[0].get("contracts", []):
        raise AgamaEvidenceCheckerError(f"{case_id} is not an Agama evidence reasoning case.")

    evidence_reviews = [_check_case(case, retrieval_fixture_path) for case in selected]

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
                f"  local_evidence: {evidence['local_evidence']['status']}",
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
    parser.add_argument(
        "--retrieval-fixture",
        type=Path,
        default=DEFAULT_RETRIEVAL_FIXTURE,
        help="Semantic retrieval chunks YAML path.",
    )
    parser.add_argument("--case-id", help="Reasoning case id, such as ZR-05.")
    parser.add_argument("--json", action="store_true", dest="json_output", help="Emit machine-readable JSON.")
    args = parser.parse_args()

    try:
        result = build_agama_evidence_check(
            args.cases,
            case_id=args.case_id,
            retrieval_fixture_path=args.retrieval_fixture,
        )
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
