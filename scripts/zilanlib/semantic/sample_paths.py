from __future__ import annotations

from pathlib import Path


def resolve_answer_sample_path(rel_file: str, *, fixture_path: Path, root: Path) -> Path | None:
    """Resolve an answer sample from repository or bundled package fixtures."""

    rel_path = Path(rel_file)
    if rel_path.is_absolute():
        return rel_path if rel_path.exists() else None

    fixture_dir = fixture_path.resolve().parent
    fixture_root = fixture_dir.parent if fixture_dir.name == "retrieval_chunks" else fixture_dir
    candidates = [
        root / rel_path,
        fixture_dir / rel_path,
        fixture_root / rel_path,
    ]

    parts = rel_path.parts
    if len(parts) >= 4 and parts[:3] == ("tests", "fixtures", "answers"):
        candidates.append(fixture_root / "answers" / Path(*parts[3:]))

    seen: set[Path] = set()
    for candidate in candidates:
        if candidate in seen:
            continue
        seen.add(candidate)
        if candidate.exists():
            return candidate
    return None
