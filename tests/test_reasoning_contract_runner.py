import json
import subprocess
import sys
from pathlib import Path

from reasoning_contract_runner import build_reasoning_contract_run
from semantic_retrieval_dry_run import DEFAULT_FIXTURE, FixtureError

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "reasoning_contract_runner.py"


def test_reasoning_contract_runner_passes_hetuvidya_sample() -> None:
    result = build_reasoning_contract_run(
        DEFAULT_FIXTURE,
        query_id="SRQ-05",
        sample_id="srq05-hetuvidya-non-pervasive-pass",
    )

    assert result["mode"] == "reasoning-contract-runner-v0"
    assert result["output_schema"] == "reasoning-contract-runner-output-v0"
    assert result["query_id"] == "SRQ-05"
    assert result["overall_status"] == "pass"
    assert result["retrieval"]["expected_chunk_ids"] == [
        "context:hetuvidya:trairupya",
        "reasoning:ZR-07:hetuvidya-non-pervasive",
    ]
    assert result["role_coverage"]["coverage_status"] == "complete"
    assert result["role_coverage"]["missing_needs"] == []
    assert result["answer_review_status"] == "pass"
    assert result["answer_contract_review"]["overall_status"] == "pass"

    validator = result["validators"]["hetuvidya"]
    assert validator["status"] == "run"
    assert validator["case_ids"] == ["ZR-07"]
    assert validator["validations"][0]["case_id"] == "ZR-07"
    assert validator["validations"][0]["judgment"]["status"] == "invalid"
    assert validator["validations"][0]["judgment"]["failed_checks"] == ["vipaksa_asattva"]


def test_reasoning_contract_runner_skips_hetuvidya_validator_for_madhyamaka_sample() -> None:
    result = build_reasoning_contract_run(
        DEFAULT_FIXTURE,
        query_id="SRQ-08",
        sample_id="srq08-madhyamaka-nihilism-boundary-pass",
    )

    assert result["overall_status"] == "pass"
    assert result["role_coverage"]["covered_needs"] == {
        "madhyamaka_prasanga": [
            "context:madhyamaka:prasanga-method",
            "reasoning:ZR-09:madhyamaka-nihilism-boundary",
        ],
    }
    assert result["answer_contract_review"]["overall_status"] == "pass"
    assert result["validators"]["hetuvidya"] == {
        "status": "not_applicable",
        "case_ids": [],
        "validations": [],
        "limitations": [
            "No selected reasoning case with hetuvidya role was found for this query fixture.",
        ],
    }


def test_reasoning_contract_runner_marks_answer_contracts_without_answer_as_review_needed() -> None:
    result = build_reasoning_contract_run(DEFAULT_FIXTURE, query_id="SRQ-05")

    assert result["overall_status"] == "review_needed"
    assert result["answer_review_status"] == "review_needed"
    assert result["answer_contract_review"] is None
    assert result["validators"]["hetuvidya"]["status"] == "run"


def test_reasoning_contract_runner_fails_when_role_coverage_is_incomplete() -> None:
    result = build_reasoning_contract_run(DEFAULT_FIXTURE, query_id="SRQ-01", limit=1)

    assert result["overall_status"] == "fail"
    assert result["answer_review_status"] == "no_answer_contracts"
    assert result["role_coverage"]["missing_needs"] == [
        "collected_topics",
        "hetuvidya",
        "madhyamaka_prasanga",
    ]
    assert result["validators"]["hetuvidya"]["status"] == "not_applicable"


def test_reasoning_contract_runner_rejects_multiple_answer_sources() -> None:
    try:
        build_reasoning_contract_run(
            DEFAULT_FIXTURE,
            query_id="SRQ-05",
            answer_text="sample",
            sample_id="srq05-hetuvidya-non-pervasive-pass",
        )
    except FixtureError as exc:
        assert "Provide at most one" in str(exc)
    else:
        raise AssertionError("multiple answer sources should fail")


def test_reasoning_contract_runner_cli_json_output_is_machine_readable() -> None:
    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--query-id",
            "SRQ-05",
            "--sample-id",
            "srq05-hetuvidya-non-pervasive-pass",
            "--json",
        ],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=True,
    )
    data = json.loads(result.stdout)

    assert data["mode"] == "reasoning-contract-runner-v0"
    assert data["query_id"] == "SRQ-05"
    assert data["overall_status"] == "pass"
    assert data["validators"]["hetuvidya"]["case_ids"] == ["ZR-07"]


def test_reasoning_contract_runner_passes_cognitive_practice_boundary_sample() -> None:
    result = build_reasoning_contract_run(
        DEFAULT_FIXTURE,
        query_id="SRQ-09",
        sample_id="srq09-cognitive-practice-boundary-pass",
    )

    assert result["overall_status"] == "pass"
    assert result["role_coverage"]["coverage_status"] == "complete"
    assert result["role_coverage"]["missing_needs"] == []
    assert result["answer_review_status"] == "pass"
    assert result["answer_contract_review"]["overall_status"] == "pass"
    assert result["validators"]["hetuvidya"]["status"] == "not_applicable"

def test_reasoning_contract_runner_passes_cognitive_caregiving_boundary_sample() -> None:
    result = build_reasoning_contract_run(
        DEFAULT_FIXTURE,
        query_id="SRQ-10",
        sample_id="srq10-cognitive-caregiving-boundary-pass",
    )

    assert result["overall_status"] == "pass"
    assert result["role_coverage"]["coverage_status"] == "complete"
    assert result["role_coverage"]["missing_needs"] == []
    assert result["answer_review_status"] == "pass"
    assert result["answer_contract_review"]["overall_status"] == "pass"
    assert result["validators"]["hetuvidya"]["status"] == "not_applicable"
