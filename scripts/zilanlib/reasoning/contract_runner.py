from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from zilanlib.reasoning import (
    agama_evidence_checker,
    cognitive_analysis_mapper,
    collected_topics_analyzer,
    hetuvidya_validator,
    madhyamaka_critique_engine,
)
from zilanlib.reasoning.validator_output import (
    build_not_applicable_validator_output,
    build_validator_output,
)
from zilanlib.semantic.answer_contract_review import build_answer_contract_review
from zilanlib.semantic.retrieval_dry_run import DEFAULT_FIXTURE, ROOT, FixtureError, build_dry_run
from zilanlib.semantic.role_coverage import build_role_coverage

MODE = "reasoning-contract-runner-v0"
OUTPUT_SCHEMA = "reasoning-contract-runner-output-v0"
LIMITATIONS = (
    "Local fixture runner only; no answer generation, provider calls, embeddings, vector search, or reranking.",
    "Answer contracts are minimum explicitness checks and do not grade doctrinal correctness.",
    "Hetuvidya, Collected Topics, Madhyamaka, cognitive-analysis, and Agama evidence structured validators are wired "
    "in v0; other families use retrieval, role coverage, and answer contracts.",
    "This runner does not change platform validation status.",
)


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _answer_source_count(
    *,
    answer_text: str | None,
    answer_file: Path | None,
    sample_id: str | None,
) -> int:
    return sum(source is not None for source in (answer_text, answer_file, sample_id))


def _chunk_reasoning_roles(chunk: dict[str, Any]) -> list[str]:
    metadata = chunk.get("metadata")
    if not isinstance(metadata, dict):
        return []
    roles = metadata.get("reasoning_roles", [])
    if not isinstance(roles, list):
        return []
    return [role for role in roles if isinstance(role, str)]


def _reasoning_case_id(chunk: dict[str, Any]) -> str | None:
    metadata = chunk.get("metadata")
    if isinstance(metadata, dict):
        metadata_case_id = metadata.get("reasoning_case_id")
        if isinstance(metadata_case_id, str) and metadata_case_id.startswith("ZR-"):
            return metadata_case_id

    chunk_id = chunk.get("chunk_id")
    if not isinstance(chunk_id, str):
        return None
    parts = chunk_id.split(":")
    if len(parts) < 2 or parts[0] != "reasoning" or not parts[1].startswith("ZR-"):
        return None
    return parts[1]


def _reasoning_case_ids_for_role(dry_run: dict[str, Any], role: str) -> list[str]:
    needs = dry_run.get("needs", [])
    if isinstance(needs, list) and role not in needs:
        return []

    case_ids: list[str] = []
    for chunk in dry_run.get("chunks", []):
        if not isinstance(chunk, dict) or role not in _chunk_reasoning_roles(chunk):
            continue
        case_id = _reasoning_case_id(chunk)
        if case_id is not None and case_id not in case_ids:
            case_ids.append(case_id)
    return case_ids


def _build_answer_review(
    fixture_path: Path,
    dry_run: dict[str, Any],
    *,
    query_id: str | None,
    query: str | None,
    answer_text: str | None,
    answer_file: Path | None,
    sample_id: str | None,
) -> tuple[dict[str, Any] | None, str]:
    source_count = _answer_source_count(answer_text=answer_text, answer_file=answer_file, sample_id=sample_id)
    if source_count > 1:
        raise FixtureError("Provide at most one of --answer-text, --answer-file, or --sample-id.")

    answer_contracts = dry_run.get("answer_contracts", {})
    has_answer_contracts = isinstance(answer_contracts, dict) and bool(answer_contracts)
    answer_boundary_contracts = dry_run.get("answer_boundary_contracts", {})
    has_answer_boundary_contracts = isinstance(answer_boundary_contracts, dict) and bool(answer_boundary_contracts)

    if source_count == 0:
        return None, "review_needed" if has_answer_contracts or has_answer_boundary_contracts else "no_answer_contracts"

    review = build_answer_contract_review(
        fixture_path,
        query_id=query_id,
        query=query,
        answer_text=answer_text,
        answer_file=answer_file,
        sample_id=sample_id,
    )
    return review, str(review.get("overall_status", "unknown"))


@dataclass(frozen=True)
class _ValidatorSpec:
    role: str
    result_key: str
    payload_key: str
    module: Any
    build_case: Callable[[Path, str, Path, Path | None], dict[str, Any]]


def _build_hetuvidya_case(
    cases_path: Path,
    case_id: str,
    _retrieval_fixture_path: Path,
    _source_root: Path | None,
) -> dict[str, Any]:
    return hetuvidya_validator.build_hetuvidya_validation(cases_path, case_id=case_id)


def _build_collected_topics_case(
    cases_path: Path,
    case_id: str,
    _retrieval_fixture_path: Path,
    _source_root: Path | None,
) -> dict[str, Any]:
    return collected_topics_analyzer.build_collected_topics_analysis(cases_path, case_id=case_id)


def _build_madhyamaka_case(
    cases_path: Path,
    case_id: str,
    _retrieval_fixture_path: Path,
    _source_root: Path | None,
) -> dict[str, Any]:
    return madhyamaka_critique_engine.build_madhyamaka_critique(cases_path, case_id=case_id)


def _build_cognitive_analysis_case(
    cases_path: Path,
    case_id: str,
    _retrieval_fixture_path: Path,
    _source_root: Path | None,
) -> dict[str, Any]:
    return cognitive_analysis_mapper.build_cognitive_analysis_mapping(cases_path, case_id=case_id)


def _build_agama_evidence_case(
    cases_path: Path,
    case_id: str,
    retrieval_fixture_path: Path,
    source_root: Path | None,
) -> dict[str, Any]:
    return agama_evidence_checker.build_agama_evidence_check(
        cases_path,
        case_id=case_id,
        retrieval_fixture_path=retrieval_fixture_path,
        source_root=source_root,
    )


_VALIDATOR_SPECS = (
    _ValidatorSpec(
        role="hetuvidya",
        result_key="validations",
        payload_key="validations",
        module=hetuvidya_validator,
        build_case=_build_hetuvidya_case,
    ),
    _ValidatorSpec(
        role="collected_topics",
        result_key="analyses",
        payload_key="analyses",
        module=collected_topics_analyzer,
        build_case=_build_collected_topics_case,
    ),
    _ValidatorSpec(
        role="madhyamaka_prasanga",
        result_key="critiques",
        payload_key="critiques",
        module=madhyamaka_critique_engine,
        build_case=_build_madhyamaka_case,
    ),
    _ValidatorSpec(
        role="cognitive_analysis",
        result_key="mappings",
        payload_key="mappings",
        module=cognitive_analysis_mapper,
        build_case=_build_cognitive_analysis_case,
    ),
    _ValidatorSpec(
        role="agama_evidence",
        result_key="evidence_reviews",
        payload_key="evidence_reviews",
        module=agama_evidence_checker,
        build_case=_build_agama_evidence_case,
    ),
)


def _build_validator_from_spec(
    spec: _ValidatorSpec,
    cases_path: Path,
    dry_run: dict[str, Any],
    retrieval_fixture_path: Path,
    source_root: Path | None,
) -> dict[str, Any]:
    case_ids = _reasoning_case_ids_for_role(dry_run, spec.role)
    if not case_ids:
        return build_not_applicable_validator_output(
            validator=spec.module.VALIDATOR,
            contract_family=spec.module.CONTRACT_FAMILY,
            output_schema=spec.module.OUTPUT_SCHEMA,
            source=_display_path(cases_path),
            payload_key=spec.payload_key,
            limitation=f"No selected reasoning case with {spec.role} role was found for this query fixture.",
        )

    payload: list[dict[str, Any]] = []
    mode = ""
    output_schema = ""
    source = _display_path(cases_path)
    limitations: list[str] = []

    for case_id in case_ids:
        result = spec.build_case(cases_path, case_id, retrieval_fixture_path, source_root)
        mode = str(result["mode"])
        output_schema = str(result["output_schema"])
        source = str(result["source"])
        payload.extend(result[spec.result_key])
        for limitation in result["limitations"]:
            if limitation not in limitations:
                limitations.append(limitation)

    return build_validator_output(
        validator=spec.module.VALIDATOR,
        contract_family=spec.module.CONTRACT_FAMILY,
        mode=mode,
        output_schema=output_schema,
        source=source,
        case_id=None,
        payload_key=spec.payload_key,
        payload=payload,
        limitations=limitations,
    )


def _build_validators(
    cases_path: Path,
    dry_run: dict[str, Any],
    retrieval_fixture_path: Path,
    source_root: Path | None,
) -> dict[str, dict[str, Any]]:
    return {
        spec.role: _build_validator_from_spec(spec, cases_path, dry_run, retrieval_fixture_path, source_root)
        for spec in _VALIDATOR_SPECS
    }


def _build_answer_validator_alignment(
    dry_run: dict[str, Any],
    answer_review_status: str,
    validators: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    if answer_review_status != "pass":
        return {
            "status": "not_applicable",
            "checked_roles": [],
            "missing_validator_cases": [],
            "limitations": [
                "Alignment is checked only after answer_contract_review passes.",
            ],
        }

    needs = dry_run.get("needs", [])
    need_set = {need for need in needs if isinstance(need, str)} if isinstance(needs, list) else set()
    checked_roles: list[dict[str, Any]] = []
    missing_validator_cases: list[dict[str, Any]] = []

    for spec in _VALIDATOR_SPECS:
        if spec.role not in need_set:
            continue

        validator = validators.get(spec.role, {})
        validator_status = str(validator.get("status", "missing"))
        case_ids_value = validator.get("case_ids", [])
        case_ids = (
            [case_id for case_id in case_ids_value if isinstance(case_id, str)]
            if isinstance(case_ids_value, list)
            else []
        )
        checked_role = {
            "role": spec.role,
            "validator": spec.module.VALIDATOR,
            "validator_status": validator_status,
            "case_ids": case_ids,
        }
        checked_roles.append(checked_role)

        if validator_status != "run" or not case_ids:
            missing_validator_cases.append(
                {
                    **checked_role,
                    "reason": "answer_contract_passed_without_structured_validator_case",
                }
            )

    return {
        "status": "fail" if missing_validator_cases else "pass",
        "checked_roles": checked_roles,
        "missing_validator_cases": missing_validator_cases,
        "limitations": [
            "Checks only structured validator roles declared in retrieval fixture needs after answer contracts pass.",
            "This is a consistency guard; it does not grade doctrinal correctness.",
        ],
    }


def _overall_status(
    role_coverage: dict[str, Any],
    answer_review_status: str,
    answer_validator_alignment_status: str,
) -> str:
    if role_coverage.get("missing_needs"):
        return "fail"
    if answer_review_status == "fail":
        return "fail"
    if answer_validator_alignment_status == "fail":
        return "fail"
    if answer_review_status == "review_needed":
        return "review_needed"
    return "pass"


def build_reasoning_contract_run(
    fixture_path: Path = DEFAULT_FIXTURE,
    cases_path: Path = hetuvidya_validator.DEFAULT_CASES,
    *,
    query_id: str | None = None,
    query: str | None = None,
    limit: int | None = None,
    answer_text: str | None = None,
    answer_file: Path | None = None,
    sample_id: str | None = None,
    source_root: Path | None = agama_evidence_checker.DEFAULT_SOURCE_ROOT,
) -> dict[str, Any]:
    """Run the local reasoning-contract fixture checks for one semantic query."""

    dry_run = build_dry_run(fixture_path, query_id=query_id, query=query, limit=limit)
    role_coverage = build_role_coverage(fixture_path, query_id=query_id, query=query, limit=limit)
    answer_contract_review, answer_review_status = _build_answer_review(
        fixture_path,
        dry_run,
        query_id=query_id,
        query=query,
        answer_text=answer_text,
        answer_file=answer_file,
        sample_id=sample_id,
    )
    validators = _build_validators(cases_path, dry_run, fixture_path, source_root)
    answer_validator_alignment = _build_answer_validator_alignment(dry_run, answer_review_status, validators)
    status = _overall_status(role_coverage, answer_review_status, str(answer_validator_alignment["status"]))

    return {
        "mode": MODE,
        "output_schema": OUTPUT_SCHEMA,
        "fixture": dry_run["fixture"],
        "reasoning_cases": _display_path(cases_path),
        "query_id": dry_run["query_id"],
        "query": dry_run["query"],
        "overall_status": status,
        "retrieval": dry_run,
        "role_coverage": role_coverage,
        "answer_review_status": answer_review_status,
        "answer_contract_review": answer_contract_review,
        "answer_validator_alignment": answer_validator_alignment,
        "validators": validators,
        "limitations": list(LIMITATIONS),
    }
