from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from zilanlib.semantic.context_bundle import build_context_bundle
from zilanlib.semantic.retrieval_dry_run import DEFAULT_FIXTURE, FixtureError


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        description="Assemble fixture-selected semantic retrieval chunks into prompt-ready context text."
    )
    parser.add_argument("--fixture", type=Path, default=DEFAULT_FIXTURE, help="Semantic chunks fixture YAML path.")
    parser.add_argument("--query-id", help="Query fixture id, such as SRQ-01.")
    parser.add_argument("--query", help="Exact query text to match from the fixture.")
    parser.add_argument("--limit", type=int, help="Maximum expected chunks to include.")
    parser.add_argument("--json", action="store_true", dest="json_output", help="Emit machine-readable JSON.")
    args = parser.parse_args()

    try:
        result = build_context_bundle(
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
        print(result["bundle_text"], end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
