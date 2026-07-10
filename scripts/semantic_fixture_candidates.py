from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from zilanlib.agama.candidates import DEFAULT_PATTERN, ROOT, CandidateError, build_candidate_set


def _print_text(result: dict[str, Any]) -> None:
    print(f"mode: {result['mode']}")
    print(f"source_script: {result['source_script']}")
    print(f"terms: {result['terms']}")
    print("chunks:")
    for index, chunk in enumerate(result["chunks"], start=1):
        print(f"{index}. {chunk['chunk_id']}")
        print(f"   source_file: {chunk['source_file']}")
        print(f"   citation: {chunk['citation']}")
        print(f"   passage_citation: {chunk['passage_citation']}")
    print("limitations:")
    for item in result["limitations"]:
        print(f"- {item}")


def _print_yaml(result: dict[str, Any]) -> None:
    try:
        import yaml  # type: ignore[import-not-found]
    except ModuleNotFoundError as exc:
        raise CandidateError("PyYAML is required for --yaml output.") from exc
    print(yaml.safe_dump(result, allow_unicode=True, sort_keys=False))


def _reconfigure_stream(stream: object) -> None:
    reconfigure = getattr(stream, "reconfigure", None)
    if callable(reconfigure):
        reconfigure(encoding="utf-8")


def main() -> int:
    _reconfigure_stream(sys.stdout)
    _reconfigure_stream(sys.stderr)

    parser = argparse.ArgumentParser(
        description="Generate semantic retrieval fixture candidates from the Agama keyword-search baseline."
    )
    parser.add_argument("--root", type=Path, default=ROOT, help="Repository root.")
    parser.add_argument("--terms", default=DEFAULT_PATTERN, help="Regex terms passed to search_agama.py.")
    parser.add_argument("--limit", type=int, default=5, help="Maximum unique passage candidates; 0 means no limit.")
    parser.add_argument("--topic", action="append", default=[], help="Topic metadata value. Can be repeated.")
    parser.add_argument(
        "--include-false-positives",
        action="store_true",
        help="Do not filter search_agama.py known keyword collisions.",
    )
    output = parser.add_mutually_exclusive_group()
    output.add_argument("--json", action="store_true", dest="json_output", help="Emit JSON.")
    output.add_argument("--yaml", action="store_true", dest="yaml_output", help="Emit YAML.")
    args = parser.parse_args()

    try:
        result = build_candidate_set(
            root=args.root,
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
    except CandidateError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    return 0 if result["chunks"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
