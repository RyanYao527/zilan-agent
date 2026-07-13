from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from zilanlib.reasoning.agama_evidence_checker import (
    DEFAULT_CASES,
    DEFAULT_RETRIEVAL_FIXTURE,
    AgamaEvidenceCheckerError,
    build_agama_evidence_check,
)


def _render_text(result: dict[str, Any]) -> str:
    lines = [
        f"mode: {result['mode']}",
        f"source: {result['source']}",
    ]
    for item in result["evidence_reviews"]:
        evidence = item["agama_evidence"]
        lines.extend(
            [
                "",
                f"{item['case_id']}: {item['title']}",
                f"  prompt: {item['prompt']}",
                f"  citation_required: {evidence['citation_required']['status']}",
                f"  search_scope: {evidence['search_scope']['scope']}",
                f"  collation_boundary: {evidence['collation_boundary']['status']}",
                f"  local_evidence: {evidence['local_evidence']['status']}",
            ]
        )
        if item["diagnostics"]:
            lines.append("  diagnostics:")
            for diagnostic in item["diagnostics"]:
                lines.append(f"  - {diagnostic['code']}: {diagnostic['message']}")
    lines.extend(["", "limitations:"])
    for item in result["limitations"]:
        lines.append(f"- {item}")
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        description="Check structured Agama evidence reasoning cases from tests/reasoning_cases.yaml."
    )
    parser.add_argument("--cases", type=Path, default=DEFAULT_CASES, help="Reasoning cases YAML path.")
    parser.add_argument(
        "--retrieval-fixture",
        type=Path,
        default=DEFAULT_RETRIEVAL_FIXTURE,
        help="Semantic retrieval chunks YAML path.",
    )
    parser.add_argument("--case-id", help="Reasoning case id, such as ZR-05.")
    parser.add_argument("--json", action="store_true", dest="json_output", help="Emit machine-readable JSON.")
    args = parser.parse_args()

    try:
        result = build_agama_evidence_check(
            args.cases,
            case_id=args.case_id,
            retrieval_fixture_path=args.retrieval_fixture,
        )
    except AgamaEvidenceCheckerError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    if args.json_output:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(_render_text(result), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
