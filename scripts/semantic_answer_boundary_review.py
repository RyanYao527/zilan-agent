from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from semantic_retrieval_dry_run import DEFAULT_FIXTURE, FixtureError, build_dry_run

MODE = "semantic-answer-boundary-review"
LIMITATIONS = (
    "Fixture-defined answer-boundary review only; no provider calls or answer generation.",
    "Keyword checks are a minimum contract and do not grade doctrinal correctness or practice usefulness.",
    "practice_boundary is reviewed as answer behavior, not as retrieval evidence.",
)


def _string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, str) and item]


def _review_contract(need: str, contract: dict[str, Any], answer_text: str) -> dict[str, Any]:
    required_terms = _string_list(contract.get("required_terms"))
    forbidden_terms = _string_list(contract.get("forbidden_terms"))
    missing_required_terms = [term for term in required_terms if term not in answer_text]
    present_forbidden_terms = [term for term in forbidden_terms if term in answer_text]
    status = "pass" if not missing_required_terms and not present_forbidden_terms else "fail"

    return {
        "need": need,
        "status": status,
        "description": contract.get("description", ""),
        "required_terms": required_terms,
        "missing_required_terms": missing_required_terms,
        "forbidden_terms": forbidden_terms,
        "present_forbidden_terms": present_forbidden_terms,
    }


def _render_review_text(result: dict[str, Any]) -> str:
    lines = [
        "# Semantic Answer Boundary Review",
        "",
        f"Query ID: {result['query_id']}",
        f"Query: {result['query']}",
        f"Overall status: {result['overall_status']}",
        "",
        "Boundary: fixture-only answer text review; this is not runtime validation.",
        "",
        "## Reviews",
    ]
    for review in result["reviews"]:
        lines.extend(
            [
                "",
                f"### {review['need']}: {review['status']}",
                f"- Description: {review['description']}",
                f"- Missing required terms: {', '.join(review['missing_required_terms']) or 'none'}",
                f"- Present forbidden terms: {', '.join(review['present_forbidden_terms']) or 'none'}",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def build_answer_boundary_review(
    fixture_path: Path = DEFAULT_FIXTURE,
    *,
    query_id: str | None = None,
    query: str | None = None,
    answer_text: str,
) -> dict[str, Any]:
    """Review answer text against fixture-defined non-chunk boundary contracts."""

    dry_run = build_dry_run(fixture_path, query_id=query_id, query=query)
    non_chunk_needs = _string_list(dry_run.get("non_chunk_needs"))
    contracts = dry_run.get("answer_boundary_contracts", {})
    if not isinstance(contracts, dict):
        raise FixtureError("answer_boundary_contracts must be a mapping.")

    reviews: list[dict[str, Any]] = []
    for need in non_chunk_needs:
        contract = contracts.get(need)
        if not isinstance(contract, dict):
            reviews.append(
                {
                    "need": need,
                    "status": "fail",
                    "description": "",
                    "required_terms": [],
                    "missing_required_terms": ["<missing contract>"],
                    "forbidden_terms": [],
                    "present_forbidden_terms": [],
                }
            )
            continue
        reviews.append(_review_contract(need, contract, answer_text))

    if not non_chunk_needs:
        overall_status = "no_non_chunk_needs"
    elif all(review["status"] == "pass" for review in reviews):
        overall_status = "pass"
    else:
        overall_status = "fail"

    result = {
        "mode": MODE,
        "fixture": dry_run["fixture"],
        "query_id": dry_run["query_id"],
        "query": dry_run["query"],
        "non_chunk_needs": non_chunk_needs,
        "overall_status": overall_status,
        "reviews": reviews,
        "limitations": list(LIMITATIONS),
    }
    result["review_text"] = _render_review_text(result)
    return result


def _read_answer_text(answer_text: str | None, answer_file: Path | None) -> str:
    if answer_text and answer_file:
        raise FixtureError("Use either --answer-text or --answer-file, not both.")
    if answer_text is not None:
        return answer_text
    if answer_file is not None:
        if not answer_file.exists():
            raise FixtureError(f"Answer file not found: {answer_file}")
        return answer_file.read_text(encoding="utf-8")
    raise FixtureError("Provide --answer-text or --answer-file.")


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        description="Review answer text against fixture-defined non-chunk answer-boundary contracts."
    )
    parser.add_argument("--fixture", type=Path, default=DEFAULT_FIXTURE, help="Semantic chunks fixture YAML path.")
    parser.add_argument("--query-id", help="Query fixture id, such as SRQ-01.")
    parser.add_argument("--query", help="Exact query text to match from the fixture.")
    parser.add_argument("--answer-text", help="Answer text to review.")
    parser.add_argument("--answer-file", type=Path, help="UTF-8 answer text file to review.")
    parser.add_argument("--json", action="store_true", dest="json_output", help="Emit machine-readable JSON.")
    args = parser.parse_args()

    try:
        answer_text = _read_answer_text(args.answer_text, args.answer_file)
        result = build_answer_boundary_review(
            args.fixture,
            query_id=args.query_id,
            query=args.query,
            answer_text=answer_text,
        )
    except FixtureError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    if args.json_output:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(result["review_text"], end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
