from __future__ import annotations

from collections.abc import Iterable


def check_required_fragments(
    text: str,
    fragments: Iterable[str],
    failures: list[str],
    *,
    rel_path: str,
    message: str = "missing required fragment",
) -> None:
    for fragment in fragments:
        if fragment not in text:
            failures.append(f"{rel_path} {message}: {fragment}")