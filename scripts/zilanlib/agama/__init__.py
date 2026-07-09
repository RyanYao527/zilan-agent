"""Agama corpus helper APIs."""

from zilanlib.agama.search import (
    DEFAULT_FALSE_POSITIVE_PHRASES,
    DEFAULT_PATTERN,
    AgamaMatch,
    AgamaPassage,
    is_false_positive,
    iter_agama_markdown_files,
    search_agama,
    search_agama_passages,
)

__all__ = [
    "DEFAULT_FALSE_POSITIVE_PHRASES",
    "DEFAULT_PATTERN",
    "AgamaMatch",
    "AgamaPassage",
    "is_false_positive",
    "iter_agama_markdown_files",
    "search_agama",
    "search_agama_passages",
]
