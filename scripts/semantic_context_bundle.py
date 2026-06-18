from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from semantic_retrieval_dry_run import DEFAULT_FIXTURE, FixtureError, build_dry_run

MODE = "semantic-context-bundle"
LIMITATIONS = (
    "Fixture-defined context bundle only; no embeddings, vector search, reranking, or provider calls.",
    "Chunk order follows the query fixture expected_chunk_ids order.",
    "This output is prompt-ready scaffolding, not runtime answer-quality validation.",
)


def _reasoning_roles(chunk: dict[str, Any]) -> list[str]:
    metadata = chunk.get("metadata")
    if not isinstance(metadata, dict):
        return []
    roles = metadata.get("reasoning_roles", [])
    if not isinstance(roles, list):
        return []
    return [role for role in roles if isinstance(role, str)]


def _citation(chunk: dict[str, Any]) -> str:
    citation = chunk.get("passage_citation") or chunk.get("citation")
    return citation if isinstance(citation, str) else ""


def _bundle_chunk(index: int, chunk: dict[str, Any]) -> dict[str, Any]:
    return {
        "index": index,
        "chunk_id": chunk.get("chunk_id"),
        "chunk_type": chunk.get("chunk_type"),
        "source_file": chunk.get("source_file"),
        "citation": _citation(chunk),
        "reasoning_roles": _reasoning_roles(chunk),
        "text": chunk.get("text"),
    }


def _render_bundle_text(query: str, chunks: list[dict[str, Any]]) -> str:
    lines = [
        "# Semantic Retrieval Context Bundle",
        "",
        f"Query: {query}",
        "",
        "Boundary: fixture-only context assembly; verify citations before scholarly or publication use.",
        "",
        "## Chunks",
    ]
    for chunk in chunks:
        roles = ", ".join(chunk["reasoning_roles"]) if chunk["reasoning_roles"] else "unspecified"
        lines.extend(
            [
                "",
                f"### {chunk['index']}. {chunk['chunk_id']}",
                f"- Type: {chunk['chunk_type']}",
                f"- Source: {chunk['source_file']}",
                f"- Citation: {chunk['citation']}",
                f"- Reasoning roles: {roles}",
                "",
                str(chunk["text"] or ""),
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def build_context_bundle(
    fixture_path: Path = DEFAULT_FIXTURE,
    *,
    query_id: str | None = None,
    query: str | None = None,
    limit: int | None = None,
) -> dict[str, Any]:
    """Build a prompt-ready context bundle from fixture-selected chunks."""

    dry_run = build_dry_run(fixture_path, query_id=query_id, query=query, limit=limit)
    chunks = [_bundle_chunk(index, chunk) for index, chunk in enumerate(dry_run["chunks"], start=1)]
    bundle_text = _render_bundle_text(str(dry_run["query"]), chunks)

    return {
        "mode": MODE,
        "fixture": dry_run["fixture"],
        "query_id": dry_run["query_id"],
        "query": dry_run["query"],
        "needs": dry_run["needs"],
        "chunk_ids": dry_run["expected_chunk_ids"],
        "chunks": chunks,
        "bundle_text": bundle_text,
        "limitations": list(LIMITATIONS),
    }


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
