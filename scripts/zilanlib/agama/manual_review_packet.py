from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from zilanlib.yaml_io import display_path, load_yaml_mapping

ROOT = Path(__file__).resolve().parents[3]
DEFAULT_CANDIDATES = ROOT / "tests" / "fixtures" / "collation" / "high_value_no_self_parallel_candidates.yaml"
DEFAULT_DECISIONS = ROOT / "tests" / "fixtures" / "collation" / "srq04_manual_semantic_boundary_decisions.yaml"
DEFAULT_ANCHOR_PROBES = ROOT / "tests" / "fixtures" / "collation" / "cbeta_anchor_probes.yaml"
MODE = "srq04-manual-review-packet-v0"
OUTPUT_SCHEMA = "srq04-manual-review-packet-v1"
REPORT_TITLE = "SRQ-04 Manual Semantic-Boundary Review Packet"
REQUIRED_REVIEWER_FIELDS = (
    "theme_parallel",
    "textual_equivalence",
    "source_dependence",
    "publication_ready",
    "decision_notes",
)
DATED_EVIDENCE_NOTE_PATTERN = "docs/runtime-evidence/YYYY-MM-DD-*.md"
INGESTION_RULES = {
    "decision_fixture": "tests/fixtures/collation/srq04_manual_semantic_boundary_decisions.yaml",
    "dated_evidence_note_pattern": DATED_EVIDENCE_NOTE_PATTERN,
    "status_transitions": {
        "pending_reviewer_decision": {
            "field_values": "all reviewer boundary fields remain pending",
            "evidence_file": "not_allowed",
            "candidate_map_update": "blocked_until_dated_decision",
            "manifest_status": "manual_review_required",
        },
        "limited_theme_parallel_confirmed": {
            "field_values": "theme_parallel=limited; stronger boundary fields=not_established",
            "evidence_file": "required_dated_note",
            "candidate_map_update": "not_required_for_stronger_claims",
            "manifest_status": "manual_review_required",
        },
        "stronger_claim_requires_separate_evidence": {
            "field_values": "at least one stronger boundary field=supported_with_evidence",
            "evidence_file": "required_dated_note",
            "candidate_map_update": "matching_candidate_set_only",
            "manifest_status": "manual_review_required_until_scoped_evidence_pr",
        },
    },
}
LIMITATIONS = (
    "anchor located does not prove textual equivalence",
    "limited theme-parallel does not prove source dependence",
    "this packet is not publication-ready collation",
    "this packet is not runtime evidence and does not change platform validation status",
)


class Srq04ManualReviewPacketError(ValueError):
    """Raised when the local SRQ-04 manual review packet cannot be built."""


def _display(path: Path) -> str:
    return display_path(path, root=ROOT)


def _load_yaml(path: Path) -> dict[str, Any]:
    return load_yaml_mapping(
        path,
        root=ROOT,
        error_type=Srq04ManualReviewPacketError,
        missing_message="PyYAML is required to build the SRQ-04 manual review packet.",
        missing_file_label="Manual review packet fixture not found",
        parse_label="Failed to parse manual review packet fixture",
        mapping_label="Manual review packet fixture must be a mapping",
    )


def _mapping_list(data: dict[str, Any], field: str, *, source: Path) -> list[dict[str, Any]]:
    values = data.get(field)
    if not isinstance(values, list):
        raise Srq04ManualReviewPacketError(f"{_display(source)} {field} must be a list.")
    return [value for value in values if isinstance(value, dict)]


def _anchor_probes_by_id(path: Path) -> dict[str, dict[str, Any]]:
    probes: dict[str, dict[str, Any]] = {}
    for probe in _mapping_list(_load_yaml(path), "anchor_probes", source=path):
        probe_id = probe.get("probe_id")
        if isinstance(probe_id, str) and probe_id:
            probes[probe_id] = probe
    return probes


def _decisions_by_candidate_set(path: Path) -> dict[str, dict[str, Any]]:
    decisions: dict[str, dict[str, Any]] = {}
    for decision in _mapping_list(_load_yaml(path), "decisions", source=path):
        candidate_set_id = decision.get("candidate_set_id")
        if isinstance(candidate_set_id, str) and candidate_set_id:
            decisions[candidate_set_id] = decision
    return decisions


def _candidate_anchor_probe_ids(candidate_set: dict[str, Any]) -> list[str]:
    probe_ids: set[str] = set()
    source_anchor_probe = candidate_set.get("source_anchor_probe")
    if isinstance(source_anchor_probe, str) and source_anchor_probe:
        probe_ids.add(source_anchor_probe)
    for parallel in candidate_set.get("candidate_parallels", []):
        if not isinstance(parallel, dict):
            continue
        anchor_probe = parallel.get("anchor_probe")
        if isinstance(anchor_probe, str) and anchor_probe:
            probe_ids.add(anchor_probe)
    return sorted(probe_ids)


def _parallel_values(candidate_set: dict[str, Any], field: str) -> list[str]:
    values: set[str] = set()
    for parallel in candidate_set.get("candidate_parallels", []):
        if not isinstance(parallel, dict):
            continue
        value = parallel.get(field)
        if isinstance(value, str) and value:
            values.add(value)
    return sorted(values)


def _claim_count(candidate_set: dict[str, Any], field: str) -> int:
    return sum(
        1
        for parallel in candidate_set.get("candidate_parallels", [])
        if isinstance(parallel, dict) and parallel.get(field) is True
    )


def _boundary_claims(candidate_set: dict[str, Any], anchor_probes: dict[str, dict[str, Any]]) -> dict[str, Any]:
    probe_ids = _candidate_anchor_probe_ids(candidate_set)
    missing_probes = [probe_id for probe_id in probe_ids if probe_id not in anchor_probes]
    textual_equivalence_claim = _claim_count(candidate_set, "equivalence_claim") > 0
    source_dependence_claim = _claim_count(candidate_set, "source_dependence_claim") > 0
    publication_ready = _claim_count(candidate_set, "publication_ready") > 0
    limited_theme_parallel = (
        "manual_xml_p5_theme_parallel_reviewed" in _parallel_values(candidate_set, "collation_status")
        and not textual_equivalence_claim
        and not source_dependence_claim
        and not publication_ready
    )
    return {
        "anchor_located": bool(probe_ids) and not missing_probes,
        "limited_theme_parallel": limited_theme_parallel,
        "textual_equivalence_claim": textual_equivalence_claim,
        "source_dependence_claim": source_dependence_claim,
        "publication_ready": publication_ready,
        "anchor_probe_ids": probe_ids,
        "missing_anchor_probe_ids": missing_probes,
    }


def _parallel_summary(candidate_set: dict[str, Any]) -> list[dict[str, Any]]:
    summaries: list[dict[str, Any]] = []
    for parallel in candidate_set.get("candidate_parallels", []):
        if not isinstance(parallel, dict):
            continue
        summaries.append(
            {
                "anchor_probe": parallel.get("anchor_probe"),
                "chunk_id": parallel.get("chunk_id"),
                "relation": parallel.get("relation"),
                "confidence": parallel.get("confidence"),
                "collation_status": parallel.get("collation_status"),
                "qualified_conclusion": parallel.get("qualified_conclusion"),
            }
        )
    return summaries


def _decision_ingestion(decision: dict[str, Any]) -> dict[str, Any]:
    status = decision.get("status")
    if status == "limited_theme_parallel_confirmed":
        return {
            "next_action": "record_dated_limited_theme_parallel_decision",
            "requires_dated_evidence_note": True,
            "candidate_map_update_allowed": False,
            "candidate_map_update_scope": "none_for_stronger_claims",
            "manifest_status": "manual_review_required",
        }
    if status == "stronger_claim_requires_separate_evidence":
        return {
            "next_action": "open_scoped_candidate_map_evidence_pr",
            "requires_dated_evidence_note": True,
            "candidate_map_update_allowed": True,
            "candidate_map_update_scope": "matching_candidate_set_only",
            "manifest_status": "manual_review_required_until_scoped_evidence_pr",
        }
    return {
        "next_action": "await_dated_human_reviewer_decision",
        "requires_dated_evidence_note": False,
        "candidate_map_update_allowed": False,
        "candidate_map_update_scope": "none",
        "manifest_status": "manual_review_required",
    }


def _candidate_packet(
    candidate_set: dict[str, Any],
    *,
    decisions_by_id: dict[str, dict[str, Any]],
    anchor_probes: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    set_id = str(candidate_set.get("set_id", ""))
    decision = decisions_by_id.get(
        set_id,
        {
            "candidate_set_id": set_id,
            "status": "missing_reviewer_decision",
            "decision_notes": "No reviewer-decision intake row is recorded for this candidate set.",
        },
    )
    boundary_claims = _boundary_claims(candidate_set, anchor_probes)
    manual_review = candidate_set.get("manual_review")
    return {
        "set_id": set_id,
        "theme": candidate_set.get("theme"),
        "candidate_status": candidate_set.get("status"),
        "source_anchor_probe": candidate_set.get("source_anchor_probe"),
        "source_chunk_id": candidate_set.get("source_chunk_id"),
        "manual_review": manual_review if isinstance(manual_review, dict) else {},
        "candidate_parallels": _parallel_summary(candidate_set),
        "decision": decision,
        "ingestion": _decision_ingestion(decision),
        "reviewer_required_fields": list(REQUIRED_REVIEWER_FIELDS),
        "boundary_claims": boundary_claims,
        "reviewer_questions": {
            "theme_parallel": "Is the relation only a limited doctrinal theme parallel?",
            "textual_equivalence": "Can the reviewer establish textual equivalence from the cited spans?",
            "source_dependence": "Can the reviewer establish source dependence from the cited spans?",
            "publication_ready": "Is this evidence publication-ready collation?",
            "decision_notes": "Record dated reasoning and remaining limits.",
        },
    }


def _summary(candidate_sets: list[dict[str, Any]]) -> dict[str, Any]:
    decision_counts = Counter(
        str(candidate["decision"]["status"])
        for candidate in candidate_sets
        if isinstance(candidate.get("decision"), dict)
        and isinstance(candidate["decision"].get("status"), str)
    )
    return {
        "candidate_set_count": len(candidate_sets),
        "reviewer_decision_status_counts": dict(sorted(decision_counts.items())),
        "pending_reviewer_decisions": sorted(
            str(candidate["set_id"])
            for candidate in candidate_sets
            if candidate.get("decision", {}).get("status") == "pending_reviewer_decision"
        ),
        "textual_equivalence_claims": sum(
            1 for candidate in candidate_sets if candidate["boundary_claims"]["textual_equivalence_claim"]
        ),
        "source_dependence_claims": sum(
            1 for candidate in candidate_sets if candidate["boundary_claims"]["source_dependence_claim"]
        ),
        "publication_ready_claims": sum(
            1 for candidate in candidate_sets if candidate["boundary_claims"]["publication_ready"]
        ),
    }


def build_srq04_manual_review_packet(
    *,
    candidates_path: Path = DEFAULT_CANDIDATES,
    decisions_path: Path = DEFAULT_DECISIONS,
    anchor_probes_path: Path = DEFAULT_ANCHOR_PROBES,
) -> dict[str, Any]:
    """Build a local SRQ-04 packet for human semantic-boundary review."""

    candidate_data = _load_yaml(candidates_path)
    candidate_sets = sorted(
        _mapping_list(candidate_data, "candidate_sets", source=candidates_path),
        key=lambda candidate: str(candidate.get("set_id", "")),
    )
    decisions_by_id = _decisions_by_candidate_set(decisions_path)
    anchor_probes = _anchor_probes_by_id(anchor_probes_path)
    packets = [
        _candidate_packet(candidate, decisions_by_id=decisions_by_id, anchor_probes=anchor_probes)
        for candidate in candidate_sets
    ]
    return {
        "mode": MODE,
        "output_schema": OUTPUT_SCHEMA,
        "query_id": "SRQ-04",
        "source": {
            "candidates": _display(candidates_path),
            "reviewer_decisions": _display(decisions_path),
            "xml_anchor_probes": _display(anchor_probes_path),
        },
        "reviewer_required_fields": list(REQUIRED_REVIEWER_FIELDS),
        "ingestion_rules": INGESTION_RULES,
        "summary": _summary(packets),
        "candidate_sets": packets,
        "limitations": list(LIMITATIONS),
    }


def render_markdown_packet(packet: dict[str, Any]) -> str:
    lines = [
        f"# {REPORT_TITLE}",
        "",
        "This local packet prepares existing SRQ-04 XML-P5 candidate evidence for human review.",
        "It does not make a new scholarly or runtime claim.",
        "",
        "## Summary",
        "",
        f"- Candidate sets: `{packet['summary']['candidate_set_count']}`",
        f"- Reviewer decision status counts: `{packet['summary']['reviewer_decision_status_counts']}`",
        f"- Pending reviewer decisions: `{packet['summary']['pending_reviewer_decisions']}`",
        "",
        "## Reviewer Fields",
        "",
    ]
    lines.extend(f"- `{field}`" for field in packet["reviewer_required_fields"])
    lines.extend(
        [
            "",
            "## Ingestion Rules",
            "",
            f"- Decision fixture: `{packet['ingestion_rules']['decision_fixture']}`",
            f"- Dated evidence note pattern: `{packet['ingestion_rules']['dated_evidence_note_pattern']}`",
            "- Pending rows block candidate map update until a dated human decision is recorded.",
            "- Stronger claims require a scoped evidence PR and candidate map update "
            "for the matching candidate set only.",
        ]
    )
    lines.extend(
        [
            "",
            "## Candidate Sets",
            "",
            "| Candidate set | Decision | Source chunk | Anchor probes | Current boundary |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for candidate in packet["candidate_sets"]:
        boundary = candidate["boundary_claims"]
        current_boundary = (
            "anchor_located={anchor}; limited_theme_parallel={theme}; "
            "textual_equivalence={equivalence}; source_dependence={source}; publication_ready={publication}"
        ).format(
            anchor=boundary["anchor_located"],
            theme=boundary["limited_theme_parallel"],
            equivalence=boundary["textual_equivalence_claim"],
            source=boundary["source_dependence_claim"],
            publication=boundary["publication_ready"],
        )
        lines.append(
            "| {set_id} | `{status}` | {chunk} | {probes} | {boundary} |".format(
                set_id=candidate["set_id"],
                status=candidate["decision"]["status"],
                chunk=candidate["source_chunk_id"],
                probes=", ".join(candidate["boundary_claims"]["anchor_probe_ids"]) or "-",
                boundary=current_boundary,
            )
        )
    lines.extend(["", "## Limitations", ""])
    lines.extend(f"- {limitation}" for limitation in packet["limitations"])
    lines.append("")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description="Build a local SRQ-04 manual semantic-boundary review packet.")
    parser.add_argument("--json", action="store_true", dest="json_output", help="Emit machine-readable JSON.")
    args = parser.parse_args(argv)

    packet = build_srq04_manual_review_packet()
    if args.json_output:
        print(json.dumps(packet, ensure_ascii=False, indent=2))
    else:
        print(render_markdown_packet(packet), end="")
    return 0
