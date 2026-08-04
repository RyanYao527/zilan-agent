from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path
from typing import Any

import yaml

from zilan_contract import AnswerContractResult, AnswerContractRunner


def _load_contracts(path: Path) -> dict[str, object]:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise ValueError(f"Contract file contains invalid YAML: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError("Contract file must contain a top-level contracts mapping.")
    contracts = data.get("contracts")
    if not isinstance(contracts, dict):
        raise ValueError("Contract file must contain a top-level contracts mapping.")
    return _string_key_mapping(contracts)


def _string_key_mapping(value: dict[Any, Any]) -> dict[str, object]:
    return {str(key): item for key, item in value.items()}


def _json_payload(result: AnswerContractResult) -> dict[str, object]:
    payload = result.to_summary()
    payload["issues"] = [asdict(issue) for issue in result.issues()]
    return payload


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="zilan-contract")
    subparsers = parser.add_subparsers(dest="command", required=True)
    check = subparsers.add_parser("check")
    check.add_argument("--contract-file", type=Path, required=True)
    check.add_argument("--answer-file", type=Path, required=True)
    output = check.add_mutually_exclusive_group()
    output.add_argument("--json", action="store_true")
    output.add_argument("--markdown", action="store_true")
    args = parser.parse_args(argv)

    try:
        contracts = _load_contracts(args.contract_file)
        result = AnswerContractRunner().check_file(answer_file=args.answer_file, contracts=contracts)
    except (OSError, ValueError) as exc:
        parser.exit(2, f"zilan-contract failed: {exc}\n")

    if args.json:
        print(json.dumps(_json_payload(result), ensure_ascii=False, indent=2))
    else:
        print(result.to_markdown(), end="")
    return 0 if result.passed() else 1


if __name__ == "__main__":
    raise SystemExit(main())
