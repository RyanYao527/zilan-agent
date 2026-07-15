from __future__ import annotations

from pathlib import Path
from typing import Any

from zilanlib.reasoning.contract_runner import build_reasoning_contract_run
from zilanlib.semantic.retrieval_dry_run import DEFAULT_FIXTURE

MODE = "reasoning-answer-review-v0"
OUTPUT_SCHEMA = "reasoning-answer-review-output-v0"
LIMITATIONS = (
    "Answer-grounded local fixture review only; no provider calls, answer generation, embeddings, or reranking.",
    "Answer contracts are minimum explicitness checks and do not grade doctrinal correctness.",
    "Structured validators review fixture-linked reasoning cases, not arbitrary natural-language claims.",
    "This review does not change platform validation status.",
)


def _contract_summary(answer_contract_review: dict[str, Any] | None, answer_review_status: str) -> dict[str, Any]:
    if answer_contract_review is None:
        return {
            "status": answer_review_status,
            "contracts": [],
            "missing_required_terms": [],
            "present_forbidden_terms": [],
            "missing_required_slots": [],
        }

    contracts: list[dict[str, Any]] = []
    missing_terms: list[str] = []
    forbidden_terms: list[str] = []
    missing_slots: list[str] = []

    for review in answer_contract_review.get("reviews", []):
        if not isinstance(review, dict):
            continue
        contract_id = str(review.get("contract_id", ""))
        contract_missing_terms = _string_list(review.get("missing_required_terms"))
        contract_forbidden_terms = _string_list(review.get("present_forbidden_terms"))
        contract_missing_slots = _string_list(review.get("missing_required_slots"))
        contracts.append(
            {
                "contract_id": contract_id,
                "status": review.get("status", "unknown"),
                "missing_required_terms": contract_missing_terms,
                "present_forbidden_terms": contract_forbidden_terms,
                "missing_required_slots": contract_missing_slots,
            }
        )
        missing_terms.extend(_prefixed(contract_id, contract_missing_terms))
        forbidden_terms.extend(_prefixed(contract_id, contract_forbidden_terms))
        missing_slots.extend(_prefixed(contract_id, contract_missing_slots))

    return {
        "status": answer_contract_review.get("overall_status", "unknown"),
        "contracts": contracts,
        "missing_required_terms": missing_terms,
        "present_forbidden_terms": forbidden_terms,
        "missing_required_slots": missing_slots,
    }


def _prefixed(contract_id: str, values: list[str]) -> list[str]:
    if not contract_id:
        return values
    return [f"{contract_id}:{value}" for value in values]


def _string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, str) and item]


def _validator_summary(validators: dict[str, Any]) -> list[dict[str, Any]]:
    summaries: list[dict[str, Any]] = []
    for family, validator in validators.items():
        if not isinstance(validator, dict):
            continue
        summaries.append(
            {
                "family": family,
                "status": validator.get("status", "unknown"),
                "validator": validator.get("validator", ""),
                "contract_family": validator.get("contract_family", family),
                "case_ids": _string_list(validator.get("case_ids")),
                "count": validator.get("count", 0),
            }
        )
    return summaries


def _role_summary(role_coverage: dict[str, Any]) -> dict[str, Any]:
    return {
        "status": role_coverage.get("coverage_status", "unknown"),
        "covered_needs": role_coverage.get("covered_needs", {}),
        "missing_needs": _string_list(role_coverage.get("missing_needs")),
    }


def _answer_source(answer_contract_review: dict[str, Any] | None) -> dict[str, Any] | None:
    if answer_contract_review is None:
        return None
    source = answer_contract_review.get("answer_source")
    return source if isinstance(source, dict) else None


def _render_review_text(result: dict[str, Any]) -> str:
    contract_summary = result["contract_summary"]
    role_summary = result["role_coverage_summary"]
    lines = [
        "# Reasoning Answer Review",
        "",
        f"Query ID: {result['query_id']}",
        f"Query: {result['query']}",
        f"Overall status: {result['overall_status']}",
        f"Answer review: {result['answer_review_status']}",
        f"Role coverage: {role_summary['status']}",
        f"Answer source: {_render_answer_source(result.get('answer_source'))}",
        "",
        "Boundary: local fixture review only; this is not runtime platform validation.",
        "",
        "## Missing Contract Items",
        f"- Required terms: {', '.join(contract_summary['missing_required_terms']) or 'none'}",
        f"- Forbidden terms present: {', '.join(contract_summary['present_forbidden_terms']) or 'none'}",
        f"- Required slots: {', '.join(contract_summary['missing_required_slots']) or 'none'}",
        "",
        "## Missing Reasoning Needs",
    ]
    if role_summary["missing_needs"]:
        for need in role_summary["missing_needs"]:
            lines.append(f"- {need}")
    else:
        lines.append("- none")

    lines.extend(["", "## Validator Families"])
    for validator in result["validator_summaries"]:
        case_ids = ", ".join(validator["case_ids"]) or "none"
        lines.append(f"- {validator['family']}: {validator['status']} ({case_ids})")

    lines.extend(["", "## Limitations"])
    for limitation in result["limitations"]:
        lines.append(f"- {limitation}")

    return "\n".join(lines).rstrip() + "\n"


def _render_answer_source(source: dict[str, Any] | None) -> str:
    if source is None:
        return "none"
    source_type = source.get("type", "unknown")
    if source_type == "sample":
        return f"sample:{source.get('sample_id', '')}"
    if source_type == "file":
        return f"file:{source.get('file', '')}"
    return str(source_type)


def build_reasoning_answer_review(
    fixture_path: Path = DEFAULT_FIXTURE,
    cases_path: Path | None = None,
    *,
    query_id: str | None = None,
    query: str | None = None,
    limit: int | None = None,
    answer_text: str | None = None,
    answer_file: Path | None = None,
    sample_id: str | None = None,
) -> dict[str, Any]:
    """Build a compact answer-grounded reasoning review from local fixtures."""

    runner_kwargs: dict[str, Any] = {
        "query_id": query_id,
        "query": query,
        "limit": limit,
        "answer_text": answer_text,
        "answer_file": answer_file,
        "sample_id": sample_id,
    }
    if cases_path is None:
        runner = build_reasoning_contract_run(fixture_path, **runner_kwargs)
    else:
        runner = build_reasoning_contract_run(fixture_path, cases_path, **runner_kwargs)

    answer_review_status = str(runner["answer_review_status"])
    contract_summary = _contract_summary(runner.get("answer_contract_review"), answer_review_status)
    result = {
        "mode": MODE,
        "output_schema": OUTPUT_SCHEMA,
        "fixture": runner["fixture"],
        "reasoning_cases": runner["reasoning_cases"],
        "query_id": runner["query_id"],
        "query": runner["query"],
        "overall_status": runner["overall_status"],
        "answer_review_status": answer_review_status,
        "answer_source": _answer_source(runner.get("answer_contract_review")),
        "role_coverage_summary": _role_summary(runner["role_coverage"]),
        "contract_summary": contract_summary,
        "validator_summaries": _validator_summary(runner["validators"]),
        "limitations": list(LIMITATIONS),
    }
    result["review_text"] = _render_review_text(result)
    return result
