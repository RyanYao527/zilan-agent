import json
import subprocess
import sys
from pathlib import Path

from cognitive_analysis_mapper import (
    DEFAULT_CASES,
    CognitiveAnalysisMapperError,
    build_cognitive_analysis_mapping,
)

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "cognitive_analysis_mapper.py"


def test_cognitive_analysis_mapper_returns_caregiving_case() -> None:
    result = build_cognitive_analysis_mapping(DEFAULT_CASES, case_id="ZR-11")
    mapping = result["mappings"][0]
    cognitive = mapping["cognitive_analysis"]

    assert result["status"] == "run"
    assert result["validator"] == "cognitive_analysis_mapper"
    assert result["contract_family"] == "cognitive_analysis"
    assert result["mode"] == "cognitive-analysis-mapper-v0"
    assert result["output_schema"] == "cognitive-analysis-mapper-output-v0"
    assert result["source"] == "tests/reasoning_cases.yaml"
    assert result["case_ids"] == ["ZR-11"]
    assert result["count"] == 1
    assert mapping["case_id"] == "ZR-11"
    assert mapping["source_regression_cases"] == ["ZC-01", "ZC-03"]
    assert mapping["boundary_statement_required"] is True
    assert cognitive["chain"] == ["触", "作意", "受", "想", "思"]
    assert [item["role"] for item in cognitive["chain_steps"]] == [
        "input_contact",
        "attention_orientation",
        "feeling_tone",
        "classification_labeling",
        "volitional_response",
    ]
    assert [item["term"] for item in cognitive["afflictions"]] == ["瞋", "忿", "恼"]
    assert [item["term"] for item in cognitive["corrective_factors"]] == ["念", "慧", "无瞋", "不害"]
    assert cognitive["practice_boundary"] == {"required": True, "status": "required"}
    assert mapping["diagnostics"] == [
        {
            "code": "practice_boundary_required",
            "severity": "info",
            "message": "The fixture requires explicit practice-boundary language.",
        }
    ]


def test_cognitive_analysis_mapper_returns_all_cognitive_cases_by_default() -> None:
    result = build_cognitive_analysis_mapping(DEFAULT_CASES)

    assert [item["case_id"] for item in result["mappings"]] == ["ZR-02", "ZR-06", "ZR-10", "ZR-11"]
    assert all(item["cognitive_analysis"]["chain"] == ["触", "作意", "受", "想", "思"] for item in result["mappings"])
    assert any("structured tests/reasoning_cases.yaml" in item for item in result["limitations"])


def test_cognitive_analysis_mapper_rejects_non_cognitive_case() -> None:
    try:
        build_cognitive_analysis_mapping(DEFAULT_CASES, case_id="ZR-04")
    except CognitiveAnalysisMapperError as exc:
        assert "ZR-04 is not a cognitive-analysis reasoning case" in str(exc)
    else:
        raise AssertionError("non-cognitive case should fail")


def test_cognitive_analysis_mapper_cli_json_output_is_machine_readable() -> None:
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--case-id", "ZR-10", "--json"],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=True,
    )
    data = json.loads(result.stdout)
    mapping = data["mappings"][0]

    assert data["mode"] == "cognitive-analysis-mapper-v0"
    assert data["output_schema"] == "cognitive-analysis-mapper-output-v0"
    assert data["count"] == 1
    assert mapping["case_id"] == "ZR-10"
    assert mapping["cognitive_analysis"]["chain_steps"][0] == {
        "term": "触",
        "id": "contact",
        "role": "input_contact",
        "description": "Root, object, and consciousness come into contact.",
        "status": "mapped",
    }
    assert mapping["cognitive_analysis"]["practice_boundary"]["status"] == "required"