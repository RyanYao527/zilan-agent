from __future__ import annotations

from pathlib import Path
from typing import Any

from zilanlib.semantic.retrieval_dry_run import DEFAULT_FIXTURE, ROOT, FixtureError, build_dry_run
from zilanlib.semantic.sample_paths import resolve_answer_sample_path

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


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _mapping_list(value: Any, field: str) -> list[dict[str, Any]]:
    if value is None:
        return []
    if not isinstance(value, list) or not all(isinstance(item, dict) for item in value):
        raise FixtureError(f"{field} must be a list of mappings.")
    return value


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
    answer_text: str | None = None,
    answer_file: Path | None = None,
    sample_id: str | None = None,
) -> dict[str, Any]:
    """Review answer text against fixture-defined non-chunk boundary contracts."""

    dry_run = build_dry_run(fixture_path, query_id=query_id, query=query)
    resolved_answer_text, answer_source = _resolve_answer_source(
        fixture_path,
        dry_run,
        answer_text=answer_text,
        answer_file=answer_file,
        sample_id=sample_id,
    )
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
        reviews.append(_review_contract(need, contract, resolved_answer_text))

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
        "answer_source": answer_source,
        "overall_status": overall_status,
        "reviews": reviews,
        "limitations": list(LIMITATIONS),
    }
    expected_status = answer_source.get("expected_status")
    if isinstance(expected_status, str) and expected_status:
        result["expected_status"] = expected_status
        result["expected_status_match"] = overall_status == expected_status
    result["review_text"] = _render_review_text(result)
    return result


def _resolve_answer_source(
    fixture_path: Path,
    dry_run: dict[str, Any],
    *,
    answer_text: str | None,
    answer_file: Path | None,
    sample_id: str | None,
) -> tuple[str, dict[str, Any]]:
    source_count = sum(source is not None for source in (answer_text, answer_file, sample_id))
    if source_count != 1:
        raise FixtureError("Provide exactly one of --answer-text, --answer-file, or --sample-id.")

    if answer_text is not None:
        return answer_text, {"type": "inline"}
    if answer_file is not None:
        if not answer_file.exists():
            raise FixtureError(f"Answer file not found: {answer_file}")
        return answer_file.read_text(encoding="utf-8"), {
            "type": "file",
            "file": _display_path(answer_file),
        }

    samples = _mapping_list(dry_run.get("answer_boundary_samples"), "answer_boundary_samples")
    for sample in samples:
        if sample.get("id") != sample_id:
            continue

        rel_file = sample.get("file")
        if not isinstance(rel_file, str) or not rel_file:
            raise FixtureError(f"Answer boundary sample {sample_id} missing file.")
        sample_path = resolve_answer_sample_path(rel_file, fixture_path=fixture_path, root=ROOT)
        if sample_path is None:
            raise FixtureError(f"Answer boundary sample file not found: {rel_file}")
        return sample_path.read_text(encoding="utf-8"), {
            "type": "sample",
            "sample_id": sample_id,
            "file": rel_file,
            "expected_status": sample.get("expected_status"),
        }

    raise FixtureError(f"Unknown answer boundary sample id for {dry_run['query_id']}: {sample_id}")
