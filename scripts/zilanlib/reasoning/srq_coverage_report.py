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


def _source_file(chunk: dict[str, Any] | None) -> str | None:
    if not isinstance(chunk, dict):
        return None
    source_file = chunk.get("source_file")
    return source_file if isinstance(source_file, str) and source_file else None


def _line_value(chunk: dict[str, Any] | None, field: str) -> int | None:
    if not isinstance(chunk, dict):
        return None
    value = chunk.get(field)
    return value if isinstance(value, int) and value > 0 else None


def _cbeta_id(chunk: dict[str, Any] | None) -> str | None:
    value = _metadata(chunk).get("cbeta_id")
    return value if isinstance(value, str) and value else None


def _line_text_hash(chunk: dict[str, Any] | None) -> str | None:
    metadata = _metadata(chunk)
    value = metadata.get("line_text_hash")
    if isinstance(value, str) and value:
        return value
    provenance = metadata.get("provenance")
    if isinstance(provenance, dict):
        provenance_value = provenance.get("line_text_hash")
        if isinstance(provenance_value, str) and provenance_value:
            return provenance_value
    return None


def _citation_value(chunk: dict[str, Any] | None, field: str) -> str | None:
    if not isinstance(chunk, dict):
        return None
    value = chunk.get(field)
    return value if isinstance(value, str) and value else None


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
        "source_file": _source_file(chunk),
        "start_line": _line_value(chunk, "start_line"),
        "end_line": _line_value(chunk, "end_line"),
        "citation": _citation_value(chunk, "citation"),
        "passage_citation": _citation_value(chunk, "passage_citation"),
        "cbeta_id": _cbeta_id(chunk),
        "section_label": section_label if isinstance(section_label, str) else None,
        "line_text_hash": _line_text_hash(chunk),
        "reasoning_roles": _reasoning_roles(chunk),
        "reasoning_case_id": reasoning_case_id,
        "reasoning_case_declared": reasoning_case_id in declared_reasoning_cases if reasoning_case_id else None,
    }


def _collation_candidate_sets(collation_path: Path, *, root: Path) -> list[dict[str, Any]]:
    if not collation_path.exists():
        return []
    data = _load_yaml(collation_path, root=root)
    candidate_sets = data.get("candidate_sets")
    if not isinstance(candidate_sets, list):
        raise SrqCoverageReportError(f"{_display(collation_path, root)} candidate_sets must be a list.")
    return [candidate_set for candidate_set in candidate_sets if isinstance(candidate_set, dict)]


def _candidate_set_chunk_ids(candidate_set: dict[str, Any]) -> set[str]:
    chunk_ids: set[str] = set()
    source_chunk_id = candidate_set.get("source_chunk_id")
    if isinstance(source_chunk_id, str) and source_chunk_id:
        chunk_ids.add(source_chunk_id)
    parallels = candidate_set.get("candidate_parallels")
    if isinstance(parallels, list):
        for parallel in parallels:
            if not isinstance(parallel, dict):
                continue
            chunk_id = parallel.get("chunk_id")
            if isinstance(chunk_id, str) and chunk_id:
                chunk_ids.add(chunk_id)
    return chunk_ids


def _related_collation_candidate_sets(
    *,
    expected_chunk_ids: list[str],
    collation_candidate_sets: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    expected = set(expected_chunk_ids)
    related: list[dict[str, Any]] = []
    for candidate_set in collation_candidate_sets:
        if expected.intersection(_candidate_set_chunk_ids(candidate_set)):
            related.append(candidate_set)
    return sorted(related, key=lambda candidate_set: str(candidate_set.get("set_id", "")))


def _claim_count(candidate_sets: list[dict[str, Any]], field: str) -> int:
    count = 0
    for candidate_set in candidate_sets:
        parallels = candidate_set.get("candidate_parallels")
        if not isinstance(parallels, list):
            continue
        for parallel in parallels:
            if isinstance(parallel, dict) and parallel.get(field) is True:
                count += 1
    return count


def _citation_metadata(
    *,
    expected_chunks: list[dict[str, Any]],
    related_candidate_sets: list[dict[str, Any]],
) -> dict[str, Any]:
    agama_chunks = [
        chunk
        for chunk in expected_chunks
        if chunk.get("chunk_type") == "agama_passage" or str(chunk.get("chunk_id", "")).startswith("agama:")
    ]
    chunk_ids = [str(chunk["chunk_id"]) for chunk in agama_chunks]
    missing_cbeta_id = [str(chunk["chunk_id"]) for chunk in agama_chunks if not chunk.get("cbeta_id")]
    missing_line_anchor = [
        str(chunk["chunk_id"])
        for chunk in agama_chunks
        if not chunk.get("source_file") or not chunk.get("start_line")
    ]
    missing_line_text_hash = [str(chunk["chunk_id"]) for chunk in agama_chunks if not chunk.get("line_text_hash")]
    missing_section_label = [str(chunk["chunk_id"]) for chunk in agama_chunks if not chunk.get("section_label")]
    candidate_set_ids = sorted(
        str(candidate_set.get("set_id"))
        for candidate_set in related_candidate_sets
        if isinstance(candidate_set.get("set_id"), str)
    )
    manual_statuses = sorted(
        {
            str(candidate_set.get("status"))
            for candidate_set in related_candidate_sets
            if isinstance(candidate_set.get("status"), str)
        }
    )

    if not agama_chunks:
        status = "not_applicable"
    elif missing_cbeta_id or missing_line_anchor or missing_line_text_hash:
        status = "missing"
    elif missing_section_label:
        status = "partial"
    else:
        status = "ready"

    return {
        "status": status,
        "agama_chunk_count": len(agama_chunks),
        "agama_chunk_ids": chunk_ids,
        "chunks_with_cbeta_id": len(agama_chunks) - len(missing_cbeta_id),
        "chunks_missing_cbeta_id": missing_cbeta_id,
        "chunks_with_line_anchor": len(agama_chunks) - len(missing_line_anchor),
        "chunks_missing_line_anchor": missing_line_anchor,
        "chunks_with_line_text_hash": len(agama_chunks) - len(missing_line_text_hash),
        "chunks_missing_line_text_hash": missing_line_text_hash,
        "chunks_with_section_label": len(agama_chunks) - len(missing_section_label),
        "chunks_missing_section_label": missing_section_label,
        "manual_collation_candidate_set_ids": candidate_set_ids,
        "manual_collation_statuses": manual_statuses,
        "equivalence_claims": _claim_count(related_candidate_sets, "equivalence_claim"),
        "source_dependence_claims": _claim_count(related_candidate_sets, "source_dependence_claim"),
        "publication_ready_claims": _claim_count(related_candidate_sets, "publication_ready"),
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
        return "fail"
    return "ready"


def _build_case(
    query: dict[str, Any],
    chunks_by_id: dict[str, dict[str, Any]],
    declared_reasoning_cases: set[str],
    evidence_records: list[dict[str, Any]],
    collation_candidate_sets: list[dict[str, Any]],
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
    related_candidate_sets = _related_collation_candidate_sets(
        expected_chunk_ids=expected_chunk_ids,
        collation_candidate_sets=collation_candidate_sets,
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
        "citation_metadata": _citation_metadata(
            expected_chunks=expected_chunks,
            related_candidate_sets=related_candidate_sets,
        ),
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
    collation_candidates_path: Path | None = None,
    manifest_path: Path | None = None,
    runtime_evidence_index_path: Path | None = None,
) -> dict[str, Any]:
    fixture_path = fixture_path or root / "tests" / "fixtures" / "retrieval_chunks" / "semantic_chunks.yaml"
    reasoning_cases_path = reasoning_cases_path or root / "tests" / "reasoning_cases.yaml"
    collation_candidates_path = (
        collation_candidates_path
        or root / "tests" / "fixtures" / "collation" / "high_value_no_self_parallel_candidates.yaml"
    )
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
    collation_candidate_sets = _collation_candidate_sets(collation_candidates_path, root=root)
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
            collation_candidate_sets,
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
            "collation_candidates": _display(collation_candidates_path, root),
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


def _markdown_citation_notes(citation_metadata: dict[str, Any]) -> str:
    notes: list[str] = []
    missing_section = citation_metadata.get("chunks_missing_section_label")
    if isinstance(missing_section, list) and missing_section:
        notes.append("missing section_label: " + ", ".join(str(chunk_id) for chunk_id in missing_section))
    missing_line_anchor = citation_metadata.get("chunks_missing_line_anchor")
    if isinstance(missing_line_anchor, list) and missing_line_anchor:
        notes.append("missing line anchor: " + ", ".join(str(chunk_id) for chunk_id in missing_line_anchor))
    candidate_ids = citation_metadata.get("manual_collation_candidate_set_ids")
    if isinstance(candidate_ids, list) and candidate_ids:
        notes.append(f"manual collation candidates: {len(candidate_ids)}")
    if citation_metadata.get("publication_ready_claims") == 0 and candidate_ids:
        notes.append("publication-ready claims: 0")
    return "; ".join(notes) or "-"


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

    lines.extend(
        [
            "",
            "## Citation Metadata",
            "",
            "This table audits citation metadata only. It does not prove textual equivalence, source dependence, "
            "publication-ready collation, runtime quality, or platform validation status.",
            "",
            "| SRQ | Citation status | Agama chunks | CBETA IDs | Line anchors | Section labels | Line hashes | "
            "Manual collation | Notes |",
            "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
        ]
    )
    for case in report["cases"]:
        citation_metadata = case["citation_metadata"]
        agama_count = citation_metadata["agama_chunk_count"]
        if agama_count == 0:
            continue
        candidate_ids = citation_metadata["manual_collation_candidate_set_ids"]
        manual_collation = (
            f"{len(candidate_ids)} candidate set(s)" if isinstance(candidate_ids, list) and candidate_ids else "-"
        )
        lines.append(
            "| {query_id} | `{status}` | {agama_count} | {cbeta_count}/{agama_count} | "
            "{line_count}/{agama_count} | {section_count}/{agama_count} | {hash_count}/{agama_count} | "
            "{manual_collation} | {notes} |".format(
                query_id=case["query_id"],
                status=citation_metadata["status"],
                agama_count=agama_count,
                cbeta_count=citation_metadata["chunks_with_cbeta_id"],
                line_count=citation_metadata["chunks_with_line_anchor"],
                section_count=citation_metadata["chunks_with_section_label"],
                hash_count=citation_metadata["chunks_with_line_text_hash"],
                manual_collation=manual_collation,
                notes=_markdown_citation_notes(citation_metadata),
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
