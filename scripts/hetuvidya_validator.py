from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from reasoning_validator_output import build_validator_output
from zilanlib.yaml_io import display_path, load_yaml_mapping

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CASES = ROOT / "tests" / "reasoning_cases.yaml"
VALIDATOR = "hetuvidya_validator"
CONTRACT_FAMILY = "hetuvidya"
MODE = "hetuvidya-validator-v0"
OUTPUT_SCHEMA = "hetuvidya-validator-output-v0.1"
LIMITATIONS = (
    "Prototype reads structured tests/reasoning_cases.yaml fixtures only.",
    "No natural-language argument parsing, provider calls, prompt changes, or doctrinal grading.",
)

RESULT_LABELS = {
    "positive_reason": "正因成立",
    "reason_unestablished": "因不成",
    "non_pervasive": "不周遍",
    "inconclusive_or_contradictory": "不定因或相违因需进一步判别",
    "boundary_only": "边界性推理，不作三相实判",
}

RESULT_STATUSES = {
    "positive_reason": "valid",
    "reason_unestablished": "invalid",
    "non_pervasive": "invalid",
    "inconclusive_or_contradictory": "indeterminate",
    "boundary_only": "boundary",
}

RESULT_SUMMARIES = {
    "positive_reason": "All three reason marks are declared as satisfied in the fixture.",
    "reason_unestablished": "The reason is not established on the subject, so the first reason mark fails.",
    "non_pervasive": "The reason is established on the subject but fails the opposite-side pervasion check.",
    "inconclusive_or_contradictory": "The reason cannot decide the thesis without further classification.",
    "boundary_only": "The fixture records a boundary case and does not claim a full trairupya adjudication.",
}

CHECK_DEFINITIONS = {
    "paksa_dharmata": {
        "name": "遍是宗法性",
        "role": "subject_reason_relation",
        "description": "The reason must be established on the subject.",
    },
    "sapaksa_sattva": {
        "name": "同品定有性",
        "role": "same_side_presence",
        "description": "The reason must be present in at least one same-side case.",
    },
    "vipaksa_asattva": {
        "name": "异品遍无性",
        "role": "opposite_side_absence",
        "description": "The reason must be absent from opposite-side cases.",
    },
}

CHECK_STATUS_LABELS = {
    "pass": "passes",
    "fail": "fails",
    "boundary": "boundary",
    "not_applicable": "not applicable",
}

DIAGNOSTIC_MESSAGES = {
    "positive_reason": [],
    "reason_unestablished": [
        {
            "code": "reason_unestablished",
            "severity": "error",
            "check_id": "paksa_dharmata",
            "message": "The reason is not established on the subject.",
        }
    ],
    "non_pervasive": [
        {
            "code": "non_pervasive",
            "severity": "error",
            "check_id": "vipaksa_asattva",
            "message": "The reason is not pervaded by the predicate because the opposite-side check fails.",
        }
    ],
    "inconclusive_or_contradictory": [
        {
            "code": "inconclusive_or_contradictory",
            "severity": "warning",
            "check_id": "vipaksa_asattva",
            "message": "The reason occurs where it cannot decide the thesis without further classification.",
        }
    ],
    "boundary_only": [
        {
            "code": "boundary_only",
            "severity": "info",
            "check_id": None,
            "message": "This case requires boundary language rather than a full three-mark adjudication.",
        }
    ],
}


class HetuvidyaValidatorError(ValueError):
    """Raised when the structured Hetuvidya fixture cannot be validated."""


def _display_path(path: Path) -> str:
    return display_path(path, root=ROOT)


def _load_yaml(path: Path) -> dict[str, Any]:
    return load_yaml_mapping(
        path,
        root=ROOT,
        error_type=HetuvidyaValidatorError,
        missing_message="PyYAML is required to read reasoning cases.",
        missing_file_label="Reasoning cases not found",
        parse_label="Failed to parse reasoning cases",
        mapping_label="Reasoning cases must be a mapping",
    )


def _case_list(data: dict[str, Any]) -> list[dict[str, Any]]:
    cases = data.get("cases")
    if not isinstance(cases, list) or not cases:
        raise HetuvidyaValidatorError("Reasoning cases must contain a non-empty cases list.")
    if not all(isinstance(item, dict) for item in cases):
        raise HetuvidyaValidatorError("Every reasoning case must be a mapping.")
    return cases


def _select_cases(cases: list[dict[str, Any]], case_id: str | None) -> list[dict[str, Any]]:
    if case_id is None:
        return [case for case in cases if "hetuvidya" in case.get("contracts", [])]

    for case in cases:
        if case.get("id") == case_id:
            return [case]
    raise HetuvidyaValidatorError(f"Unknown reasoning case id: {case_id}")


def _structured_check(check_id: str, status: Any) -> dict[str, Any]:
    definition = CHECK_DEFINITIONS[check_id]
    status_text = status if isinstance(status, str) else "unknown"
    return {
        "id": check_id,
        "name": definition["name"],
        "role": definition["role"],
        "status": status_text,
        "status_label": CHECK_STATUS_LABELS.get(status_text, "unknown"),
        "description": definition["description"],
    }


def _structured_judgment(result: str, checks: dict[str, Any], *, boundary_required: bool) -> dict[str, Any]:
    failed_checks = [check_id for check_id, status in checks.items() if status == "fail"]
    boundary_checks = [check_id for check_id, status in checks.items() if status == "boundary"]
    return {
        "result": result,
        "status": RESULT_STATUSES.get(result, "unknown"),
        "label": RESULT_LABELS.get(result, "未知判定"),
        "summary": RESULT_SUMMARIES.get(result, "The fixture result is not recognized by this validator."),
        "failed_checks": failed_checks,
        "boundary_checks": boundary_checks,
        "boundary_statement_required": boundary_required,
    }


def _validate_case(case: dict[str, Any]) -> dict[str, Any]:
    case_id = case.get("id")
    expected = case.get("expected")
    if not isinstance(case_id, str) or not case_id:
        raise HetuvidyaValidatorError("Every selected reasoning case must have a non-empty id.")
    if not isinstance(expected, dict):
        raise HetuvidyaValidatorError(f"{case_id} expected must be a mapping.")

    hetuvidya = expected.get("hetuvidya")
    if not isinstance(hetuvidya, dict):
        raise HetuvidyaValidatorError(f"{case_id} expected.hetuvidya must be a mapping.")

    checks = hetuvidya.get("checks")
    if not isinstance(checks, dict):
        raise HetuvidyaValidatorError(f"{case_id} expected.hetuvidya.checks must be a mapping.")

    result = hetuvidya.get("result")
    if not isinstance(result, str) or not result:
        raise HetuvidyaValidatorError(f"{case_id} expected.hetuvidya.result must be a non-empty string.")

    normalized_checks = {
        "paksa_dharmata": checks.get("paksa_dharmata"),
        "sapaksa_sattva": checks.get("sapaksa_sattva"),
        "vipaksa_asattva": checks.get("vipaksa_asattva"),
    }
    boundary_required = bool(expected.get("boundary_statement", False))

    return {
        "case_id": case_id,
        "title": case.get("title", ""),
        "prompt": case.get("prompt", ""),
        "argument": {
            "subject": hetuvidya.get("subject"),
            "predicate": hetuvidya.get("predicate"),
            "reason": hetuvidya.get("reason"),
        },
        "checks": normalized_checks,
        "trairupya_checks": [
            _structured_check("paksa_dharmata", normalized_checks["paksa_dharmata"]),
            _structured_check("sapaksa_sattva", normalized_checks["sapaksa_sattva"]),
            _structured_check("vipaksa_asattva", normalized_checks["vipaksa_asattva"]),
        ],
        "result": result,
        "classification": RESULT_LABELS.get(result, "未知判定"),
        "judgment": _structured_judgment(result, normalized_checks, boundary_required=boundary_required),
        "diagnostics": DIAGNOSTIC_MESSAGES.get(result, []),
        "boundary_statement_required": boundary_required,
    }


def build_hetuvidya_validation(cases_path: Path = DEFAULT_CASES, *, case_id: str | None = None) -> dict[str, Any]:
    """Return structured Hetuvidya validation results from checked-in reasoning cases."""

    data = _load_yaml(cases_path)
    selected = _select_cases(_case_list(data), case_id)
    if case_id is not None and "hetuvidya" not in selected[0].get("contracts", []):
        raise HetuvidyaValidatorError(f"{case_id} is not a Hetuvidya reasoning case.")

    validations = [_validate_case(case) for case in selected]

    return build_validator_output(
        validator=VALIDATOR,
        contract_family=CONTRACT_FAMILY,
        mode=MODE,
        output_schema=OUTPUT_SCHEMA,
        source=_display_path(cases_path),
        case_id=case_id,
        payload_key="validations",
        payload=validations,
        limitations=LIMITATIONS,
    )


def _print_text(result: dict[str, Any]) -> None:
    print(f"mode: {result['mode']}")
    print(f"source: {result['source']}")
    for item in result["validations"]:
        argument = item["argument"]
        checks = item["checks"]
        judgment = item["judgment"]
        print("")
        print(f"{item['case_id']}: {item['classification']}")
        print(f"  prompt: {item['prompt']}")
        print(f"  argument: 有法={argument['subject']} / 所立法={argument['predicate']} / 因={argument['reason']}")
        print(f"  judgment: {judgment['status']} / {judgment['result']}")
        print(
            "  checks: "
            f"遍是宗法性={checks['paksa_dharmata']}, "
            f"同品定有性={checks['sapaksa_sattva']}, "
            f"异品遍无性={checks['vipaksa_asattva']}"
        )
        if item["diagnostics"]:
            print("  diagnostics:")
            for diagnostic in item["diagnostics"]:
                print(f"  - {diagnostic['code']}: {diagnostic['message']}")
    print("")
    print("limitations:")
    for item in result["limitations"]:
        print(f"- {item}")


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        description="Validate structured Hetuvidya reasoning cases from tests/reasoning_cases.yaml."
    )
    parser.add_argument("--cases", type=Path, default=DEFAULT_CASES, help="Reasoning cases YAML path.")
    parser.add_argument("--case-id", help="Reasoning case id, such as ZR-03.")
    parser.add_argument("--json", action="store_true", dest="json_output", help="Emit machine-readable JSON.")
    args = parser.parse_args()

    try:
        result = build_hetuvidya_validation(args.cases, case_id=args.case_id)
    except HetuvidyaValidatorError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    if args.json_output:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        _print_text(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
