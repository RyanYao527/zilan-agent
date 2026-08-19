from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from zilanlib.reasoning.answer_review import build_reasoning_answer_review
from zilanlib.semantic.retrieval_dry_run import DEFAULT_FIXTURE

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "reasoning_answer_review.py"


def test_reasoning_answer_review_passes_agama_boundary_sample() -> None:
    result = build_reasoning_answer_review(
        DEFAULT_FIXTURE,
        query_id="SRQ-04",
        sample_id="srq04-agama-citation-boundary-pass",
    )

    assert result["mode"] == "reasoning-answer-review-v0"
    assert result["output_schema"] == "reasoning-answer-review-output-v0"
    assert result["query_id"] == "SRQ-04"
    assert result["overall_status"] == "pass"
    assert result["answer_review_status"] == "pass"
    assert result["answer_source"]["type"] == "sample"
    assert result["answer_source"]["sample_id"] == "srq04-agama-citation-boundary-pass"
    assert result["role_coverage_summary"]["status"] == "complete"
    assert result["role_coverage_summary"]["missing_needs"] == []
    assert result["contract_summary"]["status"] == "pass"
    assert result["contract_summary"]["missing_required_terms"] == []
    assert result["contract_summary"]["present_forbidden_terms"] == []
    assert result["contract_summary"]["missing_required_slots"] == []
    assert result["validator_summaries"][-1]["family"] == "agama_evidence"
    assert result["validator_summaries"][-1]["status"] == "run"
    assert result["validator_summaries"][-1]["case_ids"] == ["ZR-05"]
    assert "Answer review: pass" in result["review_text"]


def test_reasoning_answer_review_summarizes_failed_answer_contract_sample() -> None:
    result = build_reasoning_answer_review(
        DEFAULT_FIXTURE,
        query_id="SRQ-04",
        sample_id="srq04-agama-citation-boundary-fail",
    )

    assert result["overall_status"] == "fail"
    assert result["answer_review_status"] == "fail"
    assert result["contract_summary"]["status"] == "fail"
    assert "agama_citation_boundary:CBETA" in result["contract_summary"]["missing_required_terms"]
    assert result["contract_summary"]["missing_required_slots"]
    assert "Answer review: fail" in result["review_text"]


def test_reasoning_answer_review_summarizes_missing_required_term_groups() -> None:
    result = build_reasoning_answer_review(
        DEFAULT_FIXTURE,
        query_id="SRQ-06",
        sample_id="srq06-hetuvidya-indeterminate-fail",
    )

    assert result["overall_status"] == "fail"
    assert (
        "hetuvidya_indeterminate_detection:indeterminate_resolution"
        in result["contract_summary"]["missing_required_term_groups"]
    )
    assert "Required term groups:" in result["review_text"]


def test_reasoning_answer_review_marks_missing_answer_as_review_needed() -> None:
    result = build_reasoning_answer_review(DEFAULT_FIXTURE, query_id="SRQ-05")

    assert result["overall_status"] == "review_needed"
    assert result["answer_review_status"] == "review_needed"
    assert result["answer_source"] is None
    assert result["contract_summary"]["status"] == "review_needed"
    assert result["validator_summaries"][0]["family"] == "hetuvidya"
    assert result["validator_summaries"][0]["case_ids"] == ["ZR-07"]
    assert "Answer source: none" in result["review_text"]


def test_reasoning_answer_review_exposes_answer_validator_alignment_failure(tmp_path: Path) -> None:
    fixture_path = tmp_path / "semantic_chunks.yaml"
    fixture_text = DEFAULT_FIXTURE.read_text(encoding="utf-8").replace(
        "      - reasoning:ZR-07:hetuvidya-non-pervasive\n",
        "",
    )
    fixture_path.write_text(fixture_text, encoding="utf-8")

    result = build_reasoning_answer_review(
        fixture_path,
        query_id="SRQ-05",
        sample_id="srq05-hetuvidya-non-pervasive-pass",
    )

    assert result["overall_status"] == "fail"
    assert result["answer_review_status"] == "pass"
    assert result["contract_summary"]["status"] == "pass"
    assert result["answer_validator_alignment_summary"]["status"] == "fail"
    assert result["answer_validator_alignment_summary"]["missing_validator_cases"] == [
        {
            "role": "hetuvidya",
            "validator": "hetuvidya_validator",
            "validator_status": "not_applicable",
            "case_ids": [],
            "reason": "answer_contract_passed_without_structured_validator_case",
        }
    ]
    assert "Answer-validator alignment: fail" in result["review_text"]
    assert "hetuvidya: hetuvidya_validator (not_applicable; cases=none)" in result["review_text"]


def test_reasoning_answer_review_cli_json_output_is_machine_readable() -> None:
    completed = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--query-id",
            "SRQ-04",
            "--sample-id",
            "srq04-agama-citation-boundary-pass",
            "--json",
        ],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=True,
    )
    data = json.loads(completed.stdout)

    assert data["mode"] == "reasoning-answer-review-v0"
    assert data["query_id"] == "SRQ-04"
    assert data["overall_status"] == "pass"
    assert data["validator_summaries"][-1]["case_ids"] == ["ZR-05"]
