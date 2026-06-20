import json
import subprocess
import sys
from pathlib import Path

from semantic_answer_contract_review import build_answer_contract_review
from semantic_retrieval_dry_run import DEFAULT_FIXTURE, FixtureError

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "semantic_answer_contract_review.py"


PASSING_ANSWER = "论式判定：因不成。第一相遍是宗法性不成立：色形不是声的属性。"


def test_answer_contract_review_passes_when_required_terms_are_present() -> None:
    result = build_answer_contract_review(DEFAULT_FIXTURE, query_id="SRQ-02", answer_text=PASSING_ANSWER)

    assert result["mode"] == "semantic-answer-contract-review"
    assert result["overall_status"] == "pass"
    assert result["answer_source"] == {"type": "inline"}
    assert result["reviews"][0]["contract_id"] == "hetuvidya_error_detection"
    assert result["reviews"][0]["missing_required_terms"] == []
    assert result["reviews"][0]["present_forbidden_terms"] == []
    assert result["reviews"][0]["missing_required_slots"] == []
    assert result["reviews"][0]["required_slots"][0]["label"] == "argument_decomposition"


def test_answer_contract_review_passes_from_checked_in_sample() -> None:
    result = build_answer_contract_review(
        DEFAULT_FIXTURE,
        query_id="SRQ-02",
        sample_id="srq02-hetuvidya-error-pass",
    )

    assert result["overall_status"] == "pass"
    assert result["expected_status"] == "pass"
    assert result["expected_status_match"] is True
    assert result["answer_source"] == {
        "type": "sample",
        "sample_id": "srq02-hetuvidya-error-pass",
        "file": "tests/fixtures/answers/srq02-hetuvidya-error-pass.md",
        "expected_status": "pass",
    }


def test_answer_contract_review_fails_from_checked_in_negative_sample() -> None:
    result = build_answer_contract_review(
        DEFAULT_FIXTURE,
        query_id="SRQ-02",
        sample_id="srq02-hetuvidya-error-fail",
    )

    assert result["overall_status"] == "fail"
    assert result["expected_status"] == "fail"
    assert result["expected_status_match"] is True
    assert result["reviews"][0]["missing_required_terms"] == ["因不成", "遍是宗法性", "不成立"]
    assert result["reviews"][0]["present_forbidden_terms"] == ["因三相完全满足", "正因成立"]


def test_answer_contract_review_fails_when_required_terms_are_missing() -> None:
    result = build_answer_contract_review(DEFAULT_FIXTURE, query_id="SRQ-02", answer_text="声可见，因为是色形。")

    assert result["overall_status"] == "fail"
    assert "因不成" in result["reviews"][0]["missing_required_terms"]
    assert "遍是宗法性" in result["reviews"][0]["missing_required_terms"]
    assert "不成立" in result["reviews"][0]["missing_required_terms"]


def test_answer_contract_review_fails_when_required_slot_is_missing() -> None:
    result = build_answer_contract_review(
        DEFAULT_FIXTURE,
        query_id="SRQ-02",
        answer_text="判定：因不成。遍是宗法性不成立：色形不是声的属性。",
    )

    assert result["overall_status"] == "fail"
    assert result["reviews"][0]["missing_required_terms"] == []
    assert result["reviews"][0]["present_forbidden_terms"] == []
    assert result["reviews"][0]["missing_required_slots"] == ["argument_decomposition"]


def test_answer_contract_review_fails_when_forbidden_terms_are_present() -> None:
    result = build_answer_contract_review(
        DEFAULT_FIXTURE,
        query_id="SRQ-02",
        answer_text=PASSING_ANSWER + " 因三相完全满足，正因成立。",
    )

    assert result["overall_status"] == "fail"
    assert result["reviews"][0]["present_forbidden_terms"] == ["因三相完全满足", "正因成立"]


def test_answer_contract_review_unknown_sample_id_is_reported() -> None:
    try:
        build_answer_contract_review(DEFAULT_FIXTURE, query_id="SRQ-02", sample_id="missing-sample")
    except FixtureError as exc:
        assert "Unknown answer contract sample id for SRQ-02" in str(exc)
    else:
        raise AssertionError("unknown answer contract sample id should fail")


def test_answer_contract_review_cli_json_output_is_machine_readable() -> None:
    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--query-id",
            "SRQ-02",
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

    assert data["mode"] == "semantic-answer-contract-review"
    assert data["query_id"] == "SRQ-02"
    assert data["overall_status"] == "pass"
    assert data["reviews"][0]["status"] == "pass"


def test_answer_contract_review_cli_can_use_checked_in_sample() -> None:
    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--query-id",
            "SRQ-02",
            "--sample-id",
            "srq02-hetuvidya-error-pass",
            "--json",
        ],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=True,
    )
    data = json.loads(result.stdout)

    assert data["overall_status"] == "pass"
    assert data["answer_source"]["type"] == "sample"
    assert data["expected_status_match"] is True


def test_answer_contract_review_passes_for_madhyamaka_prasanga_sample() -> None:
    result = build_answer_contract_review(
        DEFAULT_FIXTURE,
        query_id="SRQ-03",
        sample_id="srq03-madhyamaka-prasanga-pass",
    )

    assert result["overall_status"] == "pass"
    assert result["expected_status"] == "pass"
    assert result["expected_status_match"] is True
    assert result["reviews"][0]["contract_id"] == "madhyamaka_prasanga_boundary"
    assert result["reviews"][0]["missing_required_terms"] == []
    assert result["reviews"][0]["present_forbidden_terms"] == []


def test_answer_contract_review_fails_for_madhyamaka_prasanga_negative_sample() -> None:
    result = build_answer_contract_review(
        DEFAULT_FIXTURE,
        query_id="SRQ-03",
        sample_id="srq03-madhyamaka-prasanga-fail",
    )

    assert result["overall_status"] == "fail"
    assert result["expected_status"] == "fail"
    assert result["expected_status_match"] is True
    assert result["reviews"][0]["missing_required_terms"] == [
        "对方承许",
        "归谬",
        "自性有",
        "缘起",
        "矛盾",
        "不立自宗",
    ]
    assert result["reviews"][0]["present_forbidden_terms"] == [
        "我方建立自宗",
        "证明诸法绝对不存在",
        "断灭",
    ]


def test_answer_contract_review_passes_for_hetuvidya_non_pervasive_sample() -> None:
    result = build_answer_contract_review(
        DEFAULT_FIXTURE,
        query_id="SRQ-05",
        sample_id="srq05-hetuvidya-non-pervasive-pass",
    )

    assert result["overall_status"] == "pass"
    assert result["expected_status"] == "pass"
    assert result["expected_status_match"] is True
    assert result["reviews"][0]["contract_id"] == "hetuvidya_non_pervasive_detection"
    assert result["reviews"][0]["missing_required_terms"] == []
    assert result["reviews"][0]["missing_required_slots"] == []
    assert result["reviews"][0]["present_forbidden_terms"] == []


def test_answer_contract_review_fails_for_hetuvidya_non_pervasive_negative_sample() -> None:
    result = build_answer_contract_review(
        DEFAULT_FIXTURE,
        query_id="SRQ-05",
        sample_id="srq05-hetuvidya-non-pervasive-fail",
    )

    assert result["overall_status"] == "fail"
    assert result["expected_status"] == "fail"
    assert result["expected_status_match"] is True
    assert result["reviews"][0]["missing_required_terms"] == [
        "不周遍",
        "遍是宗法性",
        "异品遍无性",
        "常法",
        "不成立",
    ]
    assert result["reviews"][0]["present_forbidden_terms"] == ["因三相完全满足", "正因成立"]
    assert result["reviews"][0]["missing_required_slots"] == [
        "subject_check",
        "pervasion_failure",
        "counterexample",
    ]


def test_answer_contract_review_passes_for_hetuvidya_indeterminate_sample() -> None:
    result = build_answer_contract_review(
        DEFAULT_FIXTURE,
        query_id="SRQ-06",
        sample_id="srq06-hetuvidya-indeterminate-pass",
    )

    assert result["overall_status"] == "pass"
    assert result["expected_status"] == "pass"
    assert result["expected_status_match"] is True
    assert result["reviews"][0]["contract_id"] == "hetuvidya_indeterminate_detection"
    assert result["reviews"][0]["missing_required_terms"] == []
    assert result["reviews"][0]["missing_required_slots"] == []
    assert result["reviews"][0]["present_forbidden_terms"] == []


def test_answer_contract_review_fails_for_hetuvidya_indeterminate_negative_sample() -> None:
    result = build_answer_contract_review(
        DEFAULT_FIXTURE,
        query_id="SRQ-06",
        sample_id="srq06-hetuvidya-indeterminate-fail",
    )

    assert result["overall_status"] == "fail"
    assert result["expected_status"] == "fail"
    assert result["expected_status_match"] is True
    assert "不定因" in result["reviews"][0]["missing_required_terms"]
    assert "不能决定" in result["reviews"][0]["missing_required_terms"]
    assert result["reviews"][0]["present_forbidden_terms"] == ["因三相完全满足", "正因成立"]
    assert result["reviews"][0]["missing_required_slots"] == [
        "subject_check",
        "error_classification",
    ]
