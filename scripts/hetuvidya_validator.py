from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from zilanlib.reasoning.hetuvidya_validator import (
    DEFAULT_CASES,
    HetuvidyaValidatorError,
    build_hetuvidya_validation,
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
