from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Any

from zilanlib.reasoning.validator_output import build_validator_output
from zilanlib.repository import detect_source_root
from zilanlib.yaml_io import display_path, load_yaml_mapping

ROOT = Path(__file__).resolve().parents[3]
DEFAULT_CASES = ROOT / "tests" / "reasoning_cases.yaml"
DEFAULT_RETRIEVAL_FIXTURE = ROOT / "tests" / "fixtures" / "retrieval_chunks" / "semantic_chunks.yaml"
DEFAULT_COLLATION_CANDIDATES = ROOT / "tests" / "fixtures" / "collation" / "high_value_no_self_parallel_candidates.yaml"
DEFAULT_XML_ANCHOR_PROBES = ROOT / "tests" / "fixtures" / "collation" / "cbeta_anchor_probes.yaml"
DEFAULT_REVIEWER_DECISIONS = (
    ROOT / "tests" / "fixtures" / "collation" / "srq04_manual_semantic_boundary_decisions.yaml"
)
DEFAULT_SOURCE_ROOT = detect_source_root(ROOT)
VALIDATOR = "agama_evidence_checker"
CONTRACT_FAMILY = "agama_evidence"
MODE = "agama-evidence-checker-v0.1"
OUTPUT_SCHEMA = "agama-evidence-checker-output-v0.1"
LIMITATIONS = (
    "Prototype reads structured tests/reasoning_cases.yaml fixtures only.",
    "Local evidence checks read checked-in semantic retrieval chunks and local Agama Markdown files.",
    "No Agama search execution, CBETA XML collation, provider calls, prompt changes, or citation grading.",
)
PACKAGE_LOCAL_EVIDENCE_LIMITATION = (
    "Local Agama source-anchor checks require a source checkout; bundled zilan_contract package fixtures "
    "do not include the full context/agama corpus."
)


class AgamaEvidenceCheckerError(ValueError):
    """Raised when the structured Agama evidence fixture cannot be checked."""


def _display_path(path: Path) -> str:
    return display_path(path, root=ROOT)


def _load_yaml(path: Path) -> dict[str, Any]:
    return load_yaml_mapping(
        path,
        root=ROOT,
        error_type=AgamaEvidenceCheckerError,
        missing_message="PyYAML is required to read reasoning cases.",
        missing_file_label="YAML file not found",
        parse_label="Failed to parse YAML",
        mapping_label="YAML file must be a mapping",
    )


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


def _optional_mapping_list(data: dict[str, Any], field: str, source: Path) -> list[dict[str, Any]]:
    values = data.get(field)
    if values is None:
        return []
    if not isinstance(values, list):
        raise AgamaEvidenceCheckerError(f"{_display_path(source)} {field} must be a list.")
    return [item for item in values if isinstance(item, dict)]


def _collation_candidate_sets(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    return _optional_mapping_list(_load_yaml(path), "candidate_sets", path)


def _anchor_probes_by_id(path: Path) -> dict[str, dict[str, Any]]:
    if not path.exists():
        return {}
    probes: dict[str, dict[str, Any]] = {}
    for probe in _optional_mapping_list(_load_yaml(path), "anchor_probes", path):
        probe_id = probe.get("probe_id")
        if isinstance(probe_id, str) and probe_id:
            probes[probe_id] = probe
    return probes


def _reviewer_decisions(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    return _optional_mapping_list(_load_yaml(path), "decisions", path)


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


def _reference_file_checks(
    reference_files: list[str],
    index_path: Path,
    source_root: Path,
) -> list[dict[str, Any]]:
    index = _index_text(index_path)
    normalized_index = _normalize_cbeta_id(index)
    checks: list[dict[str, Any]] = []

    for reference_file in reference_files:
        path = source_root / reference_file
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


def _index_check(reference_files: list[str], source_root: Path) -> dict[str, Any]:
    index_path = source_root / "context" / "agama" / "agama-index.md"
    reference_checks = _reference_file_checks(reference_files, index_path, source_root)
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


def _passage_anchor_check(chunk: dict[str, Any], source_root: Path) -> dict[str, Any]:
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

    path = source_root / source_file
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
    source_root: Path | None,
) -> dict[str, Any]:
    retrieval_fixture = _load_yaml(retrieval_fixture_path)
    chunks = _chunk_list(retrieval_fixture, retrieval_fixture_path)

    if source_root is None:
        return {
            "status": "not_applicable",
            "retrieval_fixture": _display_path(retrieval_fixture_path),
            "source_root": None,
            "index_check": {
                "path": "context/agama/agama-index.md",
                "exists": False,
                "required_agama_files": [],
                "missing_or_unindexed": [],
                "status": "not_applicable",
            },
            "reference_file_checks": [],
            "passage_anchor_checks": [],
            "failed_references": [],
            "failed_passage_anchors": [],
            "limitations": [PACKAGE_LOCAL_EVIDENCE_LIMITATION],
        }

    passage_checks = [_passage_anchor_check(chunk, source_root) for chunk in _agama_passage_chunks(chunks)]
    reference_checks = _reference_file_checks(
        reference_files,
        source_root / "context" / "agama" / "agama-index.md",
        source_root,
    )
    index_check = _index_check(reference_files, source_root)
    failed_references = [item["path"] for item in reference_checks if item["status"] != "pass"]
    failed_passages = [item["chunk_id"] for item in passage_checks if item["status"] != "pass"]
    status = "pass" if not failed_references and not failed_passages and index_check["status"] == "pass" else "fail"
    return {
        "status": status,
        "retrieval_fixture": _display_path(retrieval_fixture_path),
        "source_root": _display_path(source_root),
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


def _parallel_field_values(candidate_sets: list[dict[str, Any]], field: str) -> list[str]:
    values: set[str] = set()
    for candidate_set in candidate_sets:
        parallels = candidate_set.get("candidate_parallels")
        if not isinstance(parallels, list):
            continue
        for parallel in parallels:
            if not isinstance(parallel, dict):
                continue
            value = parallel.get(field)
            if isinstance(value, str) and value:
                values.add(value)
    return sorted(values)


def _candidate_set_ids(candidate_sets: list[dict[str, Any]]) -> list[str]:
    return sorted(
        str(candidate_set.get("set_id"))
        for candidate_set in candidate_sets
        if isinstance(candidate_set.get("set_id"), str)
    )


def _reviewer_decision_summary(
    *,
    candidate_sets: list[dict[str, Any]],
    reviewer_decisions: list[dict[str, Any]],
) -> dict[str, Any]:
    candidate_ids = set(_candidate_set_ids(candidate_sets))
    related_decisions = [
        decision
        for decision in reviewer_decisions
        if isinstance(decision.get("candidate_set_id"), str)
        and str(decision["candidate_set_id"]) in candidate_ids
    ]
    status_counts: Counter[str] = Counter(
        str(decision["status"])
        for decision in related_decisions
        if isinstance(decision.get("status"), str) and decision.get("status")
    )

    def ids_for(status: str) -> list[str]:
        return sorted(
            str(decision["candidate_set_id"])
            for decision in related_decisions
            if decision.get("status") == status and isinstance(decision.get("candidate_set_id"), str)
        )

    return {
        "reviewer_decision_status_counts": dict(sorted(status_counts.items())),
        "pending_reviewer_decisions": ids_for("pending_reviewer_decision"),
        "limited_theme_parallel_confirmed": ids_for("limited_theme_parallel_confirmed"),
        "stronger_claim_requires_separate_evidence": ids_for("stronger_claim_requires_separate_evidence"),
    }


def _candidate_anchor_probe_ids(candidate_sets: list[dict[str, Any]]) -> list[str]:
    probe_ids: set[str] = set()
    for candidate_set in candidate_sets:
        source_anchor_probe = candidate_set.get("source_anchor_probe")
        if isinstance(source_anchor_probe, str) and source_anchor_probe:
            probe_ids.add(source_anchor_probe)
        parallels = candidate_set.get("candidate_parallels")
        if not isinstance(parallels, list):
            continue
        for parallel in parallels:
            if not isinstance(parallel, dict):
                continue
            anchor_probe = parallel.get("anchor_probe")
            if isinstance(anchor_probe, str) and anchor_probe:
                probe_ids.add(anchor_probe)
    return sorted(probe_ids)


def _manual_collation_boundary(
    *,
    collation_boundary_required: bool,
    candidate_sets: list[dict[str, Any]],
    anchor_probes: dict[str, dict[str, Any]],
    reviewer_decisions: list[dict[str, Any]],
) -> dict[str, Any]:
    if not collation_boundary_required:
        return {
            "status": "not_required",
            "anchor_located": False,
            "limited_theme_parallel": False,
            "textual_equivalence_claim": False,
            "source_dependence_claim": False,
            "publication_ready": False,
            "candidate_set_ids": [],
            "missing_xml_anchor_probe_ids": [],
            "xml_anchor_probe_statuses": [],
            "parallel_collation_statuses": [],
            "reviewer_decision_status_counts": {},
            "pending_reviewer_decisions": [],
            "limited_theme_parallel_confirmed": [],
            "stronger_claim_requires_separate_evidence": [],
            "limitations": [],
        }

    candidate_set_ids = _candidate_set_ids(candidate_sets)
    probe_ids = _candidate_anchor_probe_ids(candidate_sets)
    missing_probe_ids = [probe_id for probe_id in probe_ids if probe_id not in anchor_probes]
    probe_statuses = sorted(
        {
            str(anchor_probes[probe_id].get("collation_status"))
            for probe_id in probe_ids
            if probe_id in anchor_probes and isinstance(anchor_probes[probe_id].get("collation_status"), str)
        }
    )
    parallel_statuses = _parallel_field_values(candidate_sets, "collation_status")
    textual_equivalence_claim = _claim_count(candidate_sets, "equivalence_claim") > 0
    source_dependence_claim = _claim_count(candidate_sets, "source_dependence_claim") > 0
    publication_ready = _claim_count(candidate_sets, "publication_ready") > 0
    limited_theme_parallel = (
        "manual_xml_p5_theme_parallel_reviewed" in parallel_statuses
        and not textual_equivalence_claim
        and not source_dependence_claim
        and not publication_ready
    )
    anchor_located = bool(probe_ids) and not missing_probe_ids
    status = "publication_ready" if publication_ready else "manual_review_required"
    reviewer_decision_summary = _reviewer_decision_summary(
        candidate_sets=candidate_sets,
        reviewer_decisions=reviewer_decisions,
    )

    return {
        "status": status,
        "anchor_located": anchor_located,
        "limited_theme_parallel": limited_theme_parallel,
        "textual_equivalence_claim": textual_equivalence_claim,
        "source_dependence_claim": source_dependence_claim,
        "publication_ready": publication_ready,
        "candidate_set_ids": candidate_set_ids,
        "missing_xml_anchor_probe_ids": missing_probe_ids,
        "xml_anchor_probe_statuses": probe_statuses,
        "parallel_collation_statuses": parallel_statuses,
        **reviewer_decision_summary,
        "limitations": [
            "Anchor location does not prove textual equivalence",
            "Limited theme-parallel review does not prove source dependence",
            "Manual collation boundary does not change runtime or platform validation status",
        ],
    }


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
    if local_evidence_status == "not_applicable":
        diagnostics.append(
            {
                "code": "local_evidence_anchors_not_available",
                "severity": "info",
                "message": PACKAGE_LOCAL_EVIDENCE_LIMITATION,
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


def _check_case(
    case: dict[str, Any],
    retrieval_fixture_path: Path,
    source_root: Path | None,
    candidate_sets: list[dict[str, Any]],
    anchor_probes: dict[str, dict[str, Any]],
    reviewer_decisions: list[dict[str, Any]],
) -> dict[str, Any]:
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
    local_evidence = _local_evidence(
        reference_files=reference_files,
        retrieval_fixture_path=retrieval_fixture_path,
        source_root=source_root,
    )

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
            "manual_collation_boundary": _manual_collation_boundary(
                collation_boundary_required=collation_boundary,
                candidate_sets=candidate_sets,
                anchor_probes=anchor_probes,
                reviewer_decisions=reviewer_decisions,
            ),
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
    collation_candidates_path: Path = DEFAULT_COLLATION_CANDIDATES,
    anchor_probes_path: Path = DEFAULT_XML_ANCHOR_PROBES,
    reviewer_decisions_path: Path = DEFAULT_REVIEWER_DECISIONS,
    source_root: Path | None = DEFAULT_SOURCE_ROOT,
) -> dict[str, Any]:
    """Return structured Agama evidence checks from checked-in reasoning cases."""

    data = _load_yaml(cases_path)
    selected = _select_cases(_case_list(data), case_id)
    if case_id is not None and "agama_evidence" not in selected[0].get("contracts", []):
        raise AgamaEvidenceCheckerError(f"{case_id} is not an Agama evidence reasoning case.")

    candidate_sets = _collation_candidate_sets(collation_candidates_path)
    anchor_probes = _anchor_probes_by_id(anchor_probes_path)
    reviewer_decisions = _reviewer_decisions(reviewer_decisions_path)
    evidence_reviews = [
        _check_case(case, retrieval_fixture_path, source_root, candidate_sets, anchor_probes, reviewer_decisions)
        for case in selected
    ]

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
