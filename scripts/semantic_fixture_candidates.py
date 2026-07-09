from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

from zilanlib.agama.search import DEFAULT_PATTERN, search_agama

ROOT = Path(__file__).resolve().parents[1]
MODE = "agama-fixture-candidates"
SOURCE_SCRIPT = "scripts/search_agama.py"
HASH_ALGORITHM = "sha256"
LIMITATIONS = (
    "Candidate generation is keyword-baseline only; no embeddings, vector search, reranking, or provider calls.",
    "Review generated candidates before copying them into tests/fixtures/retrieval_chunks/semantic_chunks.yaml.",
)


class CandidateError(ValueError):
    """Raised when semantic fixture candidate generation cannot proceed."""


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _terms_to_topics(terms: str) -> list[str]:
    topics: list[str] = []
    for item in terms.split("|"):
        topic = item.strip()
        if topic and topic not in topics:
            topics.append(topic)
    return topics


def _juan_slug(juan: str | None) -> str:
    if not juan:
        return "juan-unknown"
    match = re.search(r"\d+", juan)
    if match:
        return f"juan-{match.group(0)}"
    return "juan-unknown"


def _passage_text(root: Path, rel_file: str, start_line: int, end_line: int) -> str:
    path = root / rel_file
    lines = path.read_text(encoding="utf-8").splitlines()
    return "\n".join(line.strip() for line in lines[start_line - 1 : end_line] if line.strip())


def _text_hash(text: str) -> str:
    return f"{HASH_ALGORITHM}:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


def build_candidate_set(
    *,
    root: Path = ROOT,
    terms: str = DEFAULT_PATTERN,
    limit: int = 5,
    topics: list[str] | None = None,
    include_false_positives: bool = False,
) -> dict[str, Any]:
    """Generate Agama passage chunk candidates from the keyword-search baseline."""

    if limit < 0:
        raise CandidateError("--limit must be zero or greater.")

    root = root.resolve()
    topic_values = topics if topics is not None else _terms_to_topics(terms)
    matches = search_agama(
        terms,
        root=root,
        limit=0,
        include_false_positives=include_false_positives,
    )
    chunks: list[dict[str, Any]] = []
    chunks_by_passage: dict[tuple[str, int, int], dict[str, Any]] = {}

    for match in matches:
        key = (match.file, match.passage_start_line, match.passage_end_line)
        existing = chunks_by_passage.get(key)
        if existing is not None:
            existing["metadata"]["matched_lines"].append(match.line)
            existing["metadata"]["provenance"]["matched_lines"].append(match.line)
            continue

        text = _passage_text(root, match.file, match.passage_start_line, match.passage_end_line)
        line_text_hash = _text_hash(text)
        chunk = {
            "chunk_id": (
                f"agama:{match.cbeta_id}:{_juan_slug(match.juan)}:line-{match.passage_start_line}"
            ),
            "chunk_type": "agama_passage",
            "source_file": match.file,
            "start_line": match.passage_start_line,
            "end_line": match.passage_end_line,
            "citation": match.citation,
            "passage_citation": match.passage_citation,
            "text": text,
            "metadata": {
                "collection": match.sutra_name,
                "cbeta_id": match.cbeta_id,
                "juan": match.juan,
                "section_marker": match.section_marker,
                "topics": topic_values,
                "reasoning_roles": ["agama_evidence"],
                "matched_lines": [match.line],
                "source_hash": line_text_hash,
                "line_text_hash": line_text_hash,
                "provenance": {
                    "source_script": SOURCE_SCRIPT,
                    "source_file": match.file,
                    "line_range": {
                        "start": match.passage_start_line,
                        "end": match.passage_end_line,
                    },
                    "matched_lines": [match.line],
                    "hash_algorithm": HASH_ALGORITHM,
                    "line_text_hash": line_text_hash,
                    "source_hash_scope": "legacy_alias_for_line_text_hash",
                    "line_text_hash_scope": "trimmed_non_empty_lines_joined_with_lf",
                },
            },
        }
        chunks.append(chunk)
        chunks_by_passage[key] = chunk
        if limit and len(chunks) >= limit:
            break

    return {
        "mode": MODE,
        "source_script": SOURCE_SCRIPT,
        "terms": terms,
        "limit": limit,
        "chunks": chunks,
        "limitations": list(LIMITATIONS),
    }


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


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")

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
