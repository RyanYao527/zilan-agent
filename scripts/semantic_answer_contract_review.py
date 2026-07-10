from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from semantic_retrieval_dry_run import DEFAULT_FIXTURE, FixtureError
from zilanlib.semantic.answer_contract_review import build_answer_contract_review


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        description="Review answer text against fixture-defined answer contracts."
    )
    parser.add_argument("--fixture", type=Path, default=DEFAULT_FIXTURE, help="Semantic chunks fixture YAML path.")
    parser.add_argument("--query-id", help="Query fixture id, such as SRQ-02.")
    parser.add_argument("--query", help="Exact query text to match from the fixture.")
    parser.add_argument("--answer-text", help="Answer text to review.")
    parser.add_argument("--answer-file", type=Path, help="UTF-8 answer text file to review.")
    parser.add_argument("--sample-id", help="Checked-in answer contract sample id to review.")
    parser.add_argument("--json", action="store_true", dest="json_output", help="Emit machine-readable JSON.")
    args = parser.parse_args()

    try:
        result = build_answer_contract_review(
            args.fixture,
            query_id=args.query_id,
            query=args.query,
            answer_text=args.answer_text,
            answer_file=args.answer_file,
            sample_id=args.sample_id,
        )
    except FixtureError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    if args.json_output:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(result["review_text"], end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())