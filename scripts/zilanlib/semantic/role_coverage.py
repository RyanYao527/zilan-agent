from __future__ import annotations

from pathlib import Path
from typing import Any

from semantic_retrieval_dry_run import DEFAULT_FIXTURE

from zilanlib.semantic.context_bundle import build_context_bundle

MODE = "semantic-role-coverage"
LIMITATIONS = (
    "Fixture-defined role coverage review only; no embeddings, vector search, reranking, or provider calls.",
    "Missing needs are review findings, not runtime answer-quality failures.",
    "This helper does not auto-edit retrieval fixtures or infer doctrinal completeness.",
)


def _unique_ordered(items: list[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for item in items:
        if item not in seen:
            seen.add(item)
            ordered.append(item)
    return ordered


def _chunk_roles(chunk: dict[str, Any]) -> list[str]:
    roles = chunk.get("reasoning_roles", [])
    if not isinstance(roles, list):
        return []
    return [role for role in roles if isinstance(role, str)]


def _chunk_id(chunk: dict[str, Any]) -> str:
    value = chunk.get("chunk_id")
    return value if isinstance(value, str) else ""


def _coverage_by_need(needs: list[str], chunks: list[dict[str, Any]]) -> dict[str, list[str]]:
    coverage: dict[str, list[str]] = {need: [] for need in needs}
    for chunk in chunks:
        chunk_id = _chunk_id(chunk)
        roles = set(_chunk_roles(chunk))
        for need in needs:
            if need in roles:
                coverage[need].append(chunk_id)
    return coverage


def _chunk_role_map(needs: list[str], chunks: list[dict[str, Any]]) -> list[dict[str, Any]]:
    need_set = set(needs)
    mapped: list[dict[str, Any]] = []
    for chunk in chunks:
        roles = _chunk_roles(chunk)
        mapped.append(
            {
                "chunk_id": _chunk_id(chunk),
                "reasoning_roles": roles,
                "matched_needs": [role for role in roles if role in need_set],
                "extra_roles": [role for role in roles if role not in need_set],
            }
        )
    return mapped


def _render_review_text(result: dict[str, Any]) -> str:
    lines = [
        "# Semantic Context Bundle Role Coverage",
        "",
        f"Query ID: {result['query_id']}",
        f"Query: {result['query']}",
        f"Coverage status: {result['coverage_status']}",
        "",
        "Boundary: fixture-only role coverage review; missing needs require maintainer judgment.",
        "",
        "## Covered Needs",
    ]
    covered_needs = result["covered_needs"]
    if covered_needs:
        for need, chunk_ids in covered_needs.items():
            lines.append(f"- {need}: {', '.join(chunk_ids)}")
    else:
        lines.append("- none")

    lines.extend(["", "## Non-Chunk Needs"])
    non_chunk_needs = result["non_chunk_needs"]
    if non_chunk_needs:
        for need in non_chunk_needs:
            lines.append(f"- {need}")
    else:
        lines.append("- none")

    lines.extend(["", "## Missing Needs"])
    missing_needs = result["missing_needs"]
    if missing_needs:
        for need in missing_needs:
            lines.append(f"- {need}")
    else:
        lines.append("- none")

    lines.extend(["", "## Chunk Role Map"])
    for item in result["chunk_role_map"]:
        roles = ", ".join(item["reasoning_roles"]) if item["reasoning_roles"] else "unspecified"
        matched = ", ".join(item["matched_needs"]) if item["matched_needs"] else "none"
        lines.append(f"- {item['chunk_id']}: roles={roles}; matched_needs={matched}")

    return "\n".join(lines).rstrip() + "\n"


def build_role_coverage(
    fixture_path: Path = DEFAULT_FIXTURE,
    *,
    query_id: str | None = None,
    query: str | None = None,
    limit: int | None = None,
) -> dict[str, Any]:
    """Review how selected context-bundle chunk roles cover query needs."""

    bundle = build_context_bundle(fixture_path, query_id=query_id, query=query, limit=limit)
    needs = _unique_ordered([need for need in bundle["needs"] if isinstance(need, str)])
    non_chunk_needs = _unique_ordered([need for need in bundle["non_chunk_needs"] if isinstance(need, str)])
    role_needs = [need for need in needs if need not in set(non_chunk_needs)]
    chunks = bundle["chunks"]
    coverage_by_need = _coverage_by_need(role_needs, chunks)
    covered_needs = {need: chunk_ids for need, chunk_ids in coverage_by_need.items() if chunk_ids}
    missing_needs = [need for need, chunk_ids in coverage_by_need.items() if not chunk_ids]
    all_roles = _unique_ordered([role for chunk in chunks for role in _chunk_roles(chunk)])
    extra_roles = [role for role in all_roles if role not in set(role_needs)]
    coverage_status = "complete" if role_needs and not missing_needs else "partial"
    if not role_needs:
        coverage_status = "no_needs_declared"

    result = {
        "mode": MODE,
        "fixture": bundle["fixture"],
        "query_id": bundle["query_id"],
        "query": bundle["query"],
        "needs": needs,
        "role_needs": role_needs,
        "non_chunk_needs": non_chunk_needs,
        "chunk_ids": bundle["chunk_ids"],
        "coverage_status": coverage_status,
        "covered_needs": covered_needs,
        "missing_needs": missing_needs,
        "extra_roles": extra_roles,
        "chunk_role_map": _chunk_role_map(role_needs, chunks),
        "limitations": list(LIMITATIONS),
    }
    result["review_text"] = _render_review_text(result)
    return result
