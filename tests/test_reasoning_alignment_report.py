from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import yaml
from zilanlib.reasoning.alignment_report import (
    ALIGNMENT_SECTION_IDS,
    ALL_OUTPUT_SCHEMA,
    OUTPUT_SCHEMA,
    build_all_reasoning_alignment_report,
    build_reasoning_alignment_report,
    render_markdown_report,
)
from zilanlib.semantic.retrieval_dry_run import DEFAULT_FIXTURE

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "reasoning_alignment_report.py"


def test_reasoning_alignment_report_maps_srq01_zr06_cross_system_sections() -> None:
    report = build_reasoning_alignment_report(query_id="SRQ-01")

    assert report["output_schema"] == OUTPUT_SCHEMA
    assert report["query_id"] == "SRQ-01"
    assert report["focus_reasoning_case_id"] == "ZR-06"
    assert report["summary"]["missing_sections"] == []
    assert list(report["alignment"]) == list(ALIGNMENT_SECTION_IDS)

    alignment = report["alignment"]
    assert alignment["claim"]["status"] == "present"
    assert alignment["agama_evidence"]["status"] == "present"
    assert alignment["agama_evidence"]["validator_status"] == "run"
    assert "ZR-06" in alignment["agama_evidence"]["case_ids"]
    assert alignment["hetuvidya_check"]["status"] == "present"
    assert "ZR-06" in alignment["hetuvidya_check"]["case_ids"]
    assert alignment["collected_topics_boundary"]["status"] == "present"
    assert alignment["madhyamaka_boundary"]["status"] == "present"
    assert alignment["cognitive_mapping"]["status"] == "present"
    assert alignment["practice_boundary"]["status"] == "present"


def test_reasoning_alignment_report_does_not_substitute_one_system_for_another(tmp_path: Path) -> None:
    fixture = yaml.safe_load(DEFAULT_FIXTURE.read_text(encoding="utf-8"))
    for query in fixture["queries"]:
        if query.get("id") == "SRQ-01":
            query["expected_chunk_ids"] = [
                chunk_id
                for chunk_id in query["expected_chunk_ids"]
                if chunk_id != "context:madhyamaka:prasanga-method"
            ]
            break
    for chunk in fixture["chunks"]:
        if chunk.get("chunk_id") == "reasoning:ZR-06:cross-domain-no-self":
            roles = chunk["metadata"]["reasoning_roles"]
            chunk["metadata"]["reasoning_roles"] = [
                role for role in roles if role != "madhyamaka_prasanga"
            ]
            break
    fixture_path = tmp_path / "semantic_chunks_without_madhyamaka.yaml"
    fixture_path.write_text(yaml.safe_dump(fixture, allow_unicode=True, sort_keys=False), encoding="utf-8")

    report = build_reasoning_alignment_report(fixture_path=fixture_path, query_id="SRQ-01")
    alignment = report["alignment"]

    assert alignment["hetuvidya_check"]["status"] == "present"
    assert alignment["agama_evidence"]["status"] == "present"
    assert alignment["madhyamaka_boundary"]["status"] == "missing"
    assert alignment["madhyamaka_boundary"]["reason"] == "role_coverage_missing"
    assert report["summary"]["missing_sections"] == ["madhyamaka_boundary"]


def test_reasoning_alignment_report_uses_answer_contract_practice_boundary_slots() -> None:
    srq09 = build_reasoning_alignment_report(query_id="SRQ-09")
    srq10 = build_reasoning_alignment_report(query_id="SRQ-10")

    assert srq09["alignment"]["cognitive_mapping"]["status"] == "present"
    assert srq09["alignment"]["practice_boundary"]["status"] == "present"
    assert srq09["alignment"]["practice_boundary"]["reason"] == "answer_contract_practice_boundary_slot_present"
    assert srq10["alignment"]["cognitive_mapping"]["status"] == "present"
    assert srq10["alignment"]["practice_boundary"]["status"] == "present"
    assert srq10["alignment"]["practice_boundary"]["reason"] == "answer_contract_practice_boundary_slot_present"


def test_reasoning_alignment_report_does_not_substitute_cognitive_mapping_for_practice_boundary(
    tmp_path: Path,
) -> None:
    fixture = yaml.safe_load(DEFAULT_FIXTURE.read_text(encoding="utf-8"))
    for query in fixture["queries"]:
        if query.get("id") != "SRQ-10":
            continue
        for contract in query["answer_contracts"].values():
            contract["required_slots"] = [
                slot
                for slot in contract["required_slots"]
                if slot.get("label") != "practice_boundary"
            ]
        break
    fixture_path = tmp_path / "semantic_chunks_without_practice_boundary_slot.yaml"
    fixture_path.write_text(yaml.safe_dump(fixture, allow_unicode=True, sort_keys=False), encoding="utf-8")

    report = build_reasoning_alignment_report(fixture_path=fixture_path, query_id="SRQ-10")
    alignment = report["alignment"]

    assert alignment["cognitive_mapping"]["status"] == "present"
    assert alignment["practice_boundary"]["status"] == "missing"
    assert alignment["practice_boundary"]["reason"] == "non_chunk_boundary_contract_missing"
    assert report["summary"]["missing_sections"] == ["practice_boundary"]


def test_reasoning_alignment_all_report_summarizes_all_srq_cases() -> None:
    report = build_all_reasoning_alignment_report()

    assert report["output_schema"] == ALL_OUTPUT_SCHEMA
    assert report["summary"]["case_count"] == 11
    assert report["summary"]["status_counts"] == {
        "manual_review_required": 1,
        "ready": 10,
    }
    assert report["summary"]["cases_with_manual_review_required"] == ["SRQ-04"]
    assert report["summary"]["cases_with_missing_sections"] == []

    srq01 = next(case for case in report["cases"] if case["query_id"] == "SRQ-01")
    assert srq01["focus_reasoning_case_id"] == "ZR-06"
    assert srq01["summary"]["missing_sections"] == []

    srq04 = next(case for case in report["cases"] if case["query_id"] == "SRQ-04")
    assert srq04["coverage_status"] == "manual_review_required"

    srq09 = next(case for case in report["cases"] if case["query_id"] == "SRQ-09")
    srq10 = next(case for case in report["cases"] if case["query_id"] == "SRQ-10")
    assert srq09["alignment"]["practice_boundary"]["status"] == "present"
    assert srq10["alignment"]["practice_boundary"]["status"] == "present"


def test_reasoning_alignment_all_markdown_highlights_exemplar_and_manual_boundary() -> None:
    report = build_all_reasoning_alignment_report()
    markdown = render_markdown_report(report)

    assert "# Reasoning Alignment Report" in markdown
    assert "All SRQ summary" in markdown
    assert "SRQ-01 / ZR-06" in markdown
    assert "SRQ-04" in markdown
    assert "manual_review_required" in markdown
    assert "one present section cannot substitute for another missing section" in markdown


def test_reasoning_alignment_markdown_contains_boundaries_and_limitations() -> None:
    report = build_reasoning_alignment_report(query_id="SRQ-01")
    markdown = render_markdown_report(report)

    assert "# Reasoning Alignment Report" in markdown
    assert "| madhyamaka_boundary | `present`" in markdown
    assert "This report does not grade answer quality" in markdown
    assert "This report does not change platform validation status" in markdown


def test_reasoning_alignment_report_cli_outputs_json() -> None:
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--query-id", "SRQ-01", "--json"],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=True,
    )
    payload = json.loads(result.stdout)

    assert payload["output_schema"] == OUTPUT_SCHEMA
    assert payload["query_id"] == "SRQ-01"
    assert payload["alignment"]["practice_boundary"]["status"] == "present"


def test_reasoning_alignment_report_cli_all_outputs_json() -> None:
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--all", "--json"],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=True,
    )
    payload = json.loads(result.stdout)

    assert payload["output_schema"] == ALL_OUTPUT_SCHEMA
    assert payload["summary"]["case_count"] == 11
    assert payload["summary"]["cases_with_manual_review_required"] == ["SRQ-04"]
