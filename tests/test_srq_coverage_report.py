from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from zilanlib.reasoning.srq_coverage_report import (
    REPORT_VERSION,
    _decision_gate,
    build_srq_coverage_report,
    render_markdown_report,
)

ROOT = Path(__file__).resolve().parents[1]


def _case_by_id(report: dict[str, object], query_id: str) -> dict[str, object]:
    cases = report["cases"]
    assert isinstance(cases, list)
    for case in cases:
        assert isinstance(case, dict)
        if case.get("query_id") == query_id:
            return case
    raise AssertionError(f"missing case: {query_id}")


def test_srq_coverage_report_includes_key_srq_cases_and_chunk_presence() -> None:
    report = build_srq_coverage_report(ROOT)

    case_ids = [case["query_id"] for case in report["cases"]]

    assert "SRQ-01" in case_ids
    assert "SRQ-04" in case_ids
    srq04 = _case_by_id(report, "SRQ-04")
    expected_chunks = srq04["expected_chunks"]
    assert isinstance(expected_chunks, list)
    assert expected_chunks
    assert all(chunk["exists"] is True for chunk in expected_chunks)


def test_srq_coverage_report_counts_pass_fail_samples() -> None:
    report = build_srq_coverage_report(ROOT)

    srq01 = _case_by_id(report, "SRQ-01")
    sample_coverage = srq01["sample_coverage"]

    assert sample_coverage["pass_count"] >= 1
    assert sample_coverage["fail_count"] >= 1
    assert sample_coverage["has_pass_sample"] is True
    assert sample_coverage["has_fail_sample"] is True


def test_srq_coverage_report_exposes_structured_chunk_reasoning_metadata() -> None:
    report = build_srq_coverage_report(ROOT)

    srq04 = _case_by_id(report, "SRQ-04")
    expected_chunks = srq04["expected_chunks"]
    assert isinstance(expected_chunks, list)

    assert any(chunk["section_label"] for chunk in expected_chunks)
    assert any("agama_evidence" in chunk["reasoning_roles"] for chunk in expected_chunks)
    assert "ZR-05" in srq04["related_reasoning_case_ids"]


def test_srq_coverage_report_exposes_agama_citation_metadata_triage() -> None:
    report = build_srq_coverage_report(ROOT)

    srq04 = _case_by_id(report, "SRQ-04")
    citation_metadata = srq04["citation_metadata"]

    assert citation_metadata["status"] == "ready"
    assert citation_metadata["agama_chunk_count"] == 4
    assert citation_metadata["chunks_with_cbeta_id"] == 4
    assert citation_metadata["chunks_with_line_anchor"] == 4
    assert citation_metadata["chunks_with_line_text_hash"] == 4
    assert citation_metadata["chunks_with_section_label"] == 3
    assert citation_metadata["chunks_missing_section_label"] == []
    assert citation_metadata["chunks_with_section_label_source_unavailable"] == [
        "agama:T01n0001:juan-3:line-1829"
    ]
    assert citation_metadata["manual_collation_candidate_set_ids"] == [
        "long-agama-no-self-verse-and-aggregates",
        "no-self-five-aggregates-and-feeling",
        "za-agama-and-long-agama-no-self-verse",
    ]
    assert citation_metadata["manual_collation_statuses"] == ["manual_collation_reviewed"]
    assert citation_metadata["publication_ready_claims"] == 0
    assert citation_metadata["xml_anchor_status"] == "anchor_located"
    assert citation_metadata["chunks_with_xml_anchor"] == [
        "agama:T01n0001:juan-1:line-881",
        "agama:T01n0001:juan-3:line-1829",
        "agama:T01n0001:juan-10:line-3997",
        "agama:T02n0099:juan-1:line-147",
    ]
    assert citation_metadata["chunks_missing_xml_anchor"] == []
    assert citation_metadata["xml_anchor_probe_statuses"] == ["anchor_located_collation_pending"]
    assert citation_metadata["manual_collation_boundary_status"] == "theme_parallel_only"
    assert citation_metadata["reviewer_decision_status_counts"] == {
        "pending_reviewer_decision": 3,
    }
    assert citation_metadata["pending_reviewer_decisions"] == [
        "long-agama-no-self-verse-and-aggregates",
        "no-self-five-aggregates-and-feeling",
        "za-agama-and-long-agama-no-self-verse",
    ]
    assert citation_metadata["limited_theme_parallel_confirmed"] == []
    assert citation_metadata["stronger_claim_requires_separate_evidence"] == []
    assert citation_metadata["textual_equivalence_status"] == "textual_equivalence_unreviewed"
    assert citation_metadata["source_dependence_status"] == "source_dependence_unreviewed"
    assert citation_metadata["publication_ready_status"] == "publication_ready_unreviewed"


def test_srq_coverage_report_exposes_per_chunk_citation_anchor_details() -> None:
    report = build_srq_coverage_report(ROOT)

    srq04 = _case_by_id(report, "SRQ-04")
    citation_metadata = srq04["citation_metadata"]
    details = citation_metadata["citation_anchor_details"]

    assert citation_metadata["citation_anchor_detail_status_counts"] == {
        "anchor_located": 4,
    }
    assert len(details) == 4
    by_chunk = {detail["chunk_id"]: detail for detail in details}
    long_agama_unsectioned = by_chunk["agama:T01n0001:juan-3:line-1829"]

    assert long_agama_unsectioned == {
        "chunk_id": "agama:T01n0001:juan-3:line-1829",
        "cbeta_id": "T01n0001",
        "section_label": None,
        "section_label_status": "source_unavailable",
        "xml_anchor_status": "anchor_located",
        "anchor_probe_id": "cbeta-anchor:T01n0001:line-1829",
        "manual_boundary_status": "theme_parallel_only",
        "candidate_set_ids": [
            "long-agama-no-self-verse-and-aggregates",
        ],
    }
    assert by_chunk["agama:T02n0099:juan-1:line-147"]["candidate_set_ids"] == [
        "no-self-five-aggregates-and-feeling",
        "za-agama-and-long-agama-no-self-verse",
    ]


def test_srq_coverage_report_marks_referenced_missing_anchor_probe(tmp_path: Path) -> None:
    collation_fixture = tmp_path / "high_value_no_self_parallel_candidates.yaml"
    collation_fixture.write_text(
        """
version: 1
candidate_sets:
  - set_id: broken-anchor-fixture
    status: manual_collation_reviewed
    source_chunk_id: agama:T02n0099:juan-1:line-147
    source_anchor_probe: cbeta-anchor:missing
    candidate_parallels: []
""",
        encoding="utf-8",
    )

    report = build_srq_coverage_report(ROOT, collation_candidates_path=collation_fixture)

    srq04 = _case_by_id(report, "SRQ-04")
    details = srq04["citation_metadata"]["citation_anchor_details"]
    by_chunk = {detail["chunk_id"]: detail for detail in details}

    assert srq04["citation_metadata"]["citation_anchor_detail_status_counts"] == {
        "anchor_probe_missing": 1,
        "not_applicable": 3,
    }
    assert by_chunk["agama:T02n0099:juan-1:line-147"]["xml_anchor_status"] == "anchor_probe_missing"
    assert by_chunk["agama:T02n0099:juan-1:line-147"]["anchor_probe_id"] == "cbeta-anchor:missing"
    assert by_chunk["agama:T02n0099:juan-1:line-147"]["candidate_set_ids"] == ["broken-anchor-fixture"]


def test_srq_coverage_report_does_not_treat_anchor_location_as_completed_collation() -> None:
    report = build_srq_coverage_report(ROOT)

    srq04 = _case_by_id(report, "SRQ-04")
    citation_metadata = srq04["citation_metadata"]

    assert srq04["coverage_status"] == "manual_review_required"
    assert citation_metadata["xml_anchor_status"] == "anchor_located"
    assert citation_metadata["manual_collation_boundary_status"] == "theme_parallel_only"
    assert citation_metadata["textual_equivalence_status"] == "textual_equivalence_unreviewed"
    assert citation_metadata["source_dependence_status"] == "source_dependence_unreviewed"
    assert citation_metadata["publication_ready_claims"] == 0
    assert citation_metadata["publication_ready_status"] == "publication_ready_unreviewed"


def test_srq_coverage_report_json_shape_and_manifest_runtime_evidence() -> None:
    report = build_srq_coverage_report(ROOT)

    assert report["version"] == REPORT_VERSION
    assert set(report) == {
        "version",
        "source",
        "runtime_evidence_source",
        "summary",
        "triage_matrix",
        "decision_gate",
        "cases",
        "limitations",
    }
    assert report["runtime_evidence_source"] == "manifest"
    assert report["source"]["output_schema"] == "srq-coverage-report-v3"

    srq04 = _case_by_id(report, "SRQ-04")
    runtime_evidence = srq04["runtime_evidence"]
    assert runtime_evidence["source"] == "manifest"
    assert "pass" in runtime_evidence["statuses"]


def test_srq_coverage_report_exposes_citation_reasoning_triage_matrix() -> None:
    report = build_srq_coverage_report(ROOT)
    matrix = report["triage_matrix"]

    assert matrix["case_count"] == 11
    assert matrix["coverage_status_counts"] == {
        "manual_review_required": 1,
        "ready": 10,
    }
    rows = {row["query_id"]: row for row in matrix["rows"]}

    srq01 = rows["SRQ-01"]
    assert set(srq01) == {
        "query_id",
        "coverage_status",
        "citation_readiness",
        "runtime_latest_status",
        "runtime_evidence_classes",
        "reasoning_family_coverage",
        "manual_review_boundary",
        "recommended_next_action",
    }
    assert set(srq01["reasoning_family_coverage"]) == {
        "related_reasoning_case_ids",
        "reasoning_roles",
    }
    assert srq01["coverage_status"] == "ready"
    assert srq01["citation_readiness"] == "ready"
    assert "ZR-06" in srq01["reasoning_family_coverage"]["related_reasoning_case_ids"]
    assert "agama_evidence" in srq01["reasoning_family_coverage"]["reasoning_roles"]
    assert srq01["manual_review_boundary"]["status"] == "theme_parallel_only"
    assert srq01["recommended_next_action"] == "manual_collation_review_before_publication_claims"

    srq04 = rows["SRQ-04"]
    assert srq04["coverage_status"] == "manual_review_required"
    assert srq04["citation_readiness"] == "ready"
    assert srq04["runtime_latest_status"] == "manual_review_required"
    assert "manual_collation" in srq04["runtime_evidence_classes"]
    assert srq04["manual_review_boundary"]["status"] == "theme_parallel_only"
    assert srq04["manual_review_boundary"]["reviewer_decision_status_counts"] == {
        "pending_reviewer_decision": 3,
    }
    assert srq04["manual_review_boundary"]["pending_reviewer_decisions"] == [
        "long-agama-no-self-verse-and-aggregates",
        "no-self-five-aggregates-and-feeling",
        "za-agama-and-long-agama-no-self-verse",
    ]
    assert srq04["recommended_next_action"] == "manual_semantic_boundary_review"


def test_srq_coverage_report_exposes_next_work_decision_gate() -> None:
    report = build_srq_coverage_report(ROOT)
    gate = report["decision_gate"]

    assert set(gate) == {
        "runtime_rerun_candidate",
        "prompt_hardening_candidate",
        "fixture_refinement_candidate",
        "manual_review_candidate",
    }

    manual_review_ids = [item["query_id"] for item in gate["manual_review_candidate"]]
    runtime_ids = [item["query_id"] for item in gate["runtime_rerun_candidate"]]
    prompt_ids = [item["query_id"] for item in gate["prompt_hardening_candidate"]]
    fixture_ids = [item["query_id"] for item in gate["fixture_refinement_candidate"]]

    assert manual_review_ids == ["SRQ-04"]
    assert "SRQ-04" not in runtime_ids
    assert "SRQ-04" not in prompt_ids
    assert "SRQ-04" not in fixture_ids
    assert fixture_ids == []

    srq04 = gate["manual_review_candidate"][0]
    assert srq04 == {
        "query_id": "SRQ-04",
        "primary_reason": "manual_semantic_boundary_review",
        "coverage_status": "manual_review_required",
        "runtime_latest_status": "manual_review_required",
        "citation_readiness": "ready",
        "manual_boundary_status": "theme_parallel_only",
        "reasoning_roles": ["agama_evidence"],
        "details": [
            "coverage_status=manual_review_required",
            "runtime_latest_status=manual_review_required",
            "manual_boundary=theme_parallel_only",
            "pending_reviewer_decisions=3",
        ],
    }


def test_srq_coverage_decision_gate_routes_missing_and_partial_cases() -> None:
    cases = [
        {
            "query_id": "SRQ-99",
            "coverage_status": "missing",
            "runtime_evidence": {"latest_status": "pass"},
            "citation_metadata": {
                "status": "not_applicable",
                "manual_collation_boundary_status": "not_applicable",
            },
            "expected_chunks": [],
        },
        {
            "query_id": "SRQ-100",
            "coverage_status": "partial",
            "runtime_evidence": {"latest_status": "pass"},
            "citation_metadata": {
                "status": "ready",
                "manual_collation_boundary_status": "not_applicable",
            },
            "expected_chunks": [],
        },
    ]

    gate = _decision_gate(cases)

    fixture_items = {item["query_id"]: item for item in gate["fixture_refinement_candidate"]}
    assert set(fixture_items) == {"SRQ-99", "SRQ-100"}
    assert fixture_items["SRQ-99"]["primary_reason"] == "fixture_or_sample_refinement"
    assert fixture_items["SRQ-99"]["details"] == [
        "coverage_status=missing",
        "runtime_latest_status=pass",
    ]
    assert fixture_items["SRQ-100"]["primary_reason"] == "fixture_or_sample_refinement"
    assert fixture_items["SRQ-100"]["details"] == [
        "coverage_status=partial",
        "runtime_latest_status=pass",
    ]


def test_srq_coverage_decision_gate_does_not_treat_source_unavailable_as_fixture_gap() -> None:
    cases = [
        {
            "query_id": "SRQ-99",
            "coverage_status": "ready",
            "runtime_evidence": {"latest_status": "pass"},
            "citation_metadata": {
                "status": "ready",
                "chunks_with_section_label_source_unavailable": [
                    "agama:T01n0001:juan-3:line-1829",
                ],
                "chunks_missing_xml_anchor": [],
                "manual_collation_boundary_status": "theme_parallel_only",
            },
            "expected_chunks": [],
        }
    ]

    gate = _decision_gate(cases)

    assert gate["fixture_refinement_candidate"] == []
    assert gate["manual_review_candidate"] == []


def test_srq_coverage_decision_gate_routes_actionable_citation_gaps() -> None:
    cases = [
        {
            "query_id": "SRQ-99",
            "coverage_status": "ready",
            "runtime_evidence": {"latest_status": "pass"},
            "citation_metadata": {
                "status": "ready",
                "chunks_with_section_label_source_unavailable": [],
                "chunks_missing_xml_anchor": [
                    "agama:T01n0001:juan-3:line-1829",
                ],
                "manual_collation_boundary_status": "not_applicable",
            },
            "expected_chunks": [],
        },
        {
            "query_id": "SRQ-100",
            "coverage_status": "ready",
            "runtime_evidence": {"latest_status": "pass"},
            "citation_metadata": {
                "status": "partial",
                "chunks_with_section_label_source_unavailable": [],
                "chunks_missing_xml_anchor": [],
                "manual_collation_boundary_status": "not_applicable",
            },
            "expected_chunks": [],
        },
    ]

    gate = _decision_gate(cases)

    fixture_items = {item["query_id"]: item for item in gate["fixture_refinement_candidate"]}
    assert set(fixture_items) == {"SRQ-99", "SRQ-100"}
    assert fixture_items["SRQ-99"]["primary_reason"] == "citation_fixture_refinement"
    assert fixture_items["SRQ-99"]["details"] == [
        "citation_readiness=ready",
        "chunks_missing_xml_anchor=1",
    ]
    assert fixture_items["SRQ-100"]["primary_reason"] == "citation_fixture_refinement"
    assert fixture_items["SRQ-100"]["details"] == [
        "citation_readiness=partial",
    ]


def test_srq_coverage_report_groups_runtime_status_by_evidence_class() -> None:
    report = build_srq_coverage_report(ROOT)

    srq10 = _case_by_id(report, "SRQ-10")
    runtime_evidence = srq10["runtime_evidence"]
    assert srq10["coverage_status"] == "ready"
    assert runtime_evidence["status_by_evidence_class"]["standalone_answer_excerpt"] == ["pass"]
    assert "not_reviewed" in runtime_evidence["status_by_evidence_class"]["summary_only"]

    srq11 = _case_by_id(report, "SRQ-11")
    srq11_runtime = srq11["runtime_evidence"]
    assert srq11["coverage_status"] == "ready"
    assert srq11_runtime["latest_status"] == "pass"
    assert (
        srq11_runtime["latest_entry"]["entry_id"]
        == "2026-08-20-volcengine-srq11-definition-violation-alias-replay-note"
    )
    assert srq11_runtime["status_by_evidence_class"]["standalone_answer_excerpt"] == ["fail"]
    assert "fail" in srq11_runtime["status_by_evidence_class"]["batch_manifest"]
    assert "pass" in srq11_runtime["status_by_evidence_class"]["batch_manifest"]
    assert "runtime_pending" in srq11_runtime["status_by_evidence_class"]["summary_only"]
    assert "pass" in srq11_runtime["status_by_evidence_class"]["summary_only"]
    assert report["summary"]["coverage_status_counts"]["manual_review_required"] == 1

    srq04 = _case_by_id(report, "SRQ-04")
    srq04_runtime = srq04["runtime_evidence"]
    assert srq04_runtime["status_by_evidence_class"]["manual_collation"] == ["manual_review_required"]


def test_srq04_manual_collation_boundary_stays_manual_review_required_without_runtime_promotion() -> None:
    report = build_srq_coverage_report(ROOT)

    srq04 = _case_by_id(report, "SRQ-04")
    runtime_evidence = srq04["runtime_evidence"]
    latest_entry = runtime_evidence["latest_entry"]

    assert srq04["coverage_status"] == "manual_review_required"
    assert runtime_evidence["latest_status"] == "manual_review_required"
    assert latest_entry["entry_id"] == "2026-09-02-srq04-citation-anchor-section-refinement"
    assert latest_entry["evidence_class"] == "summary_only"
    assert latest_entry["answer_file_safe"] is False
    assert latest_entry["platform_status_change"] is False
    assert "Local citation-anchor refinement only" in latest_entry["notes"]
    assert "XML-P5 anchor" in latest_entry["notes"]
    assert "no stable source-derived section label is available" in latest_entry["notes"]
    assert "source dependence" in latest_entry["notes"]
    assert "platform status remain unchanged" in latest_entry["notes"]


def test_srq_coverage_report_preserves_hash_prefixed_manifest_note_text() -> None:
    report = build_srq_coverage_report(ROOT)

    srq10 = _case_by_id(report, "SRQ-10")
    latest_entry = srq10["runtime_evidence"]["latest_entry"]

    assert "#193 recorded the pre-calibration literal misses" in latest_entry["notes"]


def test_srq_coverage_report_falls_back_to_markdown_index_when_manifest_missing() -> None:
    report = build_srq_coverage_report(
        ROOT,
        manifest_path=ROOT / "docs" / "runtime-evidence" / "missing-evidence-manifest.yaml",
    )

    assert report["runtime_evidence_source"] == "markdown_index"
    srq04 = _case_by_id(report, "SRQ-04")
    assert srq04["runtime_evidence"]["source"] == "markdown_index"


def test_srq_coverage_markdown_contains_limitations_and_manual_review_language() -> None:
    report = build_srq_coverage_report(ROOT)
    markdown = render_markdown_report(report)

    assert "# SRQ/ZR Evidence Coverage Report" in markdown
    assert "## Limitations" in markdown
    assert "manual review required" in markdown
    assert "| SRQ-11 | `ready`" in markdown
    assert "standalone_answer_excerpt: fail" in markdown
    assert "summary_only: pass, fail, runtime_pending" in markdown
    assert "manual_collation: manual_review_required" in markdown
    assert "## Citation Metadata" in markdown
    assert "section_label source unavailable: agama:T01n0001:juan-3:line-1829" in markdown
    assert "XML anchors: anchor_located" in markdown
    assert "manual boundary: theme_parallel_only" in markdown
    assert "reviewer decisions: pending_reviewer_decision=3" in markdown
    assert "textual equivalence: textual_equivalence_unreviewed" in markdown
    assert "## Citation Anchor Details" in markdown
    assert (
        "| SRQ-04 | `agama:T01n0001:juan-3:line-1829` | `T01n0001` | "
        "`source_unavailable` | `anchor_located` | "
        "`cbeta-anchor:T01n0001:line-1829` | `theme_parallel_only` | "
        "long-agama-no-self-verse-and-aggregates |"
    ) in markdown
    assert "manual collation candidates: 3" in markdown
    assert "## Citation / Reasoning Triage Matrix" in markdown
    assert "## Citation / Reasoning Decision Gate" in markdown
    assert "| manual_review_candidate | SRQ-04 | manual_semantic_boundary_review |" in markdown
    assert "| fixture_refinement_candidate | - | - | - |" in markdown
    assert "manual_semantic_boundary_review" in markdown
    assert "theme_parallel_only" in markdown
    assert "ZR-06" in markdown
    assert "does not change platform validation status" in markdown


def test_srq_coverage_report_root_cli_outputs_json() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/srq_coverage_report.py", "--json"],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=True,
    )

    payload = json.loads(result.stdout)

    assert payload["version"] == REPORT_VERSION
    assert payload["runtime_evidence_source"] == "manifest"
    assert any(case["query_id"] == "SRQ-04" for case in payload["cases"])
