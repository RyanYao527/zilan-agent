from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CASES = ROOT / "tests" / "reasoning_cases.yaml"
MODE = "hetuvidya-validator-v0"
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


class HetuvidyaValidatorError(ValueError):
    """Raised when the structured Hetuvidya fixture cannot be validated."""


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise HetuvidyaValidatorError(f"Reasoning cases not found: {_display_path(path)}")

    try:
        import yaml  # type: ignore[import-not-found]
    except ModuleNotFoundError as exc:
        raise HetuvidyaValidatorError("PyYAML is required to read reasoning cases.") from exc

    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001 - keep parser failures visible in CLI output.
        raise HetuvidyaValidatorError(f"Failed to parse reasoning cases {_display_path(path)}: {exc}") from exc

    if not isinstance(data, dict):
        raise HetuvidyaValidatorError(f"Reasoning cases must be a mapping: {_display_path(path)}")
    return data


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

    return {
        "case_id": case_id,
        "title": case.get("title", ""),
        "prompt": case.get("prompt", ""),
        "argument": {
            "subject": hetuvidya.get("subject"),
            "predicate": hetuvidya.get("predicate"),
            "reason": hetuvidya.get("reason"),
        },
        "checks": {
            "paksa_dharmata": checks.get("paksa_dharmata"),
            "sapaksa_sattva": checks.get("sapaksa_sattva"),
            "vipaksa_asattva": checks.get("vipaksa_asattva"),
        },
        "result": result,
        "classification": RESULT_LABELS.get(result, "未知判定"),
        "boundary_statement_required": expected.get("boundary_statement", False),
    }


def build_hetuvidya_validation(cases_path: Path = DEFAULT_CASES, *, case_id: str | None = None) -> dict[str, Any]:
    """Return structured Hetuvidya validation results from checked-in reasoning cases."""

    data = _load_yaml(cases_path)
    selected = _select_cases(_case_list(data), case_id)
    if case_id is not None and "hetuvidya" not in selected[0].get("contracts", []):
        raise HetuvidyaValidatorError(f"{case_id} is not a Hetuvidya reasoning case.")

    validations = [_validate_case(case) for case in selected]

    return {
        "mode": MODE,
        "source": _display_path(cases_path),
        "case_id": case_id,
        "count": len(validations),
        "validations": validations,
        "limitations": list(LIMITATIONS),
    }


def _print_text(result: dict[str, Any]) -> None:
    print(f"mode: {result['mode']}")
    print(f"source: {result['source']}")
    for item in result["validations"]:
        argument = item["argument"]
        checks = item["checks"]
        print("")
        print(f"{item['case_id']}: {item['classification']}")
        print(f"  prompt: {item['prompt']}")
        print(f"  argument: 有法={argument['subject']} / 所立法={argument['predicate']} / 因={argument['reason']}")
        print(
            "  checks: "
            f"遍是宗法性={checks['paksa_dharmata']}, "
            f"同品定有性={checks['sapaksa_sattva']}, "
            f"异品遍无性={checks['vipaksa_asattva']}"
        )
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
