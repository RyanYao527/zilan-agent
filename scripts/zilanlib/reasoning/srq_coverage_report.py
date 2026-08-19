from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from zilanlib.yaml_io import display_path, load_yaml_mapping

ROOT = Path(__file__).resolve().parents[3]
DEFAULT_FIXTURE = ROOT / "tests" / "fixtures" / "retrieval_chunks" / "semantic_chunks.yaml"
DEFAULT_REASONING_CASES = ROOT / "tests" / "reasoning_cases.yaml"
DEFAULT_MANIFEST = ROOT / "docs" / "runtime-evidence" / "evidence_manifest.yaml"
DEFAULT_RUNTIME_EVIDENCE_INDEX = ROOT / "docs" / "runtime-evidence" / "index.md"
REPORT_VERSION = 1
REPORT_TITLE = "SRQ/ZR Evidence Coverage Report"
OUTPUT_SCHEMA = "srq-coverage-report-v1"
LIMITATIONS = (
    "Coverage/audit only; this report does not grade answer quality or prove runtime correctness.",
    "No provider calls, live runtime calls, embeddings, vector search, or reranking are performed.",
    "Runtime evidence status is read from a local manifest when present, otherwise from a conservative Markdown "
    "index fallback that requires manual review.",
    "This report does not change platform validation status.",
)
MANUAL_REVIEW_STATUSES = {"manual_review_required", "not_reviewed", "runtime_pending"}
STATUS_ORDER = {
    "pass": 0,
    "partial": 1,
    "fail_expected": 2,
    "fail": 3,
    "runtime_pending": 4,
    "not_reviewed": 5,
    "manual_review_required": 6,
}


class SrqCoverageReportError(ValueError):
    """Raised when local fixtures cannot be read into a coverage report."""


def _display(path: Path, root: Path) -> str:
    return display_path(path, root=root)


def _load_yaml(path: Path, *, root: Path) -> dict[str, Any]:
    return load_yaml_mapping(
        path,
        root=root,
        error_type=SrqCoverageReportError,
        missing_message="PyYAML is required to read SRQ coverage fixtures.",
        missing_file_label="Coverage fixture not found",
        parse_label="Failed to parse coverage fixture",
        mapping_label="Coverage fixture must be a mapping",
    )


def _mapping_list(data: dict[str, Any], field: str, *, source: str) -> list[dict[str, Any]]:
    values = data.get(field)
    if not isinstance(values, list):
        raise SrqCoverageReportError(f"{source} must contain a {field} list.")
    if not all(isinstance(item, dict) for item in values):
        raise SrqCoverageReportError(f"{source} {field} entries must be mappings.")
    return list(values)


def _chunk_id(chunk: dict[str, Any]) -> str | None:
    chunk_id = chunk.get("chunk_id")
    return chunk_id if isinstance(chunk_id, str) and chunk_id else None


def _query_id(query: dict[str, Any]) -> str | None:
    query_id = query.get("id")
    return query_id if isinstance(query_id, str) and query_id.startswith("SRQ-") else None


def _srq_sort_key(query: dict[str, Any]) -> tuple[int, str]:
    query_id = str(query.get("id", ""))
    match = re.match(r"^SRQ-(\d+)$", query_id)
    if match:
        return int(match.group(1)), query_id
    return 9999, query_id


def _string_list(value: object) -> list[str]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, str) and item]


def _metadata(chunk: dict[str, Any] | None) -> dict[str, Any]:
    if chunk is None:
        return {}
    value = chunk.get("metadata")
    return value if isinstance(value, dict) else {}


def _reasoning_roles(chunk: dict[str, Any] | None) -> list[str]:
    roles = _metadata(chunk).get("reasoning_roles")
    return _string_list(roles)


def _reasoning_case_id_from_chunk_id(chunk_id: str) -> str | None:
    parts = chunk_id.split(":")
    if len(parts) >= 2 and parts[0] == "reasoning" and parts[1].startswith("ZR-"):
        return parts[1]
    return None


def _reasoning_case_id(chunk_id: str, chunk: dict[str, Any] | None) -> str | None:
    metadata_case_id = _metadata(chunk).get("reasoning_case_id")
    if isinstance(metadata_case_id, str) and metadata_case_id.startswith("ZR-"):
        return metadata_case_id
    return _reasoning_case_id_from_chunk_id(chunk_id)


def _reasoning_case_ids(cases_path: Path, *, root: Path) -> set[str]:
    data = _load_yaml(cases_path, root=root)
    cases = _mapping_list(data, "cases", source=_display(cases_path, root))
    ids: set[str] = set()
    for case in cases:
        case_id = case.get("id")
        if isinstance(case_id, str) and case_id.startswith("ZR-"):
            ids.add(case_id)
    return ids


def _sample_coverage(query: dict[str, Any]) -> dict[str, Any]:
    samples: list[dict[str, Any]] = []
    for field in ("answer_contract_samples", "answer_boundary_samples"):
        value = query.get(field)
        if isinstance(value, list):
            samples.extend(item for item in value if isinstance(item, dict))

    status_counts: Counter[str] = Counter()
    sample_ids: list[str] = []
    for sample in samples:
        sample_id = sample.get("id")
        if isinstance(sample_id, str):
            sample_ids.append(sample_id)
        status = sample.get("expected_status")
        if isinstance(status, str):
            status_counts[status] += 1

    return {
        "total": len(samples),
        "pass_count": status_counts.get("pass", 0),
        "fail_count": status_counts.get("fail", 0),
        "expected_status_counts": dict(sorted(status_counts.items())),
        "has_pass_sample": status_counts.get("pass", 0) > 0,
        "has_fail_sample": status_counts.get("fail", 0) > 0,
        "sample_ids": sample_ids,
    }


def _chunk_summary(
    chunk_id: str,
    chunk: dict[str, Any] | None,
    *,
    declared_reasoning_cases: set[str],
) -> dict[str, Any]:
    metadata = _metadata(chunk)
    reasoning_case_id = _reasoning_case_id(chunk_id, chunk)
    section_label = metadata.get("section_label")
    return {
        "chunk_id": chunk_id,
        "exists": chunk is not None,
        "chunk_type": chunk.get("chunk_type") if isinstance(chunk, dict) else None,
        "section_label": section_label if isinstance(section_label, str) else None,
        "reasoning_roles": _reasoning_roles(chunk),
        "reasoning_case_id": reasoning_case_id,
        "reasoning_case_declared": reasoning_case_id in declared_reasoning_cases if reasoning_case_id else None,
    }


def _ordered_statuses(statuses: list[str]) -> list[str]:
    unique_statuses = set(statuses)
    return sorted(unique_statuses, key=lambda status: (STATUS_ORDER.get(status, 99), status))


def _manifest_evidence_by_query(manifest_path: Path, *, root: Path) -> dict[str, list[dict[str, Any]]]:
    data = _load_yaml(manifest_path, root=root)
    entries = data.get("entries")
    if not isinstance(entries, list):
        raise SrqCoverageReportError(f"{_display(manifest_path, root)} entries must be a list.")

    evidence_by_query: dict[str, list[dict[str, Any]]] = {}
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        entry_id = entry.get("id")
        entry_file = entry.get("file")
        date = entry.get("date")
        evidence_class = entry.get("evidence_class")
        reviews = entry.get("reviews")
        if not isinstance(reviews, list):
            continue
        for review in reviews:
            if not isinstance(review, dict):
                continue
            query_id = review.get("query_id")
            status = review.get("status")
            if not isinstance(query_id, str) or not query_id.startswith("SRQ-"):
                continue
            if not isinstance(status, str):
                continue
            record = {
                "entry_id": entry_id if isinstance(entry_id, str) else "",
                "file": entry_file if isinstance(entry_file, str) else "",
                "date": date if isinstance(date, str) else "",
                "evidence_class": evidence_class if isinstance(evidence_class, str) else "",
                "status": status,
                "source_file": review.get("source_file") if isinstance(review.get("source_file"), str) else None,
                "batch": review.get("batch") if isinstance(review.get("batch"), str) else None,
                "notes": review.get("notes") if isinstance(review.get("notes"), str) else "",
                "answer_file_safe": entry.get("answer_file_safe") is True,
                "platform_status_change": entry.get("platform_status_change") is True,
            }
            evidence_by_query.setdefault(query_id, []).append(record)
    for records in evidence_by_query.values():
        records.sort(key=lambda item: (str(item["date"]), str(item["entry_id"]), str(item["status"])))
    return evidence_by_query


def _markdown_index_evidence_by_query(
    index_path: Path,
    query_ids: list[str],
    *,
    root: Path,
) -> dict[str, list[dict[str, Any]]]:
    if not index_path.exists():
        return {}
    text = index_path.read_text(encoding="utf-8")
    evidence_by_query: dict[str, list[dict[str, Any]]] = {}
    for query_id in query_ids:
        if query_id not in text:
            continue
        evidence_by_query[query_id] = [
            {
                "entry_id": "markdown-index-mention",
                "file": _display(index_path, root),
                "date": "",
                "evidence_class": "markdown_index",
                "status": "manual_review_required",
                "source_file": None,
                "batch": None,
                "notes": "Markdown index mentions this SRQ; machine-readable status requires manual review.",
                "answer_file_safe": False,
                "platform_status_change": False,
            }
        ]
    return evidence_by_query


def _runtime_evidence_summary(
    records: list[dict[str, Any]],
    *,
    source: str,
) -> dict[str, Any]:
    statuses = _ordered_statuses([str(record.get("status", "")) for record in records if record.get("status")])
    status_by_evidence_class: dict[str, list[str]] = {}
    for record in records:
        evidence_class = str(record.get("evidence_class") or "unknown")
        status = record.get("status")
        if isinstance(status, str) and status:
            status_by_evidence_class.setdefault(evidence_class, []).append(status)
    status_by_evidence_class = {
        evidence_class: _ordered_statuses(class_statuses)
        for evidence_class, class_statuses in sorted(status_by_evidence_class.items())
    }
    latest = records[-1] if records else None
    return {
        "source": source,
        "statuses": statuses if statuses else ["not_reviewed"],
        "status_by_evidence_class": status_by_evidence_class,
        "latest_status": latest["status"] if latest else "not_reviewed",
        "latest_entry": latest,
        "entry_count": len(records),
        "entries": records,
    }


def _readiness(
    *,
    expected_chunks: list[dict[str, Any]],
    sample_coverage: dict[str, Any],
    runtime_evidence: dict[str, Any],
) -> str:
    if any(chunk["exists"] is not True for chunk in expected_chunks):
        return "missing"
    if sample_coverage["has_pass_sample"] is not True or sample_coverage["has_fail_sample"] is not True:
        return "partial"
    latest_status = runtime_evidence.get("latest_status")
    statuses = runtime_evidence.get("statuses")
    status_set = set(statuses) if isinstance(statuses, list) else set()
    if latest_status in MANUAL_REVIEW_STATUSES:
        return "manual_review_required"
    if "fail" in status_set and "pass" not in status_set:
        return "partial"
    return "ready"


def _build_case(
    query: dict[str, Any],
    chunks_by_id: dict[str, dict[str, Any]],
    declared_reasoning_cases: set[str],
    evidence_records: list[dict[str, Any]],
    *,
    runtime_evidence_source: str,
) -> dict[str, Any]:
    query_id = str(query["id"])
    expected_chunk_ids = _string_list(query.get("expected_chunk_ids"))
    expected_chunks = [
        _chunk_summary(chunk_id, chunks_by_id.get(chunk_id), declared_reasoning_cases=declared_reasoning_cases)
        for chunk_id in expected_chunk_ids
    ]
    related_case_ids = sorted(
        {
            chunk["reasoning_case_id"]
            for chunk in expected_chunks
            if isinstance(chunk.get("reasoning_case_id"), str)
        }
    )
    sample_coverage = _sample_coverage(query)
    runtime_evidence = _runtime_evidence_summary(evidence_records, source=runtime_evidence_source)
    return {
        "query_id": query_id,
        "query": query.get("query") if isinstance(query.get("query"), str) else "",
        "needs": _string_list(query.get("needs")),
        "expected_chunk_ids": expected_chunk_ids,
        "expected_chunks": expected_chunks,
        "missing_expected_chunk_ids": [chunk["chunk_id"] for chunk in expected_chunks if chunk["exists"] is not True],
        "related_reasoning_case_ids": related_case_ids,
        "reasoning_case_links": [
            {"case_id": case_id, "exists_in_reasoning_cases": case_id in declared_reasoning_cases}
            for case_id in related_case_ids
        ],
        "sample_coverage": sample_coverage,
        "runtime_evidence": runtime_evidence,
        "coverage_status": _readiness(
            expected_chunks=expected_chunks,
            sample_coverage=sample_coverage,
            runtime_evidence=runtime_evidence,
        ),
    }


def _summary(cases: list[dict[str, Any]]) -> dict[str, Any]:
    coverage_counts = Counter(str(case["coverage_status"]) for case in cases)
    return {
        "case_count": len(cases),
        "coverage_status_counts": dict(sorted(coverage_counts.items())),
        "cases_with_missing_chunks": [
            case["query_id"] for case in cases if case.get("missing_expected_chunk_ids")
        ],
        "cases_requiring_manual_review": [
            case["query_id"] for case in cases if case["coverage_status"] == "manual_review_required"
        ],
    }


def build_srq_coverage_report(
    root: Path = ROOT,
    *,
    fixture_path: Path | None = None,
    reasoning_cases_path: Path | None = None,
    manifest_path: Path | None = None,
    runtime_evidence_index_path: Path | None = None,
) -> dict[str, Any]:
    fixture_path = fixture_path or root / "tests" / "fixtures" / "retrieval_chunks" / "semantic_chunks.yaml"
    reasoning_cases_path = reasoning_cases_path or root / "tests" / "reasoning_cases.yaml"
    manifest_path = manifest_path or root / "docs" / "runtime-evidence" / "evidence_manifest.yaml"
    runtime_evidence_index_path = runtime_evidence_index_path or root / "docs" / "runtime-evidence" / "index.md"

    fixture = _load_yaml(fixture_path, root=root)
    chunks = _mapping_list(fixture, "chunks", source=_display(fixture_path, root))
    queries = [
        query for query in _mapping_list(fixture, "queries", source=_display(fixture_path, root)) if _query_id(query)
    ]
    queries.sort(key=_srq_sort_key)
    chunks_by_id = {chunk_id: chunk for chunk in chunks if (chunk_id := _chunk_id(chunk)) is not None}
    declared_reasoning_cases = _reasoning_case_ids(reasoning_cases_path, root=root)
    query_ids = [str(query["id"]) for query in queries]

    if manifest_path.exists():
        runtime_evidence_source = "manifest"
        evidence_by_query = _manifest_evidence_by_query(manifest_path, root=root)
    else:
        runtime_evidence_source = "markdown_index"
        evidence_by_query = _markdown_index_evidence_by_query(runtime_evidence_index_path, query_ids, root=root)

    cases = [
        _build_case(
            query,
            chunks_by_id,
            declared_reasoning_cases,
            evidence_by_query.get(str(query["id"]), []),
            runtime_evidence_source=runtime_evidence_source,
        )
        for query in queries
    ]
    return {
        "version": REPORT_VERSION,
        "source": {
            "output_schema": OUTPUT_SCHEMA,
            "fixture": _display(fixture_path, root),
            "reasoning_cases": _display(reasoning_cases_path, root),
        },
        "runtime_evidence_source": runtime_evidence_source,
        "summary": _summary(cases),
        "cases": cases,
        "limitations": list(LIMITATIONS),
    }


def _markdown_status(case: dict[str, Any]) -> str:
    runtime_evidence = case["runtime_evidence"]
    status_by_class = runtime_evidence.get("status_by_evidence_class")
    if isinstance(status_by_class, dict) and status_by_class:
        parts = []
        for evidence_class, statuses in sorted(status_by_class.items()):
            status_text = ", ".join(str(status) for status in statuses) if isinstance(statuses, list) else str(statuses)
            parts.append(f"{evidence_class}: {status_text}")
        return "; ".join(parts)
    statuses = runtime_evidence.get("statuses", [])
    if isinstance(statuses, list):
        return ", ".join(str(status) for status in statuses)
    return "unknown"


def render_markdown_report(report: dict[str, Any]) -> str:
    lines = [
        f"# {REPORT_TITLE}",
        "",
        "This is a local developer-facing coverage/audit report. It does not change platform validation status.",
        "",
        "## Summary",
        "",
        f"- Runtime evidence source: `{report['runtime_evidence_source']}`",
        f"- Cases: `{report['summary']['case_count']}`",
        f"- Coverage counts: `{report['summary']['coverage_status_counts']}`",
        "",
        "## Case Triage",
        "",
        "| SRQ | Coverage | Samples | Chunks | ZR links | Runtime evidence | Notes |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for case in report["cases"]:
        samples = case["sample_coverage"]
        chunk_total = len(case["expected_chunks"])
        chunk_missing = len(case["missing_expected_chunk_ids"])
        zr_links = ", ".join(case["related_reasoning_case_ids"]) or "-"
        runtime_status = _markdown_status(case)
        notes = "manual review required" if case["coverage_status"] == "manual_review_required" else "-"
        lines.append(
            "| {query_id} | `{coverage}` | pass={pass_count}, fail={fail_count} | "
            "{present}/{total} present | {zr_links} | {runtime_status} | {notes} |".format(
                query_id=case["query_id"],
                coverage=case["coverage_status"],
                pass_count=samples["pass_count"],
                fail_count=samples["fail_count"],
                present=chunk_total - chunk_missing,
                total=chunk_total,
                zr_links=zr_links,
                runtime_status=runtime_status,
                notes=notes,
            )
        )

    lines.extend(["", "## Limitations", ""])
    lines.extend(f"- {limitation}" for limitation in report["limitations"])
    lines.append(
        "- `manual_review_required` means the report can locate evidence pointers, "
        "not that runtime quality passed."
    )
    lines.append("")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description="Build a local SRQ/ZR evidence coverage report.")
    parser.add_argument("--json", action="store_true", dest="json_output", help="Emit machine-readable JSON.")
    args = parser.parse_args(argv)

    try:
        report = build_srq_coverage_report(ROOT)
    except SrqCoverageReportError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    if args.json_output:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(render_markdown_report(report), end="")
    return 0
