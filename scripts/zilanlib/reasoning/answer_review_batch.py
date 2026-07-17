from __future__ import annotations

from pathlib import Path
from typing import Any

from zilanlib.reasoning.answer_review import build_reasoning_answer_review
from zilanlib.reasoning.hetuvidya_validator import DEFAULT_CASES
from zilanlib.semantic.retrieval_dry_run import DEFAULT_FIXTURE, ROOT
from zilanlib.yaml_io import display_path, load_yaml_mapping

MODE = "reasoning-answer-review-batch-v0"
OUTPUT_SCHEMA = "reasoning-answer-review-batch-output-v0"
LIMITATIONS = (
    "Batch review only orchestrates local fixture answer reviews; it does not call providers or generate answers.",
    "Each batch item uses the same shallow answer-contract and structured-validator limitations as a single review.",
    "Batch status is a review convenience signal, not platform validation or doctrinal grading.",
)


class BatchReviewError(ValueError):
    """Raised when an answer-review batch manifest is invalid."""


def _display_path(path: Path) -> str:
    return display_path(path, root=ROOT)


def _load_yaml(path: Path) -> dict[str, Any]:
    return load_yaml_mapping(
        path,
        root=ROOT,
        error_type=BatchReviewError,
        missing_message="PyYAML is required to read answer review batch manifests.",
        missing_file_label="Answer review batch manifest not found",
        parse_label="Failed to parse answer review batch manifest",
        mapping_label="Answer review batch manifest must be a mapping",
    )


def _review_items(data: dict[str, Any]) -> list[dict[str, Any]]:
    version = data.get("version")
    if version != 1:
        raise BatchReviewError("Answer review batch manifest version must be 1.")

    reviews = data.get("reviews")
    if not isinstance(reviews, list) or not reviews:
        raise BatchReviewError("Answer review batch manifest must contain a non-empty reviews list.")
    if not all(isinstance(item, dict) for item in reviews):
        raise BatchReviewError("Every answer review batch item must be a mapping.")
    return reviews


def _optional_string(item: dict[str, Any], field: str, index: int) -> str | None:
    value = item.get(field)
    if value is None:
        return None
    if not isinstance(value, str) or not value:
        raise BatchReviewError(f"reviews[{index}].{field} must be a non-empty string when present.")
    return value


def _required_string(item: dict[str, Any], field: str, index: int) -> str:
    value = _optional_string(item, field, index)
    if value is None:
        raise BatchReviewError(f"reviews[{index}].{field} is required.")
    return value


def _optional_int(item: dict[str, Any], field: str, index: int) -> int | None:
    value = item.get(field)
    if value is None:
        return None
    if not isinstance(value, int) or isinstance(value, bool):
        raise BatchReviewError(f"reviews[{index}].{field} must be an integer when present.")
    return value


def _optional_path(item: dict[str, Any], field: str, index: int) -> Path | None:
    value = _optional_string(item, field, index)
    if value is None:
        return None
    path = Path(value)
    return path if path.is_absolute() else ROOT / path


def _source_count(*, answer_text: str | None, answer_file: Path | None, sample_id: str | None) -> int:
    return sum(source is not None for source in (answer_text, answer_file, sample_id))


def _review_args(item: dict[str, Any], index: int) -> dict[str, Any]:
    review_id = _required_string(item, "id", index)
    query_id = _optional_string(item, "query_id", index)
    query = _optional_string(item, "query", index)
    if query_id is None and query is None:
        raise BatchReviewError(f"reviews[{index}] must provide query_id or query.")

    answer_text = _optional_string(item, "answer_text", index)
    answer_file = _optional_path(item, "answer_file", index)
    sample_id = _optional_string(item, "sample_id", index)
    if _source_count(answer_text=answer_text, answer_file=answer_file, sample_id=sample_id) > 1:
        raise BatchReviewError(f"reviews[{index}] must provide at most one answer source.")

    return {
        "id": review_id,
        "query_id": query_id,
        "query": query,
        "limit": _optional_int(item, "limit", index),
        "answer_text": answer_text,
        "answer_file": answer_file,
        "sample_id": sample_id,
    }


def _validator_families(review: dict[str, Any]) -> list[dict[str, Any]]:
    families: list[dict[str, Any]] = []
    for validator in review["validator_summaries"]:
        families.append(
            {
                "family": validator["family"],
                "status": validator["status"],
                "case_ids": validator["case_ids"],
            }
        )
    return families


def _compact_review(review_id: str, review: dict[str, Any]) -> dict[str, Any]:
    contract_summary = review["contract_summary"]
    role_summary = review["role_coverage_summary"]
    return {
        "id": review_id,
        "query_id": review["query_id"],
        "query": review["query"],
        "overall_status": review["overall_status"],
        "answer_review_status": review["answer_review_status"],
        "answer_source": review["answer_source"],
        "role_coverage_status": role_summary["status"],
        "missing_needs": role_summary["missing_needs"],
        "contract_status": contract_summary["status"],
        "missing_required_terms": contract_summary["missing_required_terms"],
        "present_forbidden_terms": contract_summary["present_forbidden_terms"],
        "missing_required_slots": contract_summary["missing_required_slots"],
        "validator_families": _validator_families(review),
    }


def _status_summary(reviews: list[dict[str, Any]]) -> dict[str, int]:
    summary = {
        "total": len(reviews),
        "pass": 0,
        "fail": 0,
        "review_needed": 0,
        "other": 0,
    }
    for review in reviews:
        status = review["overall_status"]
        if status in ("pass", "fail", "review_needed"):
            summary[status] += 1
        else:
            summary["other"] += 1
    return summary


def _overall_status(summary: dict[str, int]) -> str:
    if summary["fail"]:
        return "fail"
    if summary["review_needed"]:
        return "review_needed"
    if summary["other"]:
        return "unknown"
    return "pass"


def _render_batch_text(result: dict[str, Any]) -> str:
    lines = [
        "# Reasoning Answer Review Batch",
        "",
        f"Batch: {result['batch']}",
        f"Overall status: {result['overall_status']}",
        (
            "Summary: "
            f"pass={result['summary']['pass']}, "
            f"fail={result['summary']['fail']}, "
            f"review_needed={result['summary']['review_needed']}, "
            f"other={result['summary']['other']}"
        ),
        "",
        "Boundary: batch fixture review only; this is not runtime platform validation.",
        "",
        "## Reviews",
    ]
    for review in result["reviews"]:
        lines.append(f"- {review['id']}: {review['overall_status']} ({review['query_id']})")
        missing = review["missing_required_terms"] + review["missing_required_slots"]
        if missing:
            lines.append(f"  missing: {', '.join(missing)}")
        if review["missing_needs"]:
            lines.append(f"  missing needs: {', '.join(review['missing_needs'])}")

    lines.extend(["", "## Limitations"])
    for limitation in result["limitations"]:
        lines.append(f"- {limitation}")
    return "\n".join(lines).rstrip() + "\n"


def build_reasoning_answer_review_batch(
    batch_path: Path,
    fixture_path: Path = DEFAULT_FIXTURE,
    cases_path: Path = DEFAULT_CASES,
) -> dict[str, Any]:
    """Build compact answer-review summaries for a YAML batch manifest."""

    compact_reviews: list[dict[str, Any]] = []
    for index, item in enumerate(_review_items(_load_yaml(batch_path))):
        args = _review_args(item, index)
        review_id = str(args.pop("id"))
        review = build_reasoning_answer_review(
            fixture_path,
            cases_path,
            query_id=args["query_id"],
            query=args["query"],
            limit=args["limit"],
            answer_text=args["answer_text"],
            answer_file=args["answer_file"],
            sample_id=args["sample_id"],
        )
        compact_reviews.append(_compact_review(review_id, review))

    summary = _status_summary(compact_reviews)
    result = {
        "mode": MODE,
        "output_schema": OUTPUT_SCHEMA,
        "batch": _display_path(batch_path),
        "fixture": _display_path(fixture_path),
        "reasoning_cases": _display_path(cases_path),
        "overall_status": _overall_status(summary),
        "summary": summary,
        "reviews": compact_reviews,
        "limitations": list(LIMITATIONS),
    }
    result["review_text"] = _render_batch_text(result)
    return result