import json
import subprocess
import sys
from pathlib import Path

from semantic_retrieval_dry_run import DEFAULT_FIXTURE, FixtureError, build_dry_run

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "semantic_retrieval_dry_run.py"


def test_dry_run_returns_expected_chunks_for_query_fixture() -> None:
    result = build_dry_run(DEFAULT_FIXTURE, query_id="SRQ-01")

    assert result["mode"] == "fixture-dry-run"
    assert result["query_id"] == "SRQ-01"
    assert result["expected_chunk_ids"] == [
        "agama:T02n0099:juan-1:line-147",
        "agama:T01n0001:juan-1:line-881",
        "agama:T01n0001:juan-3:line-1829",
        "context:hetuvidya:trairupya",
        "reasoning:ZR-01:hetuvidya",
        "context:collected-topics:prasanga-runtime",
        "context:madhyamaka:prasanga-method",
    ]
    assert [chunk["chunk_id"] for chunk in result["chunks"]] == result["expected_chunk_ids"]
    assert result["non_chunk_needs"] == ["practice_boundary"]
    assert result["answer_boundary_contracts"]["practice_boundary"]["required_terms"] == ["边界", "不等于修证"]
    assert result["answer_boundary_samples"] == [
        {
            "id": "srq01-practice-boundary-pass",
            "file": "tests/fixtures/answers/srq01-practice-boundary-pass.md",
            "expected_status": "pass",
        },
        {
            "id": "srq01-practice-boundary-fail",
            "file": "tests/fixtures/answers/srq01-practice-boundary-fail.md",
            "expected_status": "fail",
        },
    ]
    assert all("source_file" in chunk for chunk in result["chunks"])
    assert all("citation" in chunk for chunk in result["chunks"])
    assert any("no embeddings" in item for item in result["limitations"])


def test_dry_run_can_limit_expected_chunks() -> None:
    result = build_dry_run(DEFAULT_FIXTURE, query_id="SRQ-01", limit=1)

    assert result["expected_chunk_ids"] == ["agama:T02n0099:juan-1:line-147"]
    assert len(result["chunks"]) == 1


def test_dry_run_returns_hetuvidya_error_fixture_for_srq02() -> None:
    result = build_dry_run(DEFAULT_FIXTURE, query_id="SRQ-02")

    assert result["query"] == "检验论式：声，应是可见，以是色形故。"
    assert result["needs"] == ["hetuvidya"]
    assert result["non_chunk_needs"] == []
    assert result["expected_chunk_ids"] == [
        "context:hetuvidya:trairupya",
        "reasoning:ZR-03:hetuvidya-error",
    ]
    assert [chunk["chunk_id"] for chunk in result["chunks"]] == result["expected_chunk_ids"]
    assert result["answer_contracts"]["hetuvidya_error_detection"]["required_terms"] == [
        "因不成",
        "遍是宗法性",
        "色形",
        "声",
        "不成立",
    ]
    assert result["answer_contracts"]["hetuvidya_error_detection"]["forbidden_terms"] == [
        "因三相完全满足",
        "正因成立",
    ]
    assert result["answer_contract_samples"] == [
        {
            "id": "srq02-hetuvidya-error-pass",
            "file": "tests/fixtures/answers/srq02-hetuvidya-error-pass.md",
            "expected_status": "pass",
        },
        {
            "id": "srq02-hetuvidya-error-fail",
            "file": "tests/fixtures/answers/srq02-hetuvidya-error-fail.md",
            "expected_status": "fail",
        },
    ]
    assert result["chunks"][1]["text"] == "检验论式：声，应是可见，以是色形故。"


def test_dry_run_returns_hetuvidya_non_pervasive_fixture_for_srq05() -> None:
    result = build_dry_run(DEFAULT_FIXTURE, query_id="SRQ-05")

    assert result["query"] == "检验论式：声，应是无常，以是所知故。"
    assert result["needs"] == ["hetuvidya"]
    assert result["non_chunk_needs"] == []
    assert result["expected_chunk_ids"] == [
        "context:hetuvidya:trairupya",
        "reasoning:ZR-07:hetuvidya-non-pervasive",
    ]
    assert [chunk["chunk_id"] for chunk in result["chunks"]] == result["expected_chunk_ids"]
    assert result["answer_contracts"]["hetuvidya_non_pervasive_detection"]["required_terms"] == [
        "不周遍",
        "遍是宗法性",
        "异品遍无性",
        "所知",
        "常法",
        "不成立",
    ]
    assert result["answer_contracts"]["hetuvidya_non_pervasive_detection"]["forbidden_terms"] == [
        "因三相完全满足",
        "正因成立",
        "第一相不成立",
    ]
    assert result["answer_contract_samples"] == [
        {
            "id": "srq05-hetuvidya-non-pervasive-pass",
            "file": "tests/fixtures/answers/srq05-hetuvidya-non-pervasive-pass.md",
            "expected_status": "pass",
        },
        {
            "id": "srq05-hetuvidya-non-pervasive-fail",
            "file": "tests/fixtures/answers/srq05-hetuvidya-non-pervasive-fail.md",
            "expected_status": "fail",
        },
    ]
    assert result["chunks"][1]["text"] == "检验论式：声，应是无常，以是所知故。"


def test_dry_run_returns_hetuvidya_indeterminate_fixture_for_srq06() -> None:
    result = build_dry_run(DEFAULT_FIXTURE, query_id="SRQ-06")

    assert result["query"] == "检验论式：声，应是常，以是所知故。"
    assert result["needs"] == ["hetuvidya"]
    assert result["non_chunk_needs"] == []
    assert result["expected_chunk_ids"] == [
        "context:hetuvidya:trairupya",
        "reasoning:ZR-08:hetuvidya-indeterminate",
    ]
    assert [chunk["chunk_id"] for chunk in result["chunks"]] == result["expected_chunk_ids"]
    assert result["answer_contracts"]["hetuvidya_indeterminate_detection"]["required_terms"] == [
        "不定因",
        "遍是宗法性",
        "同品定有性",
        "异品遍无性",
        "所知",
        "常法",
        "无常法",
        "不能决定",
    ]
    assert result["answer_contracts"]["hetuvidya_indeterminate_detection"]["forbidden_terms"] == [
        "因三相完全满足",
        "正因成立",
        "相违因",
    ]
    assert result["answer_contract_samples"] == [
        {
            "id": "srq06-hetuvidya-indeterminate-pass",
            "file": "tests/fixtures/answers/srq06-hetuvidya-indeterminate-pass.md",
            "expected_status": "pass",
        },
        {
            "id": "srq06-hetuvidya-indeterminate-fail",
            "file": "tests/fixtures/answers/srq06-hetuvidya-indeterminate-fail.md",
            "expected_status": "fail",
        },
    ]
    assert result["chunks"][1]["text"] == "检验论式：声，应是常，以是所知故。"


def test_dry_run_returns_collected_topics_total_part_fixture_for_srq07() -> None:
    result = build_dry_run(DEFAULT_FIXTURE, query_id="SRQ-07")

    assert result["query"] == "用摄类学检验命题：这份报告有三处问题，所以我这个人没有价值。"
    assert result["needs"] == ["collected_topics"]
    assert result["non_chunk_needs"] == []
    assert result["expected_chunk_ids"] == [
        "context:collected-topics:total-part",
        "argument:work-feedback:non-pervasive",
    ]
    assert [chunk["chunk_id"] for chunk in result["chunks"]] == result["expected_chunk_ids"]
    assert result["answer_contracts"]["collected_topics_total_part_error"]["required_terms"] == [
        "摄类学",
        "总与别",
        "别法",
        "总法",
        "不周遍",
        "报告",
        "我这个人",
        "不成立",
    ]
    assert result["answer_contracts"]["collected_topics_total_part_error"]["forbidden_terms"] == [
        "所以我没有价值",
        "可以直接推出",
        "不需区分总别",
    ]
    assert result["answer_contract_samples"] == [
        {
            "id": "srq07-collected-topics-total-part-pass",
            "file": "tests/fixtures/answers/srq07-collected-topics-total-part-pass.md",
            "expected_status": "pass",
        },
        {
            "id": "srq07-collected-topics-total-part-fail",
            "file": "tests/fixtures/answers/srq07-collected-topics-total-part-fail.md",
            "expected_status": "fail",
        },
    ]
    assert result["chunks"][0]["text"] == "总与别 —— 继承/子类关系"
    assert result["chunks"][1]["text"] == "被批评者"


def test_dry_run_returns_madhyamaka_prasanga_fixture_for_srq03() -> None:
    result = build_dry_run(DEFAULT_FIXTURE, query_id="SRQ-03")

    assert result["query"] == "若有人承许诸法自性有，如何用应成法指出矛盾？"
    assert result["needs"] == ["madhyamaka_prasanga"]
    assert result["non_chunk_needs"] == []
    assert result["expected_chunk_ids"] == [
        "context:madhyamaka:prasanga-method",
        "reasoning:ZR-04:madhyamaka-prasanga",
    ]
    assert [chunk["chunk_id"] for chunk in result["chunks"]] == result["expected_chunk_ids"]
    assert result["answer_contracts"]["madhyamaka_prasanga_boundary"]["required_terms"] == [
        "对方承许",
        "归谬",
        "自性有",
        "缘起",
        "矛盾",
        "不立自宗",
    ]
    assert result["answer_contracts"]["madhyamaka_prasanga_boundary"]["forbidden_terms"] == [
        "我方建立自宗",
        "证明诸法绝对不存在",
        "断灭",
    ]
    assert result["answer_contract_samples"] == [
        {
            "id": "srq03-madhyamaka-prasanga-pass",
            "file": "tests/fixtures/answers/srq03-madhyamaka-prasanga-pass.md",
            "expected_status": "pass",
        },
        {
            "id": "srq03-madhyamaka-prasanga-fail",
            "file": "tests/fixtures/answers/srq03-madhyamaka-prasanga-fail.md",
            "expected_status": "fail",
        },
    ]
    assert result["chunks"][1]["text"] == "若有人承许诸法自性有，如何用应成法指出矛盾？"


def test_dry_run_returns_agama_citation_boundary_fixture_for_srq04() -> None:
    result = build_dry_run(DEFAULT_FIXTURE, query_id="SRQ-04")

    assert result["query"] == "查四阿含中关于无我的经文，并说明检索范围与待校勘边界。"
    assert result["needs"] == ["agama_evidence"]
    assert result["non_chunk_needs"] == []
    assert result["expected_chunk_ids"] == [
        "agama:T02n0099:juan-1:line-147",
        "agama:T01n0001:juan-1:line-881",
        "agama:T01n0001:juan-3:line-1829",
        "reasoning:ZR-05:agama-evidence",
    ]
    assert [chunk["chunk_id"] for chunk in result["chunks"]] == result["expected_chunk_ids"]
    assert result["answer_contracts"]["agama_citation_boundary"]["required_terms"] == [
        "CBETA",
        "T02n0099",
        "context/agama/",
        "检索范围",
        "代表性",
        "待校勘",
    ]
    assert result["answer_contracts"]["agama_citation_boundary"]["forbidden_terms"] == [
        "已穷尽",
        "无需校勘",
        "可作为定本",
        "校勘完成",
        "校勘确认",
    ]
    assert result["answer_contract_samples"] == [
        {
            "id": "srq04-agama-citation-boundary-pass",
            "file": "tests/fixtures/answers/srq04-agama-citation-boundary-pass.md",
            "expected_status": "pass",
        },
        {
            "id": "srq04-agama-citation-boundary-fail",
            "file": "tests/fixtures/answers/srq04-agama-citation-boundary-fail.md",
            "expected_status": "fail",
        },
    ]
    assert result["chunks"][3]["text"] == "查四阿含中关于无我的经文，并说明检索范围与待校勘边界。"


def test_dry_run_unknown_query_id_is_reported() -> None:
    try:
        build_dry_run(DEFAULT_FIXTURE, query_id="SRQ-99")
    except FixtureError as exc:
        assert "Unknown query id: SRQ-99" in str(exc)
    else:
        raise AssertionError("unknown query id should fail")


def test_dry_run_rejects_unknown_chunk_references(tmp_path: Path) -> None:
    fixture = tmp_path / "semantic_chunks.yaml"
    fixture.write_text(
        """version: 1
source: test
purpose: test
chunks:
  - chunk_id: chunk-1
    chunk_type: context_topic
    source_file: context/sample.md
    start_line: 1
    end_line: 1
    citation: "context/sample.md:1"
    passage_citation: "context/sample.md:1"
    text: sample
    metadata:
      topics:
        - sample
      reasoning_roles:
        - hetuvidya
queries:
  - id: SRQ-01
    query: sample
    expected_chunk_ids:
      - missing-chunk
""",
        encoding="utf-8",
    )

    try:
        build_dry_run(fixture, query_id="SRQ-01")
    except FixtureError as exc:
        assert "references unknown chunks" in str(exc)
    else:
        raise AssertionError("unknown chunk references should fail")


def test_dry_run_cli_json_output_is_machine_readable() -> None:
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--query-id", "SRQ-01", "--json"],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=True,
    )
    data = json.loads(result.stdout)

    assert data["mode"] == "fixture-dry-run"
    assert data["query_id"] == "SRQ-01"
    assert len(data["chunks"]) == 7
