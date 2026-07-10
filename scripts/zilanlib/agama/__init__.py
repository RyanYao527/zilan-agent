"""Agama corpus helper APIs."""

from zilanlib.agama.candidates import CandidateError, build_candidate_set
from zilanlib.agama.fixture_review import ReviewError, build_review
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
    "CandidateError",
    "ReviewError",
    "build_candidate_set",
    "build_review",
    "is_false_positive",
    "iter_agama_markdown_files",
    "search_agama",
    "search_agama_passages",
]