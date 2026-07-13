from zilanlib.semantic.answer_contract_review import build_answer_contract_review
from zilanlib.semantic.retrieval_dry_run import DEFAULT_FIXTURE


def test_answer_contract_review_passes_for_agama_citation_boundary_sample() -> None:
    result = build_answer_contract_review(
        DEFAULT_FIXTURE,
        query_id="SRQ-04",
        sample_id="srq04-agama-citation-boundary-pass",
    )

    assert result["overall_status"] == "pass"
    assert result["expected_status"] == "pass"
    assert result["expected_status_match"] is True
    assert result["reviews"][0]["contract_id"] == "agama_citation_boundary"
    assert result["reviews"][0]["missing_required_terms"] == []
    assert result["reviews"][0]["present_forbidden_terms"] == []
    assert result["reviews"][0]["missing_required_slots"] == []


def test_answer_contract_review_fails_for_agama_citation_boundary_negative_sample() -> None:
    result = build_answer_contract_review(
        DEFAULT_FIXTURE,
        query_id="SRQ-04",
        sample_id="srq04-agama-citation-boundary-fail",
    )

    assert result["overall_status"] == "fail"
    assert result["expected_status"] == "fail"
    assert result["expected_status_match"] is True
    assert result["reviews"][0]["missing_required_terms"] == [
        "CBETA",
        "T02n0099",
        "context/agama/",
        "检索范围",
        "代表性",
        "待校勘",
    ]
    assert result["reviews"][0]["present_forbidden_terms"] == [
        "已穷尽",
        "无需校勘",
        "可作为定本",
        "校勘完成",
        "校勘确认",
    ]
