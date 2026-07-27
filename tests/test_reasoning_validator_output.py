from __future__ import annotations

import reasoning_validator_output as compatibility_output
from zilanlib.reasoning.validator_output import (
    build_not_applicable_validator_output,
    build_validator_output,
    case_ids_from_items,
)


def test_case_ids_from_items_keeps_stable_unique_order() -> None:
    assert case_ids_from_items([
        {"case_id": "ZR-07"},
        {"case_id": "ZR-07"},
        {"case_id": "ZR-08"},
        {"case_id": None},
    ]) == ["ZR-07", "ZR-08"]


def test_build_validator_output_adds_common_envelope_fields() -> None:
    result = build_validator_output(
        validator="hetuvidya_validator",
        contract_family="hetuvidya",
        mode="hetuvidya-validator-v0",
        output_schema="hetuvidya-validator-output-v0.1",
        source="tests/reasoning_cases.yaml",
        case_id="ZR-07",
        payload_key="validations",
        payload=[{"case_id": "ZR-07", "result": "non_pervasive"}],
        limitations=("fixture only",),
    )

    assert result == {
        "status": "run",
        "validator": "hetuvidya_validator",
        "contract_family": "hetuvidya",
        "mode": "hetuvidya-validator-v0",
        "output_schema": "hetuvidya-validator-output-v0.1",
        "source": "tests/reasoning_cases.yaml",
        "case_id": "ZR-07",
        "case_ids": ["ZR-07"],
        "count": 1,
        "validations": [{"case_id": "ZR-07", "result": "non_pervasive"}],
        "limitations": ["fixture only"],
    }


def test_build_not_applicable_validator_output_uses_same_common_fields() -> None:
    result = build_not_applicable_validator_output(
        validator="madhyamaka_critique_engine",
        contract_family="madhyamaka_prasanga",
        output_schema="madhyamaka-critique-engine-output-v0",
        source="tests/reasoning_cases.yaml",
        payload_key="critiques",
        limitation="No selected Madhyamaka case.",
    )

    assert result == {
        "status": "not_applicable",
        "validator": "madhyamaka_critique_engine",
        "contract_family": "madhyamaka_prasanga",
        "output_schema": "madhyamaka-critique-engine-output-v0",
        "source": "tests/reasoning_cases.yaml",
        "case_ids": [],
        "critiques": [],
        "limitations": ["No selected Madhyamaka case."],
    }

def test_root_compatibility_shim_exports_shared_functions() -> None:
    assert compatibility_output.case_ids_from_items is case_ids_from_items
    assert compatibility_output.build_validator_output is build_validator_output
    assert compatibility_output.build_not_applicable_validator_output is build_not_applicable_validator_output
