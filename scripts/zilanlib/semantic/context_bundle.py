from __future__ import annotations

from pathlib import Path
from typing import Any

from semantic_retrieval_dry_run import DEFAULT_FIXTURE, build_dry_run

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


def _render_bundle_text(query: str, chunks: list[dict[str, Any]], non_chunk_needs: list[str]) -> str:
    boundary_needs = ", ".join(non_chunk_needs) if non_chunk_needs else "none"
    lines = [
        "# Semantic Retrieval Context Bundle",
        "",
        f"Query: {query}",
        f"Non-chunk needs: {boundary_needs}",
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
    non_chunk_needs = [need for need in dry_run["non_chunk_needs"] if isinstance(need, str)]
    bundle_text = _render_bundle_text(str(dry_run["query"]), chunks, non_chunk_needs)

    return {
        "mode": MODE,
        "fixture": dry_run["fixture"],
        "query_id": dry_run["query_id"],
        "query": dry_run["query"],
        "needs": dry_run["needs"],
        "non_chunk_needs": non_chunk_needs,
        "chunk_ids": dry_run["expected_chunk_ids"],
        "chunks": chunks,
        "bundle_text": bundle_text,
        "limitations": list(LIMITATIONS),
    }
