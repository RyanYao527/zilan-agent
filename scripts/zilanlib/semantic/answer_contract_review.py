from __future__ import annotations

from pathlib import Path
from typing import Any

from zilanlib.semantic.retrieval_dry_run import DEFAULT_FIXTURE, ROOT, FixtureError, build_dry_run
from zilanlib.semantic.sample_paths import resolve_answer_sample_path

MODE = "semantic-answer-contract-review"
LIMITATIONS = (
    "Fixture-defined answer contract review only; no provider calls or answer generation.",
    "Term and slot checks are a minimum contract and do not grade doctrinal correctness.",
    "This helper checks explicit answer expectations, not retrieval completeness or platform behavior.",
)


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, str) and item]


def _mapping_list(value: Any, field: str) -> list[dict[str, Any]]:
    if value is None:
        return []
    if not isinstance(value, list) or not all(isinstance(item, dict) for item in value):
        raise FixtureError(f"{field} must be a list of mappings.")
    return value


def _review_contract(contract_id: str, contract: dict[str, Any], answer_text: str) -> dict[str, Any]:
    required_terms = _string_list(contract.get("required_terms"))
    forbidden_terms = _string_list(contract.get("forbidden_terms"))
    missing_required_terms = [term for term in required_terms if term not in answer_text]
    present_forbidden_terms = [term for term in forbidden_terms if term in answer_text]
    required_slots = _mapping_list(contract.get("required_slots"), "required_slots")
    slot_reviews = [_review_required_slot(slot, answer_text) for slot in required_slots]
    missing_required_slots = [slot["label"] for slot in slot_reviews if slot["status"] == "fail"]
    status = (
        "pass"
        if not missing_required_terms and not present_forbidden_terms and not missing_required_slots
        else "fail"
    )

    return {
        "contract_id": contract_id,
        "status": status,
        "description": contract.get("description", ""),
        "required_terms": required_terms,
        "missing_required_terms": missing_required_terms,
        "forbidden_terms": forbidden_terms,
        "present_forbidden_terms": present_forbidden_terms,
        "required_slots": slot_reviews,
        "missing_required_slots": missing_required_slots,
    }


def _review_required_slot(slot: dict[str, Any], answer_text: str) -> dict[str, Any]:
    label = slot.get("label", "")
    terms = _string_list(slot.get("terms"))
    matched_terms = [term for term in terms if term in answer_text]
    return {
        "label": label,
        "terms": terms,
        "matched_terms": matched_terms,
        "status": "pass" if matched_terms else "fail",
    }


def _render_review_text(result: dict[str, Any]) -> str:
    lines = [
        "# Semantic Answer Contract Review",
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
                f"### {review['contract_id']}: {review['status']}",
                f"- Description: {review['description']}",
                f"- Missing required terms: {', '.join(review['missing_required_terms']) or 'none'}",
                f"- Present forbidden terms: {', '.join(review['present_forbidden_terms']) or 'none'}",
                f"- Missing required slots: {', '.join(review.get('missing_required_slots', [])) or 'none'}",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def build_answer_contract_review(
    fixture_path: Path = DEFAULT_FIXTURE,
    *,
    query_id: str | None = None,
    query: str | None = None,
    answer_text: str | None = None,
    answer_file: Path | None = None,
    sample_id: str | None = None,
) -> dict[str, Any]:
    """Review answer text against fixture-defined answer contracts."""

    dry_run = build_dry_run(fixture_path, query_id=query_id, query=query)
    resolved_answer_text, answer_source = _resolve_answer_source(
        fixture_path,
        dry_run,
        answer_text=answer_text,
        answer_file=answer_file,
        sample_id=sample_id,
    )
    contracts = dry_run.get("answer_contracts", {})
    if not isinstance(contracts, dict):
        raise FixtureError("answer_contracts must be a mapping.")

    reviews: list[dict[str, Any]] = []
    for contract_id, contract in contracts.items():
        if not isinstance(contract_id, str) or not isinstance(contract, dict):
            reviews.append(
                {
                    "contract_id": str(contract_id),
                    "status": "fail",
                    "description": "",
                    "required_terms": [],
                    "missing_required_terms": ["<invalid contract>"],
                    "forbidden_terms": [],
                    "present_forbidden_terms": [],
                }
            )
            continue
        reviews.append(_review_contract(contract_id, contract, resolved_answer_text))

    if not contracts:
        overall_status = "no_answer_contracts"
    elif all(review["status"] == "pass" for review in reviews):
        overall_status = "pass"
    else:
        overall_status = "fail"

    result = {
        "mode": MODE,
        "fixture": dry_run["fixture"],
        "query_id": dry_run["query_id"],
        "query": dry_run["query"],
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

    samples = _mapping_list(dry_run.get("answer_contract_samples"), "answer_contract_samples")
    for sample in samples:
        if sample.get("id") != sample_id:
            continue

        rel_file = sample.get("file")
        if not isinstance(rel_file, str) or not rel_file:
            raise FixtureError(f"Answer contract sample {sample_id} missing file.")
        sample_path = resolve_answer_sample_path(rel_file, fixture_path=fixture_path, root=ROOT)
        if sample_path is None:
            raise FixtureError(f"Answer contract sample file not found: {rel_file}")
        return sample_path.read_text(encoding="utf-8"), {
            "type": "sample",
            "sample_id": sample_id,
            "file": rel_file,
            "expected_status": sample.get("expected_status"),
        }

    raise FixtureError(f"Unknown answer contract sample id for {dry_run['query_id']}: {sample_id}")


