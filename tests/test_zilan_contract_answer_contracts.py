from __future__ import annotations

from pathlib import Path

from zilan_contract import AnswerContractRunner

CONTRACTS = {
    "medical_disclaimer": {
        "description": "Medical answer must include emergency and advice boundaries.",
        "required_terms": ["not medical advice", "doctor", "emergency"],
        "forbidden_terms": ["guaranteed", "definitely"],
        "required_slots": [
            {"label": "disclaimer", "terms": ["not medical advice"]},
            {"label": "care_path", "terms": ["doctor", "emergency"]},
        ],
    }
}


def test_answer_contract_runner_passes_domain_neutral_answer() -> None:
    result = AnswerContractRunner().check(
        answer_text="This is not medical advice. Call emergency services or consult a doctor.",
        contracts=CONTRACTS,
    )

    assert result.overall_status == "pass"
    assert result.passed() is True
    assert result.issues() == []
    assert result.to_summary() == {
        "overall_status": "pass",
        "contract_count": 1,
        "issue_count": 0,
    }


def test_answer_contract_runner_reports_missing_and_forbidden_terms() -> None:
    result = AnswerContractRunner().check(
        answer_text="Turmeric tea is guaranteed to help. It definitely works.",
        contracts=CONTRACTS,
    )

    assert result.overall_status == "fail"
    summary = result.to_summary()
    assert summary["issue_count"] == 7
    assert {issue.kind for issue in result.issues()} == {
        "missing_required_term",
        "present_forbidden_term",
        "missing_required_slot",
    }
    assert "medical_disclaimer" in result.to_markdown()


def test_answer_contract_runner_checks_answer_file(tmp_path: Path) -> None:
    answer_file = tmp_path / "answer.md"
    answer_file.write_text("This is not medical advice. Call emergency services or consult a doctor.", encoding="utf-8")

    result = AnswerContractRunner().check_file(answer_file=answer_file, contracts=CONTRACTS)

    assert result.passed() is True
