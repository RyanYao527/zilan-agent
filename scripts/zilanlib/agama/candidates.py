from __future__ import annotations

import hashlib
import re
from pathlib import Path
from typing import Any

from zilanlib.agama.search import DEFAULT_PATTERN, search_agama

ROOT = Path(__file__).resolve().parents[3]
MODE = "agama-fixture-candidates"
SOURCE_SCRIPT = "scripts/search_agama.py"
HASH_ALGORITHM = "sha256"
LIMITATIONS = (
    "Candidate generation is keyword-baseline only; no embeddings, vector search, reranking, or provider calls.",
    "Review generated candidates before copying them into tests/fixtures/retrieval_chunks/semantic_chunks.yaml.",
)


class CandidateError(ValueError):
    """Raised when semantic fixture candidate generation cannot proceed."""


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
            "chunk_id": f"agama:{match.cbeta_id}:{_juan_slug(match.juan)}:line-{match.passage_start_line}",
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
                "section_title": match.section_title,
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
