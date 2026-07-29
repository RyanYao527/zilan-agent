from __future__ import annotations

import re
from collections.abc import Mapping, Sequence
from pathlib import Path


def detect_source_root(root: Path) -> Path | None:
    """Return *root* only when it looks like a zilan-agent source checkout."""

    return root if (root / "context").is_dir() else None


def check_required_paths(
    root: Path,
    required_files: Sequence[str],
    required_context_files: Sequence[str],
    failures: list[str],
) -> None:
    for rel_path in (*required_files, *required_context_files):
        if not (root / rel_path).exists():
            failures.append(f"Missing required path: {rel_path}")


def extract_version(root: Path, rel_path: str, pattern: str, failures: list[str]) -> str | None:
    text = (root / rel_path).read_text(encoding="utf-8")
    match = re.search(pattern, text)
    if not match:
        failures.append(f"{rel_path} missing project version pattern.")
        return None
    return match.group(1)


def check_version_consistency(root: Path, version_sources: Mapping[str, str], failures: list[str]) -> None:
    versions: dict[str, str] = {}
    for rel_path, pattern in version_sources.items():
        version = extract_version(root, rel_path, pattern, failures)
        if version is not None:
            versions[rel_path] = version

    if len(set(versions.values())) > 1:
        details = ", ".join(f"{rel_path}={version}" for rel_path, version in sorted(versions.items()))
        failures.append(f"Project version mismatch: {details}")


def check_regression_matrix(
    root: Path,
    matrix_path: str,
    regression_cases: Sequence[str],
    failures: list[str],
) -> None:
    text = (root / matrix_path).read_text(encoding="utf-8")
    for case in regression_cases:
        if case not in text:
            failures.append(f"Missing regression case in {matrix_path}: {case}")