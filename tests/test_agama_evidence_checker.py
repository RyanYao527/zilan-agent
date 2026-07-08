import json
import subprocess
import sys
from pathlib import Path

from agama_evidence_checker import (
    DEFAULT_CASES,
    AgamaEvidenceCheckerError,
    build_agama_evidence_check,
)

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "agama_evidence_checker.py"


def test_agama_evidence_checker_maps_zr05_citation_boundary() -> None:
    result = build_agama_evidence_check(DEFAULT_CASES, case_id="ZR-05")
    review = result["evidence_reviews"][0]
    evidence = review["agama_evidence"]

    assert result["status"] == "run"
    assert result["validator"] == "agama_evidence_checker"
    assert result["contract_family"] == "agama_evidence"
    assert result["mode"] == "agama-evidence-checker-v0.1"
    assert result["output_schema"] == "agama-evidence-checker-output-v0.1"
    assert result["source"] == "tests/reasoning_cases.yaml"
    assert result["case_ids"] == ["ZR-05"]
    assert result["count"] == 1
    assert review["case_id"] == "ZR-05"
    assert review["boundary_statement_required"] is True
    assert evidence["citation_required"] == {
        "required": True,
        "status": "required",
        "required_fields": ["sutra_name", "cbeta_id", "local_context_anchor"],
    }
    assert evidence["search_scope"] == {
        "scope": "representative_search",
        "status": "representative",
        "exhaustive": False,
    }
    assert evidence["collation_boundary"] == {
        "required": True,
        "status": "required",
    }
    assert evidence["reference_summary"]["has_agama_index"] is True
    assert evidence["reference_summary"]["has_search_helper"] is True
    assert "context/agama/T0099-za-agama.md" in evidence["reference_summary"]["agama_files"]

    local_evidence = evidence["local_evidence"]
    assert local_evidence["status"] == "pass"
    assert local_evidence["retrieval_fixture"] == "tests/fixtures/retrieval_chunks/semantic_chunks.yaml"
    assert local_evidence["index_check"]["status"] == "pass"
    assert local_evidence["failed_references"] == []
    assert local_evidence["failed_passage_anchors"] == []
    assert [item["chunk_id"] for item in local_evidence["passage_anchor_checks"]] == [
        "agama:T02n0099:juan-1:line-147",
        "agama:T01n0001:juan-1:line-881",
        "agama:T01n0001:juan-3:line-1829",
    ]
    assert {item["status"] for item in local_evidence["passage_anchor_checks"]} == {"pass"}
    assert {item["code"] for item in review["diagnostics"]} == {
        "citation_anchor_required",
        "representative_search_scope",
        "collation_boundary_required",
        "boundary_statement_required",
        "local_evidence_anchors_verified",
    }


def test_agama_evidence_checker_defaults_to_agama_cases() -> None:
    result = build_agama_evidence_check(DEFAULT_CASES)

    assert [item["case_id"] for item in result["evidence_reviews"]] == ["ZR-05", "ZR-06"]
    assert result["count"] == 2
    assert any("Local evidence checks" in item for item in result["limitations"])


def test_agama_evidence_checker_rejects_non_agama_case() -> None:
    try:
        build_agama_evidence_check(DEFAULT_CASES, case_id="ZR-03")
    except AgamaEvidenceCheckerError as exc:
        assert "ZR-03 is not an Agama evidence reasoning case" in str(exc)
    else:
        raise AssertionError("non-Agama evidence case should fail")


def test_agama_evidence_checker_cli_json_output_is_machine_readable() -> None:
    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--case-id",
            "ZR-05",
            "--json",
        ],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=True,
    )
    data = json.loads(result.stdout)

    assert data["mode"] == "agama-evidence-checker-v0.1"
    assert data["case_id"] == "ZR-05"
    evidence = data["evidence_reviews"][0]["agama_evidence"]
    assert evidence["citation_required"]["status"] == "required"
    assert evidence["local_evidence"]["status"] == "pass"
