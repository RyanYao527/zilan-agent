from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from zilanlib.reasoning.srq_coverage_report import (
    REPORT_VERSION,
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


def test_srq_coverage_report_json_shape_and_manifest_runtime_evidence() -> None:
    report = build_srq_coverage_report(ROOT)

    assert report["version"] == REPORT_VERSION
    assert set(report) == {
        "version",
        "source",
        "runtime_evidence_source",
        "summary",
        "cases",
        "limitations",
    }
    assert report["runtime_evidence_source"] == "manifest"

    srq04 = _case_by_id(report, "SRQ-04")
    runtime_evidence = srq04["runtime_evidence"]
    assert runtime_evidence["source"] == "manifest"
    assert "pass" in runtime_evidence["statuses"]


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
    assert latest_entry["entry_id"] == "2026-08-20-srq04-manual-semantic-boundary-queue"
    assert latest_entry["evidence_class"] == "summary_only"
    assert latest_entry["answer_file_safe"] is False
    assert latest_entry["platform_status_change"] is False
    assert "anchor-located and limited theme-parallel evidence remain insufficient" in latest_entry["notes"]
    assert "source dependence" in latest_entry["notes"]
    assert "runtime pass" in latest_entry["notes"]


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
