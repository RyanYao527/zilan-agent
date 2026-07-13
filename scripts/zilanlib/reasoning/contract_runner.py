from __future__ import annotations

from pathlib import Path
from typing import Any

import agama_evidence_checker
import cognitive_analysis_mapper
from reasoning_validator_output import (
    build_not_applicable_validator_output,
    build_validator_output,
)

from zilanlib.reasoning import collected_topics_analyzer, hetuvidya_validator, madhyamaka_critique_engine
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

    if source_count == 0:
        return None, "review_needed" if has_answer_contracts else "no_answer_contracts"

    review = build_answer_contract_review(
        fixture_path,
        query_id=query_id,
        query=query,
        answer_text=answer_text,
        answer_file=answer_file,
        sample_id=sample_id,
    )
    return review, str(review.get("overall_status", "unknown"))


def _build_hetuvidya_validator(cases_path: Path, dry_run: dict[str, Any]) -> dict[str, Any]:
    case_ids = _reasoning_case_ids_for_role(dry_run, "hetuvidya")
    if not case_ids:
        return build_not_applicable_validator_output(
            validator=hetuvidya_validator.VALIDATOR,
            contract_family=hetuvidya_validator.CONTRACT_FAMILY,
            output_schema=hetuvidya_validator.OUTPUT_SCHEMA,
            source=_display_path(cases_path),
            payload_key="validations",
            limitation="No selected reasoning case with hetuvidya role was found for this query fixture.",
        )

    validations: list[dict[str, Any]] = []
    mode = ""
    output_schema = ""
    source = _display_path(cases_path)
    limitations: list[str] = []

    for case_id in case_ids:
        result = hetuvidya_validator.build_hetuvidya_validation(cases_path, case_id=case_id)
        mode = result["mode"]
        output_schema = result["output_schema"]
        source = result["source"]
        validations.extend(result["validations"])
        for limitation in result["limitations"]:
            if limitation not in limitations:
                limitations.append(limitation)

    return build_validator_output(
        validator=hetuvidya_validator.VALIDATOR,
        contract_family=hetuvidya_validator.CONTRACT_FAMILY,
        mode=mode,
        output_schema=output_schema,
        source=source,
        case_id=None,
        payload_key="validations",
        payload=validations,
        limitations=limitations,
    )


def _build_cognitive_analysis_validator(cases_path: Path, dry_run: dict[str, Any]) -> dict[str, Any]:
    case_ids = _reasoning_case_ids_for_role(dry_run, "cognitive_analysis")
    if not case_ids:
        return build_not_applicable_validator_output(
            validator=cognitive_analysis_mapper.VALIDATOR,
            contract_family=cognitive_analysis_mapper.CONTRACT_FAMILY,
            output_schema=cognitive_analysis_mapper.OUTPUT_SCHEMA,
            source=_display_path(cases_path),
            payload_key="mappings",
            limitation="No selected reasoning case with cognitive_analysis role was found for this query fixture.",
        )

    mappings: list[dict[str, Any]] = []
    mode = ""
    output_schema = ""
    source = _display_path(cases_path)
    limitations: list[str] = []

    for case_id in case_ids:
        result = cognitive_analysis_mapper.build_cognitive_analysis_mapping(cases_path, case_id=case_id)
        mode = result["mode"]
        output_schema = result["output_schema"]
        source = result["source"]
        mappings.extend(result["mappings"])
        for limitation in result["limitations"]:
            if limitation not in limitations:
                limitations.append(limitation)

    return build_validator_output(
        validator=cognitive_analysis_mapper.VALIDATOR,
        contract_family=cognitive_analysis_mapper.CONTRACT_FAMILY,
        mode=mode,
        output_schema=output_schema,
        source=source,
        case_id=None,
        payload_key="mappings",
        payload=mappings,
        limitations=limitations,
    )


def _build_collected_topics_validator(cases_path: Path, dry_run: dict[str, Any]) -> dict[str, Any]:
    case_ids = _reasoning_case_ids_for_role(dry_run, "collected_topics")
    if not case_ids:
        return build_not_applicable_validator_output(
            validator=collected_topics_analyzer.VALIDATOR,
            contract_family=collected_topics_analyzer.CONTRACT_FAMILY,
            output_schema=collected_topics_analyzer.OUTPUT_SCHEMA,
            source=_display_path(cases_path),
            payload_key="analyses",
            limitation="No selected reasoning case with collected_topics role was found for this query fixture.",
        )

    analyses: list[dict[str, Any]] = []
    mode = ""
    output_schema = ""
    source = _display_path(cases_path)
    limitations: list[str] = []

    for case_id in case_ids:
        result = collected_topics_analyzer.build_collected_topics_analysis(cases_path, case_id=case_id)
        mode = result["mode"]
        output_schema = result["output_schema"]
        source = result["source"]
        analyses.extend(result["analyses"])
        for limitation in result["limitations"]:
            if limitation not in limitations:
                limitations.append(limitation)

    return build_validator_output(
        validator=collected_topics_analyzer.VALIDATOR,
        contract_family=collected_topics_analyzer.CONTRACT_FAMILY,
        mode=mode,
        output_schema=output_schema,
        source=source,
        case_id=None,
        payload_key="analyses",
        payload=analyses,
        limitations=limitations,
    )



def _build_madhyamaka_prasanga_validator(cases_path: Path, dry_run: dict[str, Any]) -> dict[str, Any]:
    case_ids = _reasoning_case_ids_for_role(dry_run, "madhyamaka_prasanga")
    if not case_ids:
        return build_not_applicable_validator_output(
            validator=madhyamaka_critique_engine.VALIDATOR,
            contract_family=madhyamaka_critique_engine.CONTRACT_FAMILY,
            output_schema=madhyamaka_critique_engine.OUTPUT_SCHEMA,
            source=_display_path(cases_path),
            payload_key="critiques",
            limitation="No selected reasoning case with madhyamaka_prasanga role was found for this query fixture.",
        )

    critiques: list[dict[str, Any]] = []
    mode = ""
    output_schema = ""
    source = _display_path(cases_path)
    limitations: list[str] = []

    for case_id in case_ids:
        result = madhyamaka_critique_engine.build_madhyamaka_critique(cases_path, case_id=case_id)
        mode = result["mode"]
        output_schema = result["output_schema"]
        source = result["source"]
        critiques.extend(result["critiques"])
        for limitation in result["limitations"]:
            if limitation not in limitations:
                limitations.append(limitation)

    return build_validator_output(
        validator=madhyamaka_critique_engine.VALIDATOR,
        contract_family=madhyamaka_critique_engine.CONTRACT_FAMILY,
        mode=mode,
        output_schema=output_schema,
        source=source,
        case_id=None,
        payload_key="critiques",
        payload=critiques,
        limitations=limitations,
    )

def _build_agama_evidence_validator(cases_path: Path, dry_run: dict[str, Any]) -> dict[str, Any]:
    case_ids = _reasoning_case_ids_for_role(dry_run, "agama_evidence")
    if not case_ids:
        return build_not_applicable_validator_output(
            validator=agama_evidence_checker.VALIDATOR,
            contract_family=agama_evidence_checker.CONTRACT_FAMILY,
            output_schema=agama_evidence_checker.OUTPUT_SCHEMA,
            source=_display_path(cases_path),
            payload_key="evidence_reviews",
            limitation="No selected reasoning case with agama_evidence role was found for this query fixture.",
        )

    evidence_reviews: list[dict[str, Any]] = []
    mode = ""
    output_schema = ""
    source = _display_path(cases_path)
    limitations: list[str] = []

    for case_id in case_ids:
        result = agama_evidence_checker.build_agama_evidence_check(cases_path, case_id=case_id)
        mode = result["mode"]
        output_schema = result["output_schema"]
        source = result["source"]
        evidence_reviews.extend(result["evidence_reviews"])
        for limitation in result["limitations"]:
            if limitation not in limitations:
                limitations.append(limitation)

    return build_validator_output(
        validator=agama_evidence_checker.VALIDATOR,
        contract_family=agama_evidence_checker.CONTRACT_FAMILY,
        mode=mode,
        output_schema=output_schema,
        source=source,
        case_id=None,
        payload_key="evidence_reviews",
        payload=evidence_reviews,
        limitations=limitations,
    )

def _overall_status(role_coverage: dict[str, Any], answer_review_status: str) -> str:
    if role_coverage.get("missing_needs"):
        return "fail"
    if answer_review_status == "fail":
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
    validators = {
        "hetuvidya": _build_hetuvidya_validator(cases_path, dry_run),
        "collected_topics": _build_collected_topics_validator(cases_path, dry_run),
        "madhyamaka_prasanga": _build_madhyamaka_prasanga_validator(cases_path, dry_run),
        "cognitive_analysis": _build_cognitive_analysis_validator(cases_path, dry_run),
        "agama_evidence": _build_agama_evidence_validator(cases_path, dry_run),
    }
    status = _overall_status(role_coverage, answer_review_status)

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
        "validators": validators,
        "limitations": list(LIMITATIONS),
    }
