from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from zilanlib.agama.manual_review_packet import (
    OUTPUT_SCHEMA,
    REQUIRED_REVIEWER_FIELDS,
    build_srq04_manual_review_packet,
    render_markdown_packet,
)

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "srq04_manual_review_packet.py"


def test_srq04_manual_review_packet_lists_current_candidate_sets() -> None:
    packet = build_srq04_manual_review_packet()

    assert packet["output_schema"] == OUTPUT_SCHEMA
    assert packet["query_id"] == "SRQ-04"
    assert packet["summary"]["candidate_set_count"] == 3
    assert packet["summary"]["reviewer_decision_status_counts"] == {
        "pending_reviewer_decision": 3,
    }
    assert packet["reviewer_required_fields"] == list(REQUIRED_REVIEWER_FIELDS)

    candidate_ids = [candidate["set_id"] for candidate in packet["candidate_sets"]]
    assert candidate_ids == [
        "long-agama-no-self-verse-and-aggregates",
        "no-self-five-aggregates-and-feeling",
        "za-agama-and-long-agama-no-self-verse",
    ]


def test_srq04_manual_review_packet_exposes_decision_ingestion_rules() -> None:
    packet = build_srq04_manual_review_packet()

    ingestion_rules = packet["ingestion_rules"]
    assert ingestion_rules["decision_fixture"] == (
        "tests/fixtures/collation/srq04_manual_semantic_boundary_decisions.yaml"
    )
    assert ingestion_rules["dated_evidence_note_pattern"] == "docs/runtime-evidence/YYYY-MM-DD-*.md"
    assert ingestion_rules["status_transitions"]["pending_reviewer_decision"]["candidate_map_update"] == (
        "blocked_until_dated_decision"
    )
    assert ingestion_rules["status_transitions"]["limited_theme_parallel_confirmed"]["evidence_file"] == (
        "required_dated_note"
    )
    assert ingestion_rules["status_transitions"]["stronger_claim_requires_separate_evidence"][
        "candidate_map_update"
    ] == "matching_candidate_set_only"

    for candidate in packet["candidate_sets"]:
        ingestion = candidate["ingestion"]
        assert ingestion["next_action"] == "await_dated_human_reviewer_decision"
        assert ingestion["requires_dated_evidence_note"] is False
        assert ingestion["candidate_map_update_allowed"] is False
        assert ingestion["manifest_status"] == "manual_review_required"


def test_srq04_manual_review_packet_keeps_pending_decisions_conservative() -> None:
    packet = build_srq04_manual_review_packet()

    for candidate in packet["candidate_sets"]:
        assert candidate["decision"]["status"] == "pending_reviewer_decision"
        assert candidate["decision"]["theme_parallel"] == "pending"
        assert candidate["decision"]["textual_equivalence"] == "pending"
        assert candidate["decision"]["source_dependence"] == "pending"
        assert candidate["decision"]["publication_ready"] == "pending"
        boundary_claims = candidate["boundary_claims"]
        assert boundary_claims["anchor_located"] is True
        assert boundary_claims["limited_theme_parallel"] is True
        assert boundary_claims["textual_equivalence_claim"] is False
        assert boundary_claims["source_dependence_claim"] is False
        assert boundary_claims["publication_ready"] is False
        assert boundary_claims["anchor_probe_ids"]
        assert boundary_claims["missing_anchor_probe_ids"] == []


def test_srq04_manual_review_packet_markdown_is_human_review_ready() -> None:
    packet = build_srq04_manual_review_packet()
    markdown = render_markdown_packet(packet)

    assert "# SRQ-04 Manual Semantic-Boundary Review Packet" in markdown
    assert "theme_parallel" in markdown
    assert "textual_equivalence" in markdown
    assert "source_dependence" in markdown
    assert "publication_ready" in markdown
    assert "anchor located does not prove textual equivalence" in markdown
    assert "limited theme-parallel does not prove source dependence" in markdown
    assert "## Ingestion Rules" in markdown
    assert "docs/runtime-evidence/YYYY-MM-DD-*.md" in markdown
    assert "candidate map update" in markdown
    assert "not runtime evidence" in markdown
    assert "no-self-five-aggregates-and-feeling" in markdown


def test_srq04_manual_review_packet_root_cli_outputs_json() -> None:
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--json"],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=True,
    )
    payload = json.loads(result.stdout)

    assert payload["output_schema"] == OUTPUT_SCHEMA
    assert payload["summary"]["pending_reviewer_decisions"] == [
        "long-agama-no-self-verse-and-aggregates",
        "no-self-five-aggregates-and-feeling",
        "za-agama-and-long-agama-no-self-verse",
    ]
