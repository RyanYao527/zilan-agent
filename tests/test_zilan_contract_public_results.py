from __future__ import annotations

from zilan_contract import ContractResult, ContractRunner
from zilan_contract.results import ContractIssue


def test_contract_result_extracts_answer_contract_issues() -> None:
    result = ContractRunner(source_root=None).check(
        query_id="SRQ-04",
        sample_id="srq04-agama-citation-boundary-fail",
    )

    issues = result.issues()

    assert issues
    assert all(isinstance(issue, ContractIssue) for issue in issues)
    assert any(issue.kind == "missing_required_term" for issue in issues)
    assert any(issue.kind == "present_forbidden_term" for issue in issues)
    markdown = result.to_markdown()
    assert any(issue.detail in markdown for issue in issues)


def test_contract_result_summary_and_markdown_are_stable() -> None:
    result = ContractRunner(source_root=None).check(
        query_id="SRQ-05",
        sample_id="srq05-hetuvidya-non-pervasive-pass",
    )

    assert result.to_summary() == {
        "overall_status": "pass",
        "answer_review_status": "pass",
        "query_id": "SRQ-05",
        "failed_validators": [],
        "issue_count": 0,
    }
    markdown = result.to_markdown()
    assert "# zilan_contract Review" in markdown
    assert "Overall status: pass" in markdown
    assert "Failed validators: none" in markdown


def test_contract_result_import_remains_backward_compatible() -> None:
    result = ContractResult({"overall_status": "pass", "validators": {}})

    assert result.passed() is True
    assert result.failed_validators() == []


def test_contract_result_failed_validators_ignores_run_and_not_applicable_statuses() -> None:
    result = ContractResult(
        {
            "overall_status": "pass",
            "validators": {
                "retrieval": {"status": "run"},
                "local_evidence": {"status": "not_applicable"},
                "answer_contract": {"status": "fail"},
            },
        }
    )

    assert result.failed_validators() == ["answer_contract"]
