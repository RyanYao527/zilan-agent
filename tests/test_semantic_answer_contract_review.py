from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from zilanlib.semantic.answer_contract_review import build_answer_contract_review
from zilanlib.semantic.retrieval_dry_run import DEFAULT_FIXTURE, FixtureError

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


def test_answer_contract_review_passes_for_srq01_cross_domain_no_self_sample() -> None:
    result = build_answer_contract_review(
        DEFAULT_FIXTURE,
        query_id="SRQ-01",
        sample_id="srq01-cross-domain-no-self-pass",
    )

    assert result["overall_status"] == "pass"
    assert result["expected_status"] == "pass"
    assert result["expected_status_match"] is True
    assert result["reviews"][0]["contract_id"] == "cross_domain_no_self_analysis"
    assert result["reviews"][0]["missing_required_terms"] == []
    assert result["reviews"][0]["missing_required_slots"] == []
    assert result["reviews"][0]["present_forbidden_terms"] == []


def test_answer_contract_review_allows_srq01_negated_nihilism_boundary() -> None:
    answer = (
        "阿含证据 / 代表性检索：本次只基于本地 `context/agama/` 四阿含 Markdown，"
        "列出《雜阿含經》(T02n0099) 的 CBETA 锚点；这些只是代表性检索，仍待校勘。\n"
        "应成论式：对方承许诸法自性有，则以缘起事实作归谬，推出矛盾。\n"
        "因明校验：以因三相检查无常缘起故无我的论式。\n"
        "摄类学：五蕴与我、我所不能混成实体总法。\n"
        "观禅：观察触、作意、受、想、思的名色链路。\n"
        "边界：以上分析不等于修证；把空性理解为断灭，或推出因果不存在，是不成立的误读；"
        "实修需善知识指导。"
    )

    result = build_answer_contract_review(DEFAULT_FIXTURE, query_id="SRQ-01", answer_text=answer)

    assert result["overall_status"] == "pass"
    assert result["reviews"][0]["present_forbidden_terms"] == []


def test_answer_contract_review_rejects_srq01_causality_nonexistence_overclaim() -> None:
    answer = (
        "阿含证据 / 代表性检索：本次只基于本地 `context/agama/` 四阿含 Markdown，"
        "列出《雜阿含經》(T02n0099) 的 CBETA 锚点；这些只是代表性检索，仍待校勘。\n"
        "应成论式：对方承许诸法自性有，则以缘起事实作归谬，推出矛盾。\n"
        "因明校验：以因三相检查无常缘起故无我的论式。\n"
        "摄类学：五蕴与我、我所不能混成实体总法。\n"
        "观禅：观察触、作意、受、想、思的名色链路。\n"
        "边界：以上分析不等于修证；证明因果不存在；实修需善知识指导。"
    )

    result = build_answer_contract_review(DEFAULT_FIXTURE, query_id="SRQ-01", answer_text=answer)

    assert result["overall_status"] == "fail"
    assert result["reviews"][0]["present_forbidden_terms"] == ["证明因果不存在"]


def test_answer_contract_review_passes_for_srq01_runtime_spot_without_literal_labels() -> None:
    result = build_answer_contract_review(
        DEFAULT_FIXTURE,
        query_id="SRQ-01",
        answer_file=ROOT
        / "docs"
        / "runtime-evidence"
        / "2026-08-06-claude-code-zc-05-srq-01-runtime-spot-answer.md",
    )

    assert result["overall_status"] == "pass"
    assert result["reviews"][0]["missing_required_terms"] == []
    assert result["reviews"][0]["missing_required_slots"] == []
    assert result["reviews"][0]["present_forbidden_terms"] == []


def test_answer_contract_review_fails_for_srq01_cross_domain_no_self_negative_sample() -> None:
    result = build_answer_contract_review(
        DEFAULT_FIXTURE,
        query_id="SRQ-01",
        sample_id="srq01-cross-domain-no-self-fail",
    )

    assert result["overall_status"] == "fail"
    assert result["expected_status"] == "fail"
    assert result["expected_status_match"] is True
    assert "CBETA" in result["reviews"][0]["missing_required_terms"]
    assert "context/agama/" in result["reviews"][0]["missing_required_terms"]
    assert "因三相" in result["reviews"][0]["missing_required_terms"]
    assert "不等于修证" in result["reviews"][0]["missing_required_terms"]
    assert result["reviews"][0]["present_forbidden_terms"] == [
        "已证空性",
        "保证证悟",
        "证明诸法绝对不存在",
        "无需善知识",
    ]
    assert result["reviews"][0]["missing_required_slots"] == [
        "agama_evidence",
        "prasanga_argument",
        "hetuvidya_check",
        "collected_topics_check",
        "cognitive_practice_mapping",
        "practice_boundary",
    ]


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
        "断灭的结论",
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
    assert "indeterminate_resolution" in result["reviews"][0]["missing_required_term_groups"]
    assert result["reviews"][0]["present_forbidden_terms"] == ["因三相完全满足", "正因成立"]
    assert result["reviews"][0]["missing_required_slots"] == [
        "subject_check",
        "error_classification",
    ]


def test_answer_contract_review_passes_for_srq06_runtime_spot_with_cannot_decide_alias() -> None:
    result = build_answer_contract_review(
        DEFAULT_FIXTURE,
        query_id="SRQ-06",
        answer_file=ROOT
        / "docs"
        / "runtime-evidence"
        / "2026-08-19-claude-code-srq-06-runtime-spot-answer.md",
    )

    assert result["overall_status"] == "pass"
    review = result["reviews"][0]
    assert review["missing_required_terms"] == []
    assert review["missing_required_term_groups"] == []
    assert review["required_term_groups"][0]["label"] == "indeterminate_resolution"
    assert review["required_term_groups"][0]["matched_terms"] == ["无法决定"]


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


def test_answer_contract_review_passes_for_srq07_runtime_spot_with_collected_topics_surface_alias() -> None:
    result = build_answer_contract_review(
        DEFAULT_FIXTURE,
        query_id="SRQ-07",
        answer_file=ROOT
        / "docs"
        / "runtime-evidence"
        / "2026-08-19-claude-code-srq-07-runtime-spot-answer.md",
    )

    assert result["overall_status"] == "pass"
    review = result["reviews"][0]
    assert review["missing_required_terms"] == []
    assert review["missing_required_term_groups"] == []
    assert review["required_term_groups"][0]["label"] == "collected_topics_surface"
    assert review["required_term_groups"][0]["matched_terms"] == ["总与别"]


def test_answer_contract_review_passes_for_collected_topics_definition_scope_sample() -> None:
    result = build_answer_contract_review(
        DEFAULT_FIXTURE,
        query_id="SRQ-11",
        sample_id="srq11-collected-topics-definition-scope-pass",
    )

    assert result["overall_status"] == "pass"
    assert result["expected_status"] == "pass"
    assert result["expected_status_match"] is True
    assert result["reviews"][0]["contract_id"] == "collected_topics_definition_scope_error"
    assert result["reviews"][0]["missing_required_terms"] == []
    assert result["reviews"][0]["missing_required_slots"] == []
    assert result["reviews"][0]["present_forbidden_terms"] == []


def test_answer_contract_review_srq11_runtime_spot_clears_heading_collision_but_keeps_boundary_fail() -> None:
    result = build_answer_contract_review(
        DEFAULT_FIXTURE,
        query_id="SRQ-11",
        answer_file=ROOT / "docs/runtime-evidence/2026-08-19-claude-code-srq-11-runtime-spot-answer.md",
    )

    assert result["overall_status"] == "fail"
    review = result["reviews"][0]
    assert review["present_forbidden_terms"] == []
    assert review["missing_required_terms"] == [
        "性相过宽",
        "唯在所表上成立",
        "违②",
    ]
    assert review["missing_required_slots"] == ["definiendum_boundary"]


def test_answer_contract_review_fails_for_collected_topics_definition_scope_negative_sample() -> None:
    result = build_answer_contract_review(
        DEFAULT_FIXTURE,
        query_id="SRQ-11",
        sample_id="srq11-collected-topics-definition-scope-fail",
    )

    assert result["overall_status"] == "fail"
    assert result["expected_status"] == "fail"
    assert result["expected_status_match"] is True
    assert "性相过宽" in result["reviews"][0]["missing_required_terms"]
    assert "唯在所表上成立" in result["reviews"][0]["missing_required_terms"]
    assert result["reviews"][0]["present_forbidden_terms"] == [
        "能盛水者就是瓶",
        "这个性相成立",
        "不需要反例",
    ]
    assert result["reviews"][0]["missing_required_slots"] == [
        "definiendum_boundary",
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


def test_answer_contract_review_passes_for_srq10_runtime_spot_after_cognitive_alias_calibration() -> None:
    result = build_answer_contract_review(
        DEFAULT_FIXTURE,
        query_id="SRQ-10",
        answer_file=ROOT / "docs/runtime-evidence/2026-08-19-claude-code-srq-10-runtime-spot-answer.md",
    )

    assert result["overall_status"] == "pass"
    review = result["reviews"][0]
    assert review["missing_required_terms"] == []
    assert review["missing_required_term_groups"] == []
    assert review["missing_required_slots"] == []
    assert review["present_forbidden_terms"] == []
    matched_by_label = {
        group["label"]: group["matched_terms"]
        for group in review["required_term_groups"]
    }
    assert matched_by_label["attribution_error_surface"] == ["错误地投射"]
    assert matched_by_label["motive_inference_surface"] == ["他人心相续里的动机", "间接推断"]
    assert matched_by_label["affliction_surface"] == ["厌烦", "反向攻击"]
    assert matched_by_label["non_harm_surface"] == ['不把对方固化成一个"敌人"标签']


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
    assert result["reviews"][0]["missing_required_term_groups"] == [
        "attribution_error_surface",
        "motive_inference_surface",
        "affliction_surface",
        "non_harm_surface",
    ]
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
