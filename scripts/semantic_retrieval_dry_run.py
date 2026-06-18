from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_FIXTURE = ROOT / "tests" / "fixtures" / "retrieval_chunks" / "semantic_chunks.yaml"
MODE = "fixture-dry-run"
LIMITATIONS = (
    "Fixture-defined dry run only; no embeddings, vector search, reranking, or provider calls.",
    "scripts/search_agama.py remains the keyword baseline until semantic retrieval has regression evidence.",
)


class FixtureError(ValueError):
    """Raised when the semantic retrieval fixture is missing or internally inconsistent."""


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FixtureError(f"Fixture not found: {_display_path(path)}")

    try:
        import yaml  # type: ignore[import-not-found]
    except ModuleNotFoundError as exc:
        raise FixtureError("PyYAML is required to read semantic retrieval fixtures.") from exc

    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001 - keep parser failures visible in CLI output.
        raise FixtureError(f"Failed to parse fixture {_display_path(path)}: {exc}") from exc

    if not isinstance(data, dict):
        raise FixtureError(f"Fixture must be a mapping: {_display_path(path)}")
    return data


def _mapping_list(data: dict[str, Any], field: str) -> list[dict[str, Any]]:
    items = data.get(field)
    if not isinstance(items, list) or not items:
        raise FixtureError(f"Fixture must contain a non-empty {field} list.")
    if not all(isinstance(item, dict) for item in items):
        raise FixtureError(f"Fixture {field} entries must all be mappings.")
    return items


def _string_list(value: Any, field: str) -> list[str]:
    if not isinstance(value, list) or not all(isinstance(item, str) and item for item in value):
        raise FixtureError(f"{field} must be a non-empty string list.")
    return list(value)


def _chunk_map(chunks: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    mapped: dict[str, dict[str, Any]] = {}
    for chunk in chunks:
        chunk_id = chunk.get("chunk_id")
        if not isinstance(chunk_id, str) or not chunk_id:
            raise FixtureError("Every chunk must have a non-empty chunk_id.")
        if chunk_id in mapped:
            raise FixtureError(f"Duplicate chunk_id: {chunk_id}")
        mapped[chunk_id] = chunk
    return mapped


def _select_query(
    queries: list[dict[str, Any]],
    *,
    query_id: str | None,
    query: str | None,
) -> dict[str, Any]:
    if query_id and query:
        raise FixtureError("Use either --query-id or --query, not both.")

    if query_id:
        for item in queries:
            if item.get("id") == query_id:
                return item
        raise FixtureError(f"Unknown query id: {query_id}")

    if query:
        for item in queries:
            if item.get("query") == query:
                return item
        raise FixtureError("No fixture query exactly matches --query.")

    return queries[0]


def build_dry_run(
    fixture_path: Path = DEFAULT_FIXTURE,
    *,
    query_id: str | None = None,
    query: str | None = None,
    limit: int | None = None,
) -> dict[str, Any]:
    """Build a deterministic fixture-based semantic retrieval dry-run result."""

    if limit is not None and limit < 1:
        raise FixtureError("--limit must be greater than zero.")

    data = _load_yaml(fixture_path)
    chunks = _mapping_list(data, "chunks")
    queries = _mapping_list(data, "queries")
    chunks_by_id = _chunk_map(chunks)
    selected_query = _select_query(queries, query_id=query_id, query=query)

    expected_chunk_ids = _string_list(selected_query.get("expected_chunk_ids"), "expected_chunk_ids")
    if limit is not None:
        expected_chunk_ids = expected_chunk_ids[:limit]

    missing_ids = [chunk_id for chunk_id in expected_chunk_ids if chunk_id not in chunks_by_id]
    if missing_ids:
        raise FixtureError(f"Query {selected_query.get('id')} references unknown chunks: {missing_ids}")

    selected_chunks = [dict(chunks_by_id[chunk_id]) for chunk_id in expected_chunk_ids]

    return {
        "mode": MODE,
        "fixture": _display_path(fixture_path),
        "query_id": selected_query.get("id"),
        "query": selected_query.get("query"),
        "needs": selected_query.get("needs", []),
        "non_chunk_needs": selected_query.get("non_chunk_needs", []),
        "keywords": selected_query.get("keywords", {}),
        "expected_sources": selected_query.get("expected_sources", []),
        "expected_chunk_ids": expected_chunk_ids,
        "chunks": selected_chunks,
        "limitations": list(LIMITATIONS),
    }


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
