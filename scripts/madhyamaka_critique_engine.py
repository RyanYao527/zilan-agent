from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from zilanlib.reasoning.madhyamaka_critique_engine import (
    DEFAULT_CASES,
    MadhyamakaCritiqueEngineError,
    build_madhyamaka_critique,
)


def _render_text(result: dict[str, Any]) -> str:
    lines = [
        f"mode: {result['mode']}",
        f"source: {result['source']}",
    ]
    for item in result["critiques"]:
        madhyamaka = item["madhyamaka_prasanga"]
        commitments = "; ".join(term["text"] for term in madhyamaka["accepted_commitments"])
        contradictions = "; ".join(term["text"] for term in madhyamaka["contradictions"])
        lines.extend(
            [
                "",
                f"{item['case_id']}: {item['title']}",
                f"  prompt: {item['prompt']}",
                f"  opponent_premise: {madhyamaka['opponent_premise']}",
                f"  accepted_commitments: {commitments}",
                f"  contradictions: {contradictions}",
                f"  no_independent_thesis: {madhyamaka['no_independent_thesis']['status']}",
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
        description="Build structured Madhyamaka prasaṅga critiques from tests/reasoning_cases.yaml."
    )
    parser.add_argument("--cases", type=Path, default=DEFAULT_CASES, help="Reasoning cases YAML path.")
    parser.add_argument("--case-id", help="Reasoning case id, such as ZR-09.")
    parser.add_argument("--json", action="store_true", dest="json_output", help="Emit machine-readable JSON.")
    args = parser.parse_args()

    try:
        result = build_madhyamaka_critique(args.cases, case_id=args.case_id)
    except MadhyamakaCritiqueEngineError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    if args.json_output:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(_render_text(result), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
