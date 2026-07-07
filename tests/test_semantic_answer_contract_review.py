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


def test_answer_contract_review_passes_for_madhyamaka_nihilism_boundary_sample() -> None:
    result = build_answer_contract_review(
        DEFAULT_FIXTURE,
        query_id="SRQ-08",
        sample_id="srq08-madhyamaka-nihilism-boundary-pass",
    )

    assert result["overall_status"] == "pass"
    assert result["expected_status"] == "pass"
    assert result["expected_status_match"] is True
    assert result["reviews"][0]["contract_id"] == "madhyamaka_nihilism_boundary"
    assert result["reviews"][0]["missing_required_terms"] == []
    assert result["reviews"][0]["missing_required_slots"] == []
    assert result["reviews"][0]["present_forbidden_terms"] == []


def test_answer_contract_review_fails_for_madhyamaka_nihilism_boundary_negative_sample() -> None:
    result = build_answer_contract_review(
        DEFAULT_FIXTURE,
        query_id="SRQ-08",
        sample_id="srq08-madhyamaka-nihilism-boundary-fail",
    )

    assert result["overall_status"] == "fail"
    assert result["expected_status"] == "fail"
    assert result["expected_status_match"] is True
    assert "中观" in result["reviews"][0]["missing_required_terms"]
    assert "无自性" in result["reviews"][0]["missing_required_terms"]
    assert "只破自性有" in result["reviews"][0]["missing_required_terms"]
    assert "缘起" in result["reviews"][0]["missing_required_terms"]
    assert "不成立" in result["reviews"][0]["missing_required_terms"]
    assert result["reviews"][0]["present_forbidden_terms"] == [
        "空性等于什么都没有",
        "因果已经被取消",
        "可以直接推出断灭",
        "无需二谛",
    ]
    assert result["reviews"][0]["missing_required_slots"] == [
        "proposition_decomposition",
        "emptiness_boundary",
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


def test_answer_contract_review_passes_for_collected_topics_total_part_sample() -> None:
    result = build_answer_contract_review(
        DEFAULT_FIXTURE,
        query_id="SRQ-07",
        sample_id="srq07-collected-topics-total-part-pass",
    )

    assert result["overall_status"] == "pass"
    assert result["expected_status"] == "pass"
    assert result["expected_status_match"] is True
    assert result["reviews"][0]["contract_id"] == "collected_topics_total_part_error"
    assert result["reviews"][0]["missing_required_terms"] == []
    assert result["reviews"][0]["missing_required_slots"] == []
    assert result["reviews"][0]["present_forbidden_terms"] == []


def test_answer_contract_review_fails_for_collected_topics_total_part_negative_sample() -> None:
    result = build_answer_contract_review(
        DEFAULT_FIXTURE,
        query_id="SRQ-07",
        sample_id="srq07-collected-topics-total-part-fail",
    )

    assert result["overall_status"] == "fail"
    assert result["expected_status"] == "fail"
    assert result["expected_status_match"] is True
    assert "总与别" in result["reviews"][0]["missing_required_terms"]
    assert "不周遍" in result["reviews"][0]["missing_required_terms"]
    assert result["reviews"][0]["present_forbidden_terms"] == [
        "所以我没有价值",
        "可以直接推出",
        "不需区分总别",
    ]
    assert result["reviews"][0]["missing_required_slots"] == [
        "proposition_decomposition",
        "pervasion_check",
        "error_classification",
    ]


def test_answer_contract_review_passes_for_cognitive_practice_boundary_sample() -> None:
    result = build_answer_contract_review(
        DEFAULT_FIXTURE,
        query_id="SRQ-09",
        sample_id="srq09-cognitive-practice-boundary-pass",
    )

    assert result["overall_status"] == "pass"
    assert result["expected_status"] == "pass"
    assert result["expected_status_match"] is True
    assert result["reviews"][0]["contract_id"] == "cognitive_practice_boundary"
    assert result["reviews"][0]["missing_required_terms"] == []
    assert result["reviews"][0]["missing_required_slots"] == []
    assert result["reviews"][0]["present_forbidden_terms"] == []


def test_answer_contract_review_fails_for_cognitive_practice_boundary_negative_sample() -> None:
    result = build_answer_contract_review(
        DEFAULT_FIXTURE,
        query_id="SRQ-09",
        sample_id="srq09-cognitive-practice-boundary-fail",
    )

    assert result["overall_status"] == "fail"
    assert result["expected_status"] == "fail"
    assert result["expected_status_match"] is True
    assert "心类学" in result["reviews"][0]["missing_required_terms"]
    assert "触" in result["reviews"][0]["missing_required_terms"]
    assert result["reviews"][0]["present_forbidden_terms"] == [
        "保证疗愈",
        "等同心理治疗",
        "已证观智",
        "无需善知识",
    ]
    assert result["reviews"][0]["missing_required_slots"] == [
        "cognitive_chain",
        "cognitive_quality",
        "corrective_factors",
        "vipassana_mapping",
        "practice_boundary",
    ]

def test_answer_contract_review_passes_for_cognitive_caregiving_boundary_sample() -> None:
    result = build_answer_contract_review(
        DEFAULT_FIXTURE,
        query_id="SRQ-10",
        sample_id="srq10-cognitive-caregiving-boundary-pass",
    )

    assert result["overall_status"] == "pass"
    assert result["expected_status"] == "pass"
    assert result["expected_status_match"] is True
    assert result["reviews"][0]["contract_id"] == "cognitive_caregiving_boundary"
    assert result["reviews"][0]["missing_required_terms"] == []
    assert result["reviews"][0]["missing_required_slots"] == []
    assert result["reviews"][0]["present_forbidden_terms"] == []


def test_answer_contract_review_fails_for_cognitive_caregiving_boundary_negative_sample() -> None:
    result = build_answer_contract_review(
        DEFAULT_FIXTURE,
        query_id="SRQ-10",
        sample_id="srq10-cognitive-caregiving-boundary-fail",
    )

    assert result["overall_status"] == "fail"
    assert result["expected_status"] == "fail"
    assert result["expected_status_match"] is True
    assert "心类学" in result["reviews"][0]["missing_required_terms"]
    assert "错误归因" in result["reviews"][0]["missing_required_terms"]
    assert result["reviews"][0]["present_forbidden_terms"] == [
        "对方一定故意",
        "直接压下愤怒",
        "保证疗愈",
        "等同心理治疗",
        "已证观智",
        "无需善知识",
    ]
    assert result["reviews"][0]["missing_required_slots"] == [
        "cognitive_chain",
        "attribution_error",
        "affliction_chain",
        "corrective_factors",
        "vipassana_mapping",
        "practice_boundary",
    ]
