from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from zilanlib.reasoning.contract_runner import build_reasoning_contract_run
from zilanlib.semantic.retrieval_dry_run import DEFAULT_FIXTURE, ROOT

MODE = "reasoning-alignment-report-v0"
OUTPUT_SCHEMA = "reasoning-alignment-report-output-v0"
REPORT_TITLE = "Reasoning Alignment Report"
ALIGNMENT_SECTION_IDS = (
    "claim",
    "agama_evidence",
    "hetuvidya_check",
    "collected_topics_boundary",
    "madhyamaka_boundary",
    "cognitive_mapping",
    "practice_boundary",
)
SECTION_ROLE_MAP = {
    "agama_evidence": "agama_evidence",
    "hetuvidya_check": "hetuvidya",
    "collected_topics_boundary": "collected_topics",
    "madhyamaka_boundary": "madhyamaka_prasanga",
    "cognitive_mapping": "cognitive_analysis",
}
LIMITATIONS = (
    "This is a local deterministic alignment report over checked-in fixtures and validators only.",
    "This report does not grade answer quality, doctrinal correctness, semantic similarity, or runtime behavior.",
    "No provider calls, live runtime calls, embeddings, vector search, or reranking are performed.",
    "Each reasoning system is checked independently; one present section cannot substitute for "
    "another missing section.",
    "This report does not change platform validation status.",
)


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _status_from_role_coverage(contract_run: dict[str, Any], role: str) -> tuple[str, str]:
    role_coverage = contract_run.get("role_coverage", {})
    missing_needs = role_coverage.get("missing_needs", [])
    if isinstance(missing_needs, list) and role in missing_needs:
        return "missing", "role_coverage_missing"
    needs = contract_run.get("retrieval", {}).get("needs", [])
    if isinstance(needs, list) and role not in needs:
        return "not_applicable", "role_not_declared"
    return "present", "role_coverage_present"


def _validator_case_ids(validator: dict[str, Any]) -> list[str]:
    case_ids = validator.get("case_ids")
    if not isinstance(case_ids, list):
        return []
    return [case_id for case_id in case_ids if isinstance(case_id, str)]


def _validator_section(contract_run: dict[str, Any], *, section_id: str, role: str) -> dict[str, Any]:
    status, reason = _status_from_role_coverage(contract_run, role)
    validators = contract_run.get("validators", {})
    validator = validators.get(role, {}) if isinstance(validators, dict) else {}
    validator_status = validator.get("status") if isinstance(validator, dict) else None
    case_ids = _validator_case_ids(validator) if isinstance(validator, dict) else []
    if status == "present" and validator_status != "run":
        status = "missing"
        reason = "validator_not_run"
    return {
        "id": section_id,
        "role": role,
        "status": status,
        "reason": reason,
        "validator_status": validator_status,
        "case_ids": case_ids,
        "limitations": [
            "Structured validator presence is a coverage signal, not a quality score.",
        ],
    }


def _claim_section(contract_run: dict[str, Any]) -> dict[str, Any]:
    query = contract_run.get("query")
    query_id = contract_run.get("query_id")
    return {
        "id": "claim",
        "status": "present" if isinstance(query, str) and query else "missing",
        "reason": "query_fixture_present" if isinstance(query, str) and query else "query_fixture_missing",
        "query_id": query_id,
        "claim": query if isinstance(query, str) else "",
        "case_ids": [query_id] if isinstance(query_id, str) else [],
        "limitations": [
            "The claim is the fixture query surface; this report does not infer a new thesis.",
        ],
    }


def _practice_boundary_section(contract_run: dict[str, Any]) -> dict[str, Any]:
    retrieval = contract_run.get("retrieval", {})
    role_coverage = contract_run.get("role_coverage", {})
    non_chunk_needs = role_coverage.get("non_chunk_needs", [])
    answer_boundary_contracts = retrieval.get("answer_boundary_contracts", {})
    declared = isinstance(non_chunk_needs, list) and "practice_boundary" in non_chunk_needs
    has_contract = isinstance(answer_boundary_contracts, dict) and "practice_boundary" in answer_boundary_contracts
    if declared and has_contract:
        status = "present"
        reason = "non_chunk_boundary_contract_present"
    elif declared:
        status = "missing"
        reason = "non_chunk_boundary_contract_missing"
    else:
        status = "not_applicable"
        reason = "practice_boundary_not_declared"
    return {
        "id": "practice_boundary",
        "role": "practice_boundary",
        "status": status,
        "reason": reason,
        "case_ids": [],
        "limitations": [
            "Practice boundary is a non-chunk answer-boundary contract, not a structured doctrine validator.",
        ],
    }


def _alignment(contract_run: dict[str, Any]) -> dict[str, dict[str, Any]]:
    sections: dict[str, dict[str, Any]] = {"claim": _claim_section(contract_run)}
    for section_id, role in SECTION_ROLE_MAP.items():
        sections[section_id] = _validator_section(contract_run, section_id=section_id, role=role)
    sections["practice_boundary"] = _practice_boundary_section(contract_run)
    return {section_id: sections[section_id] for section_id in ALIGNMENT_SECTION_IDS}


def _focus_reasoning_case_id(alignment: dict[str, dict[str, Any]]) -> str | None:
    counts: Counter[str] = Counter()
    for section in alignment.values():
        case_ids = section.get("case_ids")
        if isinstance(case_ids, list):
            counts.update(case_id for case_id in case_ids if isinstance(case_id, str) and case_id.startswith("ZR-"))
    if not counts:
        return None
    return sorted(counts.items(), key=lambda item: (-item[1], item[0]))[0][0]


def _summary(alignment: dict[str, dict[str, Any]]) -> dict[str, Any]:
    status_counts = Counter(str(section["status"]) for section in alignment.values())
    missing_sections = [
        section_id for section_id, section in alignment.items() if section.get("status") == "missing"
    ]
    return {
        "section_count": len(alignment),
        "status_counts": dict(sorted(status_counts.items())),
        "missing_sections": missing_sections,
    }


def build_reasoning_alignment_report(
    fixture_path: Path = DEFAULT_FIXTURE,
    *,
    query_id: str = "SRQ-01",
    cases_path: Path | None = None,
) -> dict[str, Any]:
    """Build a local cross-system reasoning alignment report for one SRQ fixture."""

    if cases_path is None:
        contract_run = build_reasoning_contract_run(fixture_path, query_id=query_id)
    else:
        contract_run = build_reasoning_contract_run(fixture_path, cases_path, query_id=query_id)
    alignment = _alignment(contract_run)
    return {
        "mode": MODE,
        "output_schema": OUTPUT_SCHEMA,
        "fixture": _display_path(fixture_path),
        "reasoning_cases": contract_run["reasoning_cases"],
        "query_id": contract_run["query_id"],
        "query": contract_run["query"],
        "focus_reasoning_case_id": _focus_reasoning_case_id(alignment),
        "summary": _summary(alignment),
        "alignment": alignment,
        "limitations": list(LIMITATIONS),
    }


def render_markdown_report(report: dict[str, Any]) -> str:
    lines = [
        f"# {REPORT_TITLE}",
        "",
        f"Query ID: `{report['query_id']}`",
        f"Focus reasoning case: `{report.get('focus_reasoning_case_id') or '-'}`",
        "",
        "| Section | Status | Reason | Case IDs |",
        "| --- | --- | --- | --- |",
    ]
    for section_id, section in report["alignment"].items():
        case_ids = section.get("case_ids", [])
        case_text = ", ".join(str(case_id) for case_id in case_ids) if isinstance(case_ids, list) else "-"
        lines.append(
            "| {section_id} | `{status}` | {reason} | {case_ids} |".format(
                section_id=section_id,
                status=section["status"],
                reason=section["reason"],
                case_ids=case_text or "-",
            )
        )
    lines.extend(["", "## Limitations", ""])
    lines.extend(f"- {limitation}" for limitation in report["limitations"])
    lines.append("")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description="Build a local reasoning alignment report.")
    parser.add_argument("--fixture", type=Path, default=DEFAULT_FIXTURE, help="Semantic chunks fixture YAML path.")
    parser.add_argument("--query-id", default="SRQ-01", help="Query fixture id to inspect.")
    parser.add_argument("--json", action="store_true", dest="json_output", help="Emit machine-readable JSON.")
    args = parser.parse_args(argv)

    report = build_reasoning_alignment_report(args.fixture, query_id=args.query_id)
    if args.json_output:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(render_markdown_report(report), end="")
    return 0
