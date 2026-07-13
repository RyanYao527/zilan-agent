import json
import subprocess
import sys
from pathlib import Path

from zilanlib.reasoning.contract_runner import build_reasoning_contract_run
from zilanlib.semantic.retrieval_dry_run import DEFAULT_FIXTURE, FixtureError

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "reasoning_contract_runner.py"

NOT_APPLICABLE_HETUVIDYA = {
    "status": "not_applicable",
    "validator": "hetuvidya_validator",
    "contract_family": "hetuvidya",
    "output_schema": "hetuvidya-validator-output-v0.1",
    "source": "tests/reasoning_cases.yaml",
    "case_ids": [],
    "validations": [],
    "limitations": [
        "No selected reasoning case with hetuvidya role was found for this query fixture.",
    ],
}

NOT_APPLICABLE_COLLECTED_TOPICS = {
    "status": "not_applicable",
    "validator": "collected_topics_analyzer",
    "contract_family": "collected_topics",
    "output_schema": "collected-topics-analyzer-output-v0",
    "source": "tests/reasoning_cases.yaml",
    "case_ids": [],
    "analyses": [],
    "limitations": [
        "No selected reasoning case with collected_topics role was found for this query fixture.",
    ],
}

NOT_APPLICABLE_MADHYAMAKA = {
    "status": "not_applicable",
    "validator": "madhyamaka_critique_engine",
    "contract_family": "madhyamaka_prasanga",
    "output_schema": "madhyamaka-critique-engine-output-v0",
    "source": "tests/reasoning_cases.yaml",
    "case_ids": [],
    "critiques": [],
    "limitations": [
        "No selected reasoning case with madhyamaka_prasanga role was found for this query fixture.",
    ],
}

NOT_APPLICABLE_COGNITIVE_ANALYSIS = {
    "status": "not_applicable",
    "validator": "cognitive_analysis_mapper",
    "contract_family": "cognitive_analysis",
    "output_schema": "cognitive-analysis-mapper-output-v0",
    "source": "tests/reasoning_cases.yaml",
    "case_ids": [],
    "mappings": [],
    "limitations": [
        "No selected reasoning case with cognitive_analysis role was found for this query fixture.",
    ],
}

NOT_APPLICABLE_AGAMA_EVIDENCE = {
    "status": "not_applicable",
    "validator": "agama_evidence_checker",
    "contract_family": "agama_evidence",
    "output_schema": "agama-evidence-checker-output-v0.1",
    "source": "tests/reasoning_cases.yaml",
    "case_ids": [],
    "evidence_reviews": [],
    "limitations": [
        "No selected reasoning case with agama_evidence role was found for this query fixture.",
    ],
}
CHAIN_STEP_ROLES = [
    "input_contact",
    "attention_orientation",
    "feeling_tone",
    "classification_labeling",
    "volitional_response",
]


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
    assert result["validators"]["collected_topics"] == NOT_APPLICABLE_COLLECTED_TOPICS
    assert result["validators"]["madhyamaka_prasanga"] == NOT_APPLICABLE_MADHYAMAKA
    assert result["validators"]["cognitive_analysis"] == NOT_APPLICABLE_COGNITIVE_ANALYSIS


def test_reasoning_contract_runner_runs_madhyamaka_critique_engine_for_srq08() -> None:
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
    assert result["validators"]["hetuvidya"] == NOT_APPLICABLE_HETUVIDYA
    assert result["validators"]["collected_topics"] == NOT_APPLICABLE_COLLECTED_TOPICS
    assert result["validators"]["cognitive_analysis"] == NOT_APPLICABLE_COGNITIVE_ANALYSIS

    madhyamaka_validator = result["validators"]["madhyamaka_prasanga"]
    assert madhyamaka_validator["status"] == "run"
    assert madhyamaka_validator["case_ids"] == ["ZR-09"]
    assert madhyamaka_validator["critiques"][0]["case_id"] == "ZR-09"
    assert madhyamaka_validator["critiques"][0]["madhyamaka_prasanga"]["no_independent_thesis"] == {
        "required": True,
        "status": "required",
    }


def test_reasoning_contract_runner_marks_answer_contracts_without_answer_as_review_needed() -> None:
    result = build_reasoning_contract_run(DEFAULT_FIXTURE, query_id="SRQ-05")

    assert result["overall_status"] == "review_needed"
    assert result["answer_review_status"] == "review_needed"
    assert result["answer_contract_review"] is None
    assert result["validators"]["hetuvidya"]["status"] == "run"
    assert result["validators"]["collected_topics"] == NOT_APPLICABLE_COLLECTED_TOPICS
    assert result["validators"]["madhyamaka_prasanga"] == NOT_APPLICABLE_MADHYAMAKA
    assert result["validators"]["cognitive_analysis"] == NOT_APPLICABLE_COGNITIVE_ANALYSIS


def test_reasoning_contract_runner_fails_when_role_coverage_is_incomplete() -> None:
    result = build_reasoning_contract_run(DEFAULT_FIXTURE, query_id="SRQ-01", limit=1)

    assert result["overall_status"] == "fail"
    assert result["answer_review_status"] == "no_answer_contracts"
    assert result["role_coverage"]["missing_needs"] == [
        "collected_topics",
        "hetuvidya",
        "madhyamaka_prasanga",
    ]
    assert result["validators"]["hetuvidya"] == NOT_APPLICABLE_HETUVIDYA
    assert result["validators"]["collected_topics"] == NOT_APPLICABLE_COLLECTED_TOPICS
    assert result["validators"]["madhyamaka_prasanga"] == NOT_APPLICABLE_MADHYAMAKA
    assert result["validators"]["cognitive_analysis"] == NOT_APPLICABLE_COGNITIVE_ANALYSIS


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
    assert data["validators"]["collected_topics"] == NOT_APPLICABLE_COLLECTED_TOPICS
    assert data["validators"]["madhyamaka_prasanga"] == NOT_APPLICABLE_MADHYAMAKA
    assert data["validators"]["cognitive_analysis"] == NOT_APPLICABLE_COGNITIVE_ANALYSIS


def test_reasoning_contract_runner_runs_collected_topics_analyzer_for_srq07() -> None:
    result = build_reasoning_contract_run(
        DEFAULT_FIXTURE,
        query_id="SRQ-07",
        sample_id="srq07-collected-topics-total-part-pass",
    )

    assert result["overall_status"] == "pass"
    assert result["role_coverage"]["coverage_status"] == "complete"
    assert result["role_coverage"]["missing_needs"] == []
    assert result["answer_review_status"] == "pass"
    assert result["answer_contract_review"]["overall_status"] == "pass"
    assert result["validators"]["hetuvidya"] == NOT_APPLICABLE_HETUVIDYA
    assert result["validators"]["madhyamaka_prasanga"] == NOT_APPLICABLE_MADHYAMAKA
    assert result["validators"]["cognitive_analysis"] == NOT_APPLICABLE_COGNITIVE_ANALYSIS

    collected_topics_validator = result["validators"]["collected_topics"]
    assert collected_topics_validator["status"] == "run"
    assert collected_topics_validator["case_ids"] == ["ZR-02"]
    assert collected_topics_validator["analyses"][0]["case_id"] == "ZR-02"
    relation_checks = {
        item["id"]: item["status"]
        for item in collected_topics_validator["analyses"][0]["collected_topics"]["relation_checks"]
    }
    assert relation_checks == {
        "pervasion": "fail",
        "total_part_distinction": "required",
    }


def test_reasoning_contract_runner_runs_cognitive_mapper_for_srq09() -> None:
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
    assert result["validators"]["hetuvidya"] == NOT_APPLICABLE_HETUVIDYA
    assert result["validators"]["collected_topics"] == NOT_APPLICABLE_COLLECTED_TOPICS
    assert result["validators"]["madhyamaka_prasanga"] == NOT_APPLICABLE_MADHYAMAKA

    cognitive_validator = result["validators"]["cognitive_analysis"]
    assert cognitive_validator["status"] == "run"
    assert cognitive_validator["case_ids"] == ["ZR-10"]
    assert cognitive_validator["mappings"][0]["case_id"] == "ZR-10"
    assert cognitive_validator["mappings"][0]["cognitive_analysis"]["practice_boundary"] == {
        "required": True,
        "status": "required",
    }


def test_reasoning_contract_runner_runs_cognitive_mapper_for_srq10() -> None:
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
    assert result["validators"]["hetuvidya"] == NOT_APPLICABLE_HETUVIDYA
    assert result["validators"]["collected_topics"] == NOT_APPLICABLE_COLLECTED_TOPICS
    assert result["validators"]["madhyamaka_prasanga"] == NOT_APPLICABLE_MADHYAMAKA

    cognitive_validator = result["validators"]["cognitive_analysis"]
    assert cognitive_validator["status"] == "run"
    assert cognitive_validator["case_ids"] == ["ZR-11"]
    assert cognitive_validator["mappings"][0]["case_id"] == "ZR-11"
    chain_steps = cognitive_validator["mappings"][0]["cognitive_analysis"]["chain_steps"]
    assert [item["role"] for item in chain_steps] == CHAIN_STEP_ROLES

def test_reasoning_contract_runner_runs_agama_evidence_checker_for_srq04() -> None:
    result = build_reasoning_contract_run(
        DEFAULT_FIXTURE,
        query_id="SRQ-04",
        sample_id="srq04-agama-citation-boundary-pass",
    )

    assert result["overall_status"] == "pass"
    assert result["role_coverage"]["coverage_status"] == "complete"
    assert result["role_coverage"]["missing_needs"] == []
    assert result["answer_review_status"] == "pass"
    assert result["answer_contract_review"]["overall_status"] == "pass"
    assert result["validators"]["hetuvidya"] == NOT_APPLICABLE_HETUVIDYA
    assert result["validators"]["collected_topics"] == NOT_APPLICABLE_COLLECTED_TOPICS
    assert result["validators"]["madhyamaka_prasanga"] == NOT_APPLICABLE_MADHYAMAKA
    assert result["validators"]["cognitive_analysis"] == NOT_APPLICABLE_COGNITIVE_ANALYSIS

    agama_validator = result["validators"]["agama_evidence"]
    assert agama_validator["status"] == "run"
    assert agama_validator["validator"] == "agama_evidence_checker"
    assert agama_validator["case_ids"] == ["ZR-05"]
    review = agama_validator["evidence_reviews"][0]
    assert review["case_id"] == "ZR-05"
    assert review["agama_evidence"]["citation_required"]["status"] == "required"
    assert review["agama_evidence"]["search_scope"]["scope"] == "representative_search"
    assert review["agama_evidence"]["collation_boundary"]["status"] == "required"
    assert review["agama_evidence"]["local_evidence"]["status"] == "pass"
    assert review["agama_evidence"]["local_evidence"]["failed_passage_anchors"] == []
