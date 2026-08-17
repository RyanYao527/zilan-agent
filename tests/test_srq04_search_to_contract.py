from __future__ import annotations

from pathlib import Path

from zilanlib.agama.search import search_agama
from zilanlib.semantic.answer_contract_review import build_answer_contract_review
from zilanlib.semantic.retrieval_dry_run import DEFAULT_FIXTURE

ROOT = Path(__file__).resolve().parents[1]


def test_search_citation_satisfies_srq04_representative_anchor_contract() -> None:
    matches = search_agama("色無常，無常即苦，苦即非我", root=ROOT, limit=0)
    representative = next(match for match in matches if match.cbeta_id == "T02n0099" and match.line == 147)
    answer = (
        "检索范围：本次只基于本地 context/agama/ 做代表性检索。\n"
        f"代表性引文：{representative.citation}\n"
        "CBETA 编号保留。\n"
        "边界：这是初步证据，出版级引文仍待校勘。\n"
    )

    result = build_answer_contract_review(DEFAULT_FIXTURE, query_id="SRQ-04", answer_text=answer)

    assert representative.citation.endswith("context/agama/T0099-za-agama.md:147")
    assert result["overall_status"] == "pass"
    assert result["reviews"][0]["missing_required_slots"] == []
