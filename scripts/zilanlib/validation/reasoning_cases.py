from __future__ import annotations

import re
from pathlib import Path

from zilanlib.validation.runtime_evidence import REGRESSION_CASES
from zilanlib.yaml_io import is_non_empty_string_list, load_yaml_for_validation

REASONING_CASES_PATH = "tests/reasoning_cases.yaml"
ALLOWED_REASONING_CONTRACTS = (
    "agama_evidence",
    "cognitive_analysis",
    "collected_topics",
    "hetuvidya",
    "madhyamaka_prasanga",
)
ALLOWED_HETUVIDYA_RESULTS = (
    "positive_reason",
    "reason_unestablished",
    "non_pervasive",
    "inconclusive_or_contradictory",
    "boundary_only",
)
ALLOWED_REASONING_CHECK_STATUSES = ("pass", "fail", "boundary", "not_applicable")


def check_hetuvidya_contract(case_id: str, expected: dict[str, object], failures: list[str]) -> None:
    hetuvidya = expected.get("hetuvidya")
    if not isinstance(hetuvidya, dict):
        failures.append(f"{REASONING_CASES_PATH} {case_id} missing expected.hetuvidya mapping.")
        return

    for field in ("subject", "predicate", "reason"):
        if not isinstance(hetuvidya.get(field), str) or not hetuvidya[field]:
            failures.append(f"{REASONING_CASES_PATH} {case_id} expected.hetuvidya.{field} must be a string.")

    result = hetuvidya.get("result")
    if result not in ALLOWED_HETUVIDYA_RESULTS:
        failures.append(
            f"{REASONING_CASES_PATH} {case_id} expected.hetuvidya.result must be one of "
            f"{', '.join(ALLOWED_HETUVIDYA_RESULTS)}."
        )

    checks = hetuvidya.get("checks")
    if not isinstance(checks, dict):
        failures.append(f"{REASONING_CASES_PATH} {case_id} missing expected.hetuvidya.checks mapping.")
        return

    for field in ("paksa_dharmata", "sapaksa_sattva", "vipaksa_asattva"):
        if checks.get(field) not in ALLOWED_REASONING_CHECK_STATUSES:
            failures.append(
                f"{REASONING_CASES_PATH} {case_id} expected.hetuvidya.checks.{field} must be one of "
                f"{', '.join(ALLOWED_REASONING_CHECK_STATUSES)}."
            )


def check_collected_topics_contract(case_id: str, expected: dict[str, object], failures: list[str]) -> None:
    collected_topics = expected.get("collected_topics")
    if not isinstance(collected_topics, dict):
        failures.append(f"{REASONING_CASES_PATH} {case_id} missing expected.collected_topics mapping.")
        return

    if not is_non_empty_string_list(collected_topics.get("concepts")):
        failures.append(f"{REASONING_CASES_PATH} {case_id} expected.collected_topics.concepts must be a list.")
    relation_checks = collected_topics.get("relation_checks")
    if not isinstance(relation_checks, dict) or not relation_checks:
        failures.append(
            f"{REASONING_CASES_PATH} {case_id} expected.collected_topics.relation_checks must be a mapping."
        )
    error_type = collected_topics.get("error_type")
    if error_type is not None and (not isinstance(error_type, str) or not error_type):
        failures.append(f"{REASONING_CASES_PATH} {case_id} expected.collected_topics.error_type must be a string.")


def check_cognitive_analysis_contract(case_id: str, expected: dict[str, object], failures: list[str]) -> None:
    cognitive_analysis = expected.get("cognitive_analysis")
    if not isinstance(cognitive_analysis, dict):
        failures.append(f"{REASONING_CASES_PATH} {case_id} missing expected.cognitive_analysis mapping.")
        return

    chain = cognitive_analysis.get("chain")
    if chain != ["触", "作意", "受", "想", "思"]:
        failures.append(
            f"{REASONING_CASES_PATH} {case_id} expected.cognitive_analysis.chain must be "
            "['触', '作意', '受', '想', '思']."
        )
    for field in ("afflictions", "corrective_factors"):
        if not is_non_empty_string_list(cognitive_analysis.get(field)):
            failures.append(
                f"{REASONING_CASES_PATH} {case_id} expected.cognitive_analysis.{field} must be a list."
            )


def check_madhyamaka_prasanga_contract(case_id: str, expected: dict[str, object], failures: list[str]) -> None:
    madhyamaka_prasanga = expected.get("madhyamaka_prasanga")
    if not isinstance(madhyamaka_prasanga, dict):
        failures.append(f"{REASONING_CASES_PATH} {case_id} missing expected.madhyamaka_prasanga mapping.")
        return

    if not isinstance(madhyamaka_prasanga.get("opponent_premise"), str) or not madhyamaka_prasanga[
        "opponent_premise"
    ]:
        failures.append(
            f"{REASONING_CASES_PATH} {case_id} expected.madhyamaka_prasanga.opponent_premise must be a string."
        )
    for field in ("accepted_commitments", "contradiction"):
        if not is_non_empty_string_list(madhyamaka_prasanga.get(field)):
            failures.append(
                f"{REASONING_CASES_PATH} {case_id} expected.madhyamaka_prasanga.{field} must be a list."
            )
    if madhyamaka_prasanga.get("no_independent_thesis") is not True:
        failures.append(
            f"{REASONING_CASES_PATH} {case_id} expected.madhyamaka_prasanga.no_independent_thesis must be true."
        )


def check_agama_evidence_contract(case_id: str, expected: dict[str, object], failures: list[str]) -> None:
    agama_evidence = expected.get("agama_evidence")
    if not isinstance(agama_evidence, dict):
        failures.append(f"{REASONING_CASES_PATH} {case_id} missing expected.agama_evidence mapping.")
        return

    for field in ("citation_required", "collation_boundary"):
        if not isinstance(agama_evidence.get(field), bool):
            failures.append(f"{REASONING_CASES_PATH} {case_id} expected.agama_evidence.{field} must be boolean.")
    if not isinstance(agama_evidence.get("search_scope"), str) or not agama_evidence["search_scope"]:
        failures.append(f"{REASONING_CASES_PATH} {case_id} expected.agama_evidence.search_scope must be a string.")


def validate_reasoning_cases(root: Path, failures: list[str], warnings: list[str], strict_yaml: bool) -> None:
    data = load_yaml_for_validation(root, REASONING_CASES_PATH, failures, warnings, strict_yaml)
    if data is None:
        return
    if not isinstance(data, dict):
        failures.append(f"{REASONING_CASES_PATH} must be a mapping.")
        return
    if data.get("version") != 1:
        failures.append(f"{REASONING_CASES_PATH} version must be 1.")

    source = data.get("source")
    if not isinstance(source, str) or not (root / source).exists():
        failures.append(f"{REASONING_CASES_PATH} source must reference an existing local file.")
    if not isinstance(data.get("purpose"), str) or not data["purpose"]:
        failures.append(f"{REASONING_CASES_PATH} purpose must be a non-empty string.")

    cases = data.get("cases")
    if not isinstance(cases, list) or not cases:
        failures.append(f"{REASONING_CASES_PATH} must contain a non-empty cases list.")
        return

    seen_ids: set[str] = set()
    for item in cases:
        if not isinstance(item, dict):
            failures.append(f"{REASONING_CASES_PATH} contains a non-mapping case.")
            continue

        case_id = item.get("id")
        if not isinstance(case_id, str) or not re.fullmatch(r"ZR-\d{2}", case_id):
            failures.append(f"{REASONING_CASES_PATH} contains a case without a ZR-XX id.")
            continue
        if case_id in seen_ids:
            failures.append(f"{REASONING_CASES_PATH} contains duplicate case id: {case_id}")
        seen_ids.add(case_id)

        for field in ("title", "prompt"):
            if not isinstance(item.get(field), str) or not item[field]:
                failures.append(f"{REASONING_CASES_PATH} {case_id} missing string field: {field}")

        source_regression_cases = item.get("source_regression_cases", [])
        if not isinstance(source_regression_cases, list) or not all(
            isinstance(case, str) and case in REGRESSION_CASES for case in source_regression_cases
        ):
            failures.append(
                f"{REASONING_CASES_PATH} {case_id} source_regression_cases must reference known ZC cases."
            )

        contracts = item.get("contracts")
        if not isinstance(contracts, list) or not contracts:
            failures.append(f"{REASONING_CASES_PATH} {case_id} contracts must be a non-empty list.")
            continue
        invalid_contracts = [
            contract
            for contract in contracts
            if not isinstance(contract, str) or contract not in ALLOWED_REASONING_CONTRACTS
        ]
        if invalid_contracts:
            failures.append(f"{REASONING_CASES_PATH} {case_id} has invalid contracts: {invalid_contracts}")

        reference_files = item.get("reference_files")
        if not isinstance(reference_files, list) or not reference_files:
            failures.append(f"{REASONING_CASES_PATH} {case_id} reference_files must be a non-empty list.")
        else:
            for rel_path in reference_files:
                if not isinstance(rel_path, str) or not (root / rel_path).exists():
                    failures.append(f"{REASONING_CASES_PATH} {case_id} references missing path: {rel_path}")

        expected = item.get("expected")
        if not isinstance(expected, dict):
            failures.append(f"{REASONING_CASES_PATH} {case_id} missing expected mapping.")
            continue
        if not isinstance(expected.get("boundary_statement"), bool):
            failures.append(f"{REASONING_CASES_PATH} {case_id} expected.boundary_statement must be boolean.")
        if not is_non_empty_string_list(expected.get("structure")):
            failures.append(f"{REASONING_CASES_PATH} {case_id} expected.structure must be a list.")

        if "hetuvidya" in contracts:
            check_hetuvidya_contract(case_id, expected, failures)
        if "collected_topics" in contracts:
            check_collected_topics_contract(case_id, expected, failures)
        if "cognitive_analysis" in contracts:
            check_cognitive_analysis_contract(case_id, expected, failures)
        if "madhyamaka_prasanga" in contracts:
            check_madhyamaka_prasanga_contract(case_id, expected, failures)
        if "agama_evidence" in contracts:
            check_agama_evidence_contract(case_id, expected, failures)


_check_hetuvidya_contract = check_hetuvidya_contract
_check_collected_topics_contract = check_collected_topics_contract
_check_cognitive_analysis_contract = check_cognitive_analysis_contract
_check_madhyamaka_prasanga_contract = check_madhyamaka_prasanga_contract
_check_agama_evidence_contract = check_agama_evidence_contract
_check_reasoning_cases_yaml = validate_reasoning_cases