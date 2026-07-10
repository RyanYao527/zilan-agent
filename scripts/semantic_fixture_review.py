from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from zilanlib.agama.candidates import DEFAULT_PATTERN, ROOT
from zilanlib.agama.fixture_review import DEFAULT_FIXTURE, ReviewError, build_review


def _print_text(result: dict[str, Any]) -> None:
    summary = result["summary"]
    print(f"mode: {result['mode']}")
    print(f"fixture: {result['fixture']}")
    print(f"candidate_terms: {result['candidate_terms']}")
    print(
        "summary: "
        f"fixture={summary['fixture_chunks']}, "
        f"candidates={summary['candidate_chunks']}, "
        f"already_present={summary['already_present']}, "
        f"range_matches={summary['range_matches']}, "
        f"new_candidates={summary['new_candidates']}, "
        f"provenance_drifts={summary['provenance_drifts']}, "
        f"fixture_only_agama={summary['fixture_only_agama_chunks']}"
    )
    if result["new_candidates"]:
        print("new_candidates:")
        for index, chunk in enumerate(result["new_candidates"], start=1):
            print(f"{index}. {chunk['chunk_id']}")
            print(f"   citation: {chunk['passage_citation']}")
    if result["provenance_drifts"]:
        print("provenance_drifts:")
        for index, drift in enumerate(result["provenance_drifts"], start=1):
            candidate_id = drift["candidate"]["chunk_id"]
            fixture_id = drift["fixture"]["chunk_id"]
            print(f"{index}. {candidate_id} vs {fixture_id} ({drift['match_type']})")
            for difference in drift["differences"]:
                print(f"   - {difference['field']}")
    print("limitations:")
    for item in result["limitations"]:
        print(f"- {item}")


def _print_yaml(result: dict[str, Any]) -> None:
    try:
        import yaml  # type: ignore[import-not-found]
    except ModuleNotFoundError as exc:
        raise ReviewError("PyYAML is required for --yaml output.") from exc
    print(yaml.safe_dump(result, allow_unicode=True, sort_keys=False))


def _reconfigure_stream(stream: object) -> None:
    reconfigure = getattr(stream, "reconfigure", None)
    if callable(reconfigure):
        reconfigure(encoding="utf-8")


def main() -> int:
    _reconfigure_stream(sys.stdout)
    _reconfigure_stream(sys.stderr)

    parser = argparse.ArgumentParser(
        description="Review generated semantic fixture candidates against a checked-in fixture without writing files."
    )
    parser.add_argument("--root", type=Path, default=ROOT, help="Repository root.")
    parser.add_argument("--fixture", type=Path, default=DEFAULT_FIXTURE, help="Semantic chunks fixture YAML path.")
    parser.add_argument("--terms", default=DEFAULT_PATTERN, help="Regex terms passed to candidate generation.")
    parser.add_argument("--limit", type=int, default=5, help="Maximum unique passage candidates; 0 means no limit.")
    parser.add_argument("--topic", action="append", default=[], help="Topic metadata value. Can be repeated.")
    parser.add_argument(
        "--include-false-positives",
        action="store_true",
        help="Do not filter search_agama.py known keyword collisions during candidate generation.",
    )
    output = parser.add_mutually_exclusive_group()
    output.add_argument("--json", action="store_true", dest="json_output", help="Emit JSON.")
    output.add_argument("--yaml", action="store_true", dest="yaml_output", help="Emit YAML.")
    args = parser.parse_args()

    try:
        result = build_review(
            root=args.root,
            fixture_path=args.fixture,
            terms=args.terms,
            limit=args.limit,
            topics=args.topic or None,
            include_false_positives=args.include_false_positives,
        )
        if args.yaml_output:
            _print_yaml(result)
        elif args.json_output:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            _print_text(result)
    except ReviewError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
