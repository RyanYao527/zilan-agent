from __future__ import annotations

from zilanlib.semantic.answer_contract_review import build_answer_contract_review
from zilanlib.semantic.retrieval_dry_run import DEFAULT_FIXTURE

MISMATCHED_REPRESENTATIVE_ANCHOR_ANSWER = """
检索范围：本次只基于本地 context/agama/ 中四阿含材料做代表性检索。
为保留 CBETA 编号，另列 T02n0099 作为检索书目；代表性引文之一为
《長阿含經》(T01n0001) 卷 1, context/agama/T0001-chang-agama.md:881。
边界：以上仅为初步证据，出版级引文仍待校勘。
"""

CANONICAL_REPRESENTATIVE_ANCHOR_ANSWER = (
    "检索范围：本次只基于本地 context/agama/ 中四阿含材料做代表性检索。\n"
    "代表性引文之一：《雜阿含經》(T02n0099) 卷 1, （九）, "
    "context/agama/T0099-za-agama.md:147-149；该处保留 CBETA 编号和本地行锚点。\n"
    "边界：以上仅为初步证据，出版级引文仍待校勘。\n"
)


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


def test_answer_contract_review_rejects_srq04_mismatched_representative_anchor() -> None:
    result = build_answer_contract_review(
        DEFAULT_FIXTURE,
        query_id="SRQ-04",
        answer_text=MISMATCHED_REPRESENTATIVE_ANCHOR_ANSWER,
    )

    assert result["overall_status"] == "fail"
    assert result["reviews"][0]["missing_required_slots"] == ["representative_agama_anchor"]


def test_answer_contract_review_accepts_srq04_canonical_representative_anchor() -> None:
    result = build_answer_contract_review(
        DEFAULT_FIXTURE,
        query_id="SRQ-04",
        answer_text=CANONICAL_REPRESENTATIVE_ANCHOR_ANSWER,
    )

    assert result["overall_status"] == "pass"
    assert result["reviews"][0]["missing_required_slots"] == []
