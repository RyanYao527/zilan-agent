from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from zilanlib.semantic.retrieval_dry_run import DEFAULT_FIXTURE, FixtureError, build_dry_run


def _print_text(result: dict[str, Any]) -> None:
    print(f"mode: {result['mode']}")
    print(f"fixture: {result['fixture']}")
    print(f"query_id: {result['query_id']}")
    print(f"query: {result['query']}")
    print("chunks:")
    for index, chunk in enumerate(result["chunks"], start=1):
        citation = chunk.get("passage_citation") or chunk.get("citation")
        print(f"{index}. {chunk['chunk_id']}")
        print(f"   source_file: {chunk['source_file']}")
        print(f"   citation: {citation}")
    print("limitations:")
    for item in result["limitations"]:
        print(f"- {item}")


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        description="Return fixture-defined semantic retrieval chunks for a query fixture."
    )
    parser.add_argument("--fixture", type=Path, default=DEFAULT_FIXTURE, help="Semantic chunks fixture YAML path.")
    parser.add_argument("--query-id", help="Query fixture id, such as SRQ-01.")
    parser.add_argument("--query", help="Exact query text to match from the fixture.")
    parser.add_argument("--limit", type=int, help="Maximum expected chunks to return.")
    parser.add_argument("--json", action="store_true", dest="json_output", help="Emit machine-readable JSON.")
    args = parser.parse_args()

    try:
        result = build_dry_run(
            args.fixture,
            query_id=args.query_id,
            query=args.query,
            limit=args.limit,
        )
    except FixtureError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    if args.json_output:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        _print_text(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())