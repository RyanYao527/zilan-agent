import json
import subprocess
import sys
from pathlib import Path

from madhyamaka_critique_engine import (
    MadhyamakaCritiqueEngineError,
    build_madhyamaka_critique,
)

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "madhyamaka_critique_engine.py"


def test_madhyamaka_critique_engine_maps_zr09_nihilism_boundary() -> None:
    result = build_madhyamaka_critique(case_id="ZR-09")

    assert result["mode"] == "madhyamaka-critique-engine-v0"
    assert result["output_schema"] == "madhyamaka-critique-engine-output-v0"
    assert result["case_id"] == "ZR-09"
    assert result["count"] == 1

    critique = result["critiques"][0]
    assert critique["case_id"] == "ZR-09"
    madhyamaka = critique["madhyamaka_prasanga"]
    assert madhyamaka["opponent_premise"]
    assert len(madhyamaka["accepted_commitments"]) == 2
    assert len(madhyamaka["contradictions"]) == 2
    assert madhyamaka["no_independent_thesis"] == {
        "required": True,
        "status": "required",
    }
    assert [item["id"] for item in madhyamaka["critique_steps"]] == [
        "opponent_premise",
        "accepted_commitments",
        "contradiction",
        "no_independent_thesis",
    ]
    assert {item["code"] for item in critique["diagnostics"]} == {
        "no_independent_thesis_required",
        "boundary_statement_required",
    }


def test_madhyamaka_critique_engine_defaults_to_madhyamaka_cases() -> None:
    result = build_madhyamaka_critique()

    assert [item["case_id"] for item in result["critiques"]] == ["ZR-04", "ZR-06", "ZR-09"]
    assert result["count"] == 3


def test_madhyamaka_critique_engine_rejects_non_madhyamaka_case() -> None:
    try:
        build_madhyamaka_critique(case_id="ZR-02")
    except MadhyamakaCritiqueEngineError as exc:
        assert "not a Madhyamaka prasaṅga reasoning case" in str(exc)
    else:
        raise AssertionError("non-Madhyamaka case should fail")


def test_madhyamaka_critique_engine_cli_json_output_is_machine_readable() -> None:
    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--case-id",
            "ZR-09",
            "--json",
        ],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=True,
    )
    data = json.loads(result.stdout)

    assert data["mode"] == "madhyamaka-critique-engine-v0"
    assert data["case_id"] == "ZR-09"
    assert data["critiques"][0]["madhyamaka_prasanga"]["no_independent_thesis"]["status"] == "required"
