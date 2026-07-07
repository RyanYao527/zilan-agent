import json
import subprocess
import sys
from pathlib import Path

from collected_topics_analyzer import (
    CollectedTopicsAnalyzerError,
    build_collected_topics_analysis,
)

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "collected_topics_analyzer.py"


def test_collected_topics_analyzer_maps_zr02_total_part_error() -> None:
    result = build_collected_topics_analysis(case_id="ZR-02")

    assert result["mode"] == "collected-topics-analyzer-v0"
    assert result["output_schema"] == "collected-topics-analyzer-output-v0"
    assert result["case_id"] == "ZR-02"
    assert result["count"] == 1

    analysis = result["analyses"][0]
    assert analysis["case_id"] == "ZR-02"
    assert [concept["role"] for concept in analysis["collected_topics"]["concepts"]] == [
        "concept",
        "concept",
    ]
    relation_checks = {
        item["id"]: item["status"] for item in analysis["collected_topics"]["relation_checks"]
    }
    assert relation_checks == {
        "pervasion": "fail",
        "total_part_distinction": "required",
    }
    assert analysis["boundary_statement_required"] is True
    assert {item["code"] for item in analysis["diagnostics"]} == {
        "non_pervasive",
        "total_part_boundary_required",
        "boundary_statement_required",
    }


def test_collected_topics_analyzer_defaults_to_collected_topics_cases() -> None:
    result = build_collected_topics_analysis()

    assert [item["case_id"] for item in result["analyses"]] == ["ZR-02", "ZR-06"]
    assert result["count"] == 2


def test_collected_topics_analyzer_rejects_non_collected_topics_case() -> None:
    try:
        build_collected_topics_analysis(case_id="ZR-03")
    except CollectedTopicsAnalyzerError as exc:
        assert "not a Collected Topics reasoning case" in str(exc)
    else:
        raise AssertionError("non-collected-topics case should fail")


def test_collected_topics_analyzer_cli_json_output_is_machine_readable() -> None:
    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--case-id",
            "ZR-02",
            "--json",
        ],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=True,
    )
    data = json.loads(result.stdout)

    assert data["mode"] == "collected-topics-analyzer-v0"
    assert data["case_id"] == "ZR-02"
    assert data["analyses"][0]["collected_topics"]["relation_checks"][0]["id"] == "pervasion"
