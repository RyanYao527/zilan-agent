from __future__ import annotations

from pathlib import Path
from typing import Any

from zilanlib.agama.candidates import DEFAULT_PATTERN, ROOT, build_candidate_set

DEFAULT_FIXTURE = ROOT / "tests" / "fixtures" / "retrieval_chunks" / "semantic_chunks.yaml"
MODE = "semantic-fixture-review"
LIMITATIONS = (
    "Review only; this command does not write to tests/fixtures/retrieval_chunks/semantic_chunks.yaml.",
    "Candidate generation remains keyword-baseline only; no embeddings, vector search, reranking, or provider calls.",
)


class ReviewError(ValueError):
    """Raised when the fixture review input cannot be loaded or compared."""


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _load_fixture(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise ReviewError(f"Fixture not found: {_display_path(path)}")

    try:
        import yaml  # type: ignore[import-not-found]
    except ModuleNotFoundError as exc:
        raise ReviewError("PyYAML is required to read semantic retrieval fixtures.") from exc

    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001 - expose YAML parser details for maintainers.
        raise ReviewError(f"Failed to parse fixture {_display_path(path)}: {exc}") from exc

    if not isinstance(data, dict):
        raise ReviewError(f"Fixture must be a mapping: {_display_path(path)}")
    chunks = data.get("chunks", [])
    if not isinstance(chunks, list) or not all(isinstance(chunk, dict) for chunk in chunks):
        raise ReviewError("Fixture chunks must be a list of mappings.")
    return data


def _chunk_id(chunk: dict[str, Any]) -> str:
    value = chunk.get("chunk_id")
    if not isinstance(value, str) or not value:
        raise ReviewError("Every fixture and candidate chunk must have a non-empty chunk_id.")
    return value


def _chunk_range(chunk: dict[str, Any]) -> tuple[str, int, int] | None:
    source_file = chunk.get("source_file")
    start_line = chunk.get("start_line")
    end_line = chunk.get("end_line")
    if isinstance(source_file, str) and isinstance(start_line, int) and isinstance(end_line, int):
        return (source_file, start_line, end_line)
    return None


def _summarize_chunk(chunk: dict[str, Any]) -> dict[str, Any]:
    metadata = _metadata(chunk)
    return {
        "chunk_id": _chunk_id(chunk),
        "chunk_type": chunk.get("chunk_type"),
        "source_file": chunk.get("source_file"),
        "start_line": chunk.get("start_line"),
        "end_line": chunk.get("end_line"),
        "citation": chunk.get("citation"),
        "passage_citation": chunk.get("passage_citation"),
        "section_label": metadata.get("section_label"),
    }


def _metadata(chunk: dict[str, Any]) -> dict[str, Any]:
    metadata = chunk.get("metadata")
    return metadata if isinstance(metadata, dict) else {}


def _provenance(chunk: dict[str, Any]) -> dict[str, Any]:
    provenance = _metadata(chunk).get("provenance")
    return provenance if isinstance(provenance, dict) else {}


def _append_difference(
    differences: list[dict[str, Any]],
    *,
    field: str,
    candidate_value: Any,
    fixture_value: Any,
) -> None:
    if candidate_value != fixture_value:
        differences.append(
            {
                "field": field,
                "candidate": candidate_value,
                "fixture": fixture_value,
            }
        )


def _provenance_drift(
    candidate: dict[str, Any],
    fixture_chunk: dict[str, Any],
    *,
    match_type: str,
) -> dict[str, Any] | None:
    candidate_metadata = _metadata(candidate)
    fixture_metadata = _metadata(fixture_chunk)
    candidate_provenance = _provenance(candidate)
    fixture_provenance = _provenance(fixture_chunk)

    differences: list[dict[str, Any]] = []
    for field in ("section_marker", "section_title", "section_label", "source_hash", "line_text_hash", "matched_lines"):
        _append_difference(
            differences,
            field=f"metadata.{field}",
            candidate_value=candidate_metadata.get(field),
            fixture_value=fixture_metadata.get(field),
        )

    for field in (
        "source_script",
        "source_file",
        "line_range",
        "matched_lines",
        "hash_algorithm",
        "line_text_hash",
        "source_hash_scope",
        "line_text_hash_scope",
    ):
        _append_difference(
            differences,
            field=f"metadata.provenance.{field}",
            candidate_value=candidate_provenance.get(field),
            fixture_value=fixture_provenance.get(field),
        )

    if not differences:
        return None

    return {
        "match_type": match_type,
        "candidate": _summarize_chunk(candidate),
        "fixture": _summarize_chunk(fixture_chunk),
        "differences": differences,
    }


def build_review(
    *,
    root: Path = ROOT,
    fixture_path: Path = DEFAULT_FIXTURE,
    terms: str = DEFAULT_PATTERN,
    limit: int = 5,
    topics: list[str] | None = None,
    include_false_positives: bool = False,
) -> dict[str, Any]:
    """Compare generated Agama fixture candidates with a checked-in semantic fixture."""

    fixture_data = _load_fixture(fixture_path)
    fixture_chunks = fixture_data.get("chunks", [])
    fixture_by_id = {_chunk_id(chunk): chunk for chunk in fixture_chunks}
    fixture_ranges = {
        chunk_range: chunk
        for chunk in fixture_chunks
        if (chunk_range := _chunk_range(chunk)) is not None
    }

    candidate_set = build_candidate_set(
        root=root,
        terms=terms,
        limit=limit,
        topics=topics,
        include_false_positives=include_false_positives,
    )
    candidates = candidate_set["chunks"]

    already_present: list[dict[str, Any]] = []
    range_matches: list[dict[str, Any]] = []
    new_candidates: list[dict[str, Any]] = []
    provenance_drifts: list[dict[str, Any]] = []
    for candidate in candidates:
        candidate_id = _chunk_id(candidate)
        candidate_range = _chunk_range(candidate)
        if candidate_id in fixture_by_id:
            already_present.append(_summarize_chunk(candidate))
            if drift := _provenance_drift(candidate, fixture_by_id[candidate_id], match_type="chunk_id"):
                provenance_drifts.append(drift)
        elif candidate_range in fixture_ranges:
            range_matches.append(_summarize_chunk(candidate))
            if drift := _provenance_drift(candidate, fixture_ranges[candidate_range], match_type="line_range"):
                provenance_drifts.append(drift)
        else:
            new_candidates.append(candidate)

    candidate_ids = {_chunk_id(candidate) for candidate in candidates}
    fixture_only_agama_chunks = [
        _summarize_chunk(chunk)
        for chunk in fixture_chunks
        if chunk.get("chunk_type") == "agama_passage" and _chunk_id(chunk) not in candidate_ids
    ]

    return {
        "mode": MODE,
        "fixture": _display_path(fixture_path),
        "candidate_terms": terms,
        "candidate_limit": limit,
        "summary": {
            "fixture_chunks": len(fixture_chunks),
            "candidate_chunks": len(candidates),
            "already_present": len(already_present),
            "range_matches": len(range_matches),
            "new_candidates": len(new_candidates),
            "provenance_drifts": len(provenance_drifts),
            "fixture_only_agama_chunks": len(fixture_only_agama_chunks),
        },
        "already_present": already_present,
        "range_matches": range_matches,
        "new_candidates": new_candidates,
        "provenance_drifts": provenance_drifts,
        "fixture_only_agama_chunks": fixture_only_agama_chunks,
        "limitations": list(LIMITATIONS),
    }
