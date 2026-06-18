import json
import subprocess
import sys
from pathlib import Path

from semantic_answer_boundary_review import build_answer_boundary_review
from semantic_retrieval_dry_run import DEFAULT_FIXTURE, FixtureError

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "semantic_answer_boundary_review.py"


PASSING_ANSWER = (
    "边界：以下只是基于本地 context 的义理分析，不等于修证，也不构成临床、医疗或心理治疗建议。"
)


def test_answer_boundary_review_passes_when_required_terms_are_present() -> None:
    result = build_answer_boundary_review(DEFAULT_FIXTURE, query_id="SRQ-01", answer_text=PASSING_ANSWER)

    assert result["mode"] == "semantic-answer-boundary-review"
    assert result["overall_status"] == "pass"
    assert result["non_chunk_needs"] == ["practice_boundary"]
    assert result["reviews"][0]["need"] == "practice_boundary"
    assert result["reviews"][0]["missing_required_terms"] == []
    assert result["reviews"][0]["present_forbidden_terms"] == []


def test_answer_boundary_review_fails_when_required_terms_are_missing() -> None:
    result = build_answer_boundary_review(DEFAULT_FIXTURE, query_id="SRQ-01", answer_text="诸法无我，可以这样理解。")

    assert result["overall_status"] == "fail"
    assert "边界" in result["reviews"][0]["missing_required_terms"]
    assert "不等于修证" in result["reviews"][0]["missing_required_terms"]


def test_answer_boundary_review_fails_when_forbidden_terms_are_present() -> None:
    result = build_answer_boundary_review(
        DEFAULT_FIXTURE,
        query_id="SRQ-01",
        answer_text=PASSING_ANSWER + " 这可以保证证悟。",
    )

    assert result["overall_status"] == "fail"
    assert result["reviews"][0]["present_forbidden_terms"] == ["保证证悟"]


def test_answer_boundary_review_unknown_query_id_is_reported() -> None:
    try:
        build_answer_boundary_review(DEFAULT_FIXTURE, query_id="SRQ-99", answer_text=PASSING_ANSWER)
    except FixtureError as exc:
        assert "Unknown query id: SRQ-99" in str(exc)
    else:
        raise AssertionError("unknown query id should fail")


def test_answer_boundary_review_cli_json_output_is_machine_readable() -> None:
    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--query-id",
            "SRQ-01",
            "--answer-text",
            PASSING_ANSWER,
            "--json",
        ],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=True,
    )
    data = json.loads(result.stdout)

    assert data["mode"] == "semantic-answer-boundary-review"
    assert data["query_id"] == "SRQ-01"
    assert data["overall_status"] == "pass"
    assert data["reviews"][0]["status"] == "pass"
