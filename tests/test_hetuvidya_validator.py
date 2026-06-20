import json
import subprocess
import sys
from pathlib import Path

from hetuvidya_validator import DEFAULT_CASES, HetuvidyaValidatorError, build_hetuvidya_validation

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "hetuvidya_validator.py"


def test_hetuvidya_validator_returns_reason_unestablished_case() -> None:
    result = build_hetuvidya_validation(DEFAULT_CASES, case_id="ZR-03")
    validation = result["validations"][0]

    assert result["mode"] == "hetuvidya-validator-v0"
    assert result["source"] == "tests/reasoning_cases.yaml"
    assert result["count"] == 1
    assert validation["case_id"] == "ZR-03"
    assert validation["classification"] == "因不成"
    assert validation["argument"] == {
        "subject": "声",
        "predicate": "可见",
        "reason": "色形",
    }
    assert validation["checks"] == {
        "paksa_dharmata": "fail",
        "sapaksa_sattva": "not_applicable",
        "vipaksa_asattva": "not_applicable",
    }


def test_hetuvidya_validator_returns_all_hetuvidya_cases_by_default() -> None:
    result = build_hetuvidya_validation(DEFAULT_CASES)

    case_ids = [item["case_id"] for item in result["validations"]]
    assert case_ids == ["ZR-01", "ZR-03", "ZR-06", "ZR-07", "ZR-08"]
    assert [item["classification"] for item in result["validations"]] == [
        "正因成立",
        "因不成",
        "边界性推理，不作三相实判",
        "不周遍",
        "不定因或相违因需进一步判别",
    ]
    assert any("structured tests/reasoning_cases.yaml" in item for item in result["limitations"])


def test_hetuvidya_validator_rejects_non_hetuvidya_case() -> None:
    try:
        build_hetuvidya_validation(DEFAULT_CASES, case_id="ZR-04")
    except HetuvidyaValidatorError as exc:
        assert "ZR-04 is not a Hetuvidya reasoning case" in str(exc)
    else:
        raise AssertionError("non-Hetuvidya case should fail")


def test_hetuvidya_validator_cli_json_output_is_machine_readable() -> None:
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--case-id", "ZR-07", "--json"],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=True,
    )
    data = json.loads(result.stdout)

    assert data["mode"] == "hetuvidya-validator-v0"
    assert data["count"] == 1
    assert data["validations"][0]["case_id"] == "ZR-07"
    assert data["validations"][0]["classification"] == "不周遍"
