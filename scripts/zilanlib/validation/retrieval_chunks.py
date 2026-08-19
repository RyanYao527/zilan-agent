from __future__ import annotations

import hashlib
import re
from collections.abc import Container
from pathlib import Path
from typing import cast

from zilanlib.agama.search import _line_section_map
from zilanlib.validation.reasoning_cases import ALLOWED_REASONING_CONTRACTS
from zilanlib.yaml_io import is_non_empty_int_list, is_non_empty_string_list, load_yaml_for_validation

RETRIEVAL_CHUNKS_PATH = "tests/fixtures/retrieval_chunks/semantic_chunks.yaml"
ALLOWED_RETRIEVAL_CHUNK_TYPES = ("agama_passage", "argument_unit", "context_topic", "reasoning_case")
ALLOWED_RETRIEVAL_NEEDS = (*ALLOWED_REASONING_CONTRACTS, "practice_boundary")
ALLOWED_RETRIEVAL_NON_CHUNK_NEEDS = ("practice_boundary",)
ALLOWED_ANSWER_SAMPLE_STATUSES = ("pass", "fail")
RETRIEVAL_HASH_ALGORITHM = "sha256"
RETRIEVAL_SOURCE_SCRIPT = "scripts/search_agama.py"
RETRIEVAL_SOURCE_HASH_SCOPE = "legacy_alias_for_line_text_hash"
RETRIEVAL_LINE_TEXT_HASH_SCOPE = "trimmed_non_empty_lines_joined_with_lf"


def contains_membership(container: object, value: str) -> bool:
    return isinstance(container, Container) and value in container


def retrieval_line_text_hash(source_lines: list[str], start_line: int, end_line: int) -> str:
    text = "\n".join(line.strip() for line in source_lines[start_line - 1 : end_line] if line.strip())
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    return f"{RETRIEVAL_HASH_ALGORITHM}:{digest}"


def retrieval_section_label(section_marker: object, section_title: object) -> str | None:
    marker = section_marker if isinstance(section_marker, str) and section_marker else None
    title = section_title if isinstance(section_title, str) and section_title else None
    if marker and title:
        return f"{marker}{title}"
    if marker:
        return marker
    return title


def check_agama_section_metadata(
    *,
    chunk_id: str,
    metadata: dict[str, object],
    source_lines: list[str],
    start_line: int,
    failures: list[str],
) -> None:
    for field in ("section_marker", "section_title"):
        value = metadata.get(field)
        if value is not None and not isinstance(value, str):
            failures.append(f"{RETRIEVAL_CHUNKS_PATH} {chunk_id} metadata.{field} must be a string or null.")

    source_section_marker, source_section_title = _line_section_map(source_lines).get(start_line, (None, None))
    expected_label = retrieval_section_label(source_section_marker, source_section_title)
    if metadata.get("section_marker") != source_section_marker:
        failures.append(f"{RETRIEVAL_CHUNKS_PATH} {chunk_id} metadata.section_marker must match source section.")
    if metadata.get("section_title") != source_section_title:
        failures.append(f"{RETRIEVAL_CHUNKS_PATH} {chunk_id} metadata.section_title must match source section.")
    if "section_label" not in metadata or metadata.get("section_label") != expected_label:
        failures.append(
            f"{RETRIEVAL_CHUNKS_PATH} {chunk_id} "
            "metadata.section_label must match section_marker and section_title."
        )


def check_agama_passage_provenance(
    *,
    chunk_id: str,
    metadata: dict[str, object],
    source_file: str,
    start_line: int,
    end_line: int,
    source_lines: list[str],
    failures: list[str],
) -> None:
    expected_hash = retrieval_line_text_hash(source_lines, start_line, end_line)
    source_hash = metadata.get("source_hash")
    line_text_hash = metadata.get("line_text_hash")

    if source_hash != expected_hash:
        failures.append(f"{RETRIEVAL_CHUNKS_PATH} {chunk_id} metadata.source_hash must match source range hash.")
    if line_text_hash != expected_hash:
        failures.append(f"{RETRIEVAL_CHUNKS_PATH} {chunk_id} metadata.line_text_hash must match source range hash.")
    if source_hash != line_text_hash:
        failures.append(f"{RETRIEVAL_CHUNKS_PATH} {chunk_id} metadata.source_hash must equal line_text_hash.")

    matched_lines_value = metadata.get("matched_lines")
    matched_lines_valid = is_non_empty_int_list(matched_lines_value)
    if not matched_lines_valid:
        failures.append(f"{RETRIEVAL_CHUNKS_PATH} {chunk_id} metadata.matched_lines must be a line-number list.")
    else:
        matched_lines = cast(list[int], matched_lines_value)
        out_of_range = [line for line in matched_lines if line < start_line or line > end_line]
        if out_of_range:
            failures.append(
                f"{RETRIEVAL_CHUNKS_PATH} {chunk_id} metadata.matched_lines must fall within the line range."
            )

    provenance = metadata.get("provenance")
    if not isinstance(provenance, dict):
        failures.append(f"{RETRIEVAL_CHUNKS_PATH} {chunk_id} metadata.provenance must be a mapping.")
        return

    if provenance.get("source_script") != RETRIEVAL_SOURCE_SCRIPT:
        failures.append(
            f"{RETRIEVAL_CHUNKS_PATH} {chunk_id} metadata.provenance.source_script must be "
            f"{RETRIEVAL_SOURCE_SCRIPT}."
        )
    if provenance.get("source_file") != source_file:
        failures.append(f"{RETRIEVAL_CHUNKS_PATH} {chunk_id} metadata.provenance.source_file must match source_file.")
    if provenance.get("line_range") != {"start": start_line, "end": end_line}:
        failures.append(f"{RETRIEVAL_CHUNKS_PATH} {chunk_id} metadata.provenance.line_range must match line range.")
    if matched_lines_valid:
        matched_lines = cast(list[int], matched_lines_value)
        if provenance.get("matched_lines") != matched_lines:
            failures.append(
                f"{RETRIEVAL_CHUNKS_PATH} {chunk_id} metadata.provenance.matched_lines must match "
                "metadata.matched_lines."
            )
    if provenance.get("hash_algorithm") != RETRIEVAL_HASH_ALGORITHM:
        failures.append(
            f"{RETRIEVAL_CHUNKS_PATH} {chunk_id} metadata.provenance.hash_algorithm must be "
            f"{RETRIEVAL_HASH_ALGORITHM}."
        )
    if provenance.get("line_text_hash") != expected_hash:
        failures.append(
            f"{RETRIEVAL_CHUNKS_PATH} {chunk_id} metadata.provenance.line_text_hash must match source range hash."
        )
    if provenance.get("source_hash_scope") != RETRIEVAL_SOURCE_HASH_SCOPE:
        failures.append(
            f"{RETRIEVAL_CHUNKS_PATH} {chunk_id} metadata.provenance.source_hash_scope must be "
            f"{RETRIEVAL_SOURCE_HASH_SCOPE}."
        )
    if provenance.get("line_text_hash_scope") != RETRIEVAL_LINE_TEXT_HASH_SCOPE:
        failures.append(
            f"{RETRIEVAL_CHUNKS_PATH} {chunk_id} metadata.provenance.line_text_hash_scope must be "
            f"{RETRIEVAL_LINE_TEXT_HASH_SCOPE}."
        )


def check_retrieval_chunk_metadata(
    case_id: str,
    chunk_type: object,
    metadata: object,
    failures: list[str],
    *,
    source_file: str | None = None,
    start_line: int | None = None,
    end_line: int | None = None,
    source_lines: list[str] | None = None,
) -> None:
    if not isinstance(metadata, dict):
        failures.append(f"{RETRIEVAL_CHUNKS_PATH} {case_id} metadata must be a mapping.")
        return

    if not is_non_empty_string_list(metadata.get("topics")):
        failures.append(f"{RETRIEVAL_CHUNKS_PATH} {case_id} metadata.topics must be a list.")

    roles_value = metadata.get("reasoning_roles")
    if not is_non_empty_string_list(roles_value):
        failures.append(f"{RETRIEVAL_CHUNKS_PATH} {case_id} metadata.reasoning_roles must be a list.")
    else:
        roles = cast(list[str], roles_value)
        invalid_roles = [role for role in roles if role not in ALLOWED_REASONING_CONTRACTS]
        if invalid_roles:
            failures.append(f"{RETRIEVAL_CHUNKS_PATH} {case_id} has invalid reasoning roles: {invalid_roles}")

    if chunk_type == "agama_passage":
        for field in ("collection", "cbeta_id", "juan"):
            if not isinstance(metadata.get(field), str) or not metadata[field]:
                failures.append(f"{RETRIEVAL_CHUNKS_PATH} {case_id} metadata.{field} must be a string.")
        cbeta_id = metadata.get("cbeta_id")
        if isinstance(cbeta_id, str) and not re.fullmatch(r"T\d{2}n\d{4}", cbeta_id):
            failures.append(f"{RETRIEVAL_CHUNKS_PATH} {case_id} metadata.cbeta_id is not a CBETA id.")
        if (
            isinstance(source_file, str)
            and isinstance(start_line, int)
            and isinstance(end_line, int)
            and isinstance(source_lines, list)
        ):
            check_agama_section_metadata(
                chunk_id=case_id,
                metadata=metadata,
                source_lines=source_lines,
                start_line=start_line,
                failures=failures,
            )
            check_agama_passage_provenance(
                chunk_id=case_id,
                metadata=metadata,
                source_file=source_file,
                start_line=start_line,
                end_line=end_line,
                source_lines=source_lines,
                failures=failures,
            )


def check_answer_samples(
    root: Path,
    query_id: str,
    samples: object,
    field_name: str,
    failures: list[str],
) -> None:
    if not isinstance(samples, list) or not samples:
        failures.append(f"{RETRIEVAL_CHUNKS_PATH} {query_id} {field_name} must be a non-empty list.")
        return

    seen_sample_ids: set[str] = set()
    for sample in samples:
        if not isinstance(sample, dict):
            failures.append(f"{RETRIEVAL_CHUNKS_PATH} {query_id} contains a non-mapping {field_name} item.")
            continue

        sample_id = sample.get("id")
        if not isinstance(sample_id, str) or not re.fullmatch(r"[a-z0-9][a-z0-9-]*", sample_id):
            failures.append(f"{RETRIEVAL_CHUNKS_PATH} {query_id} {field_name} id must be kebab-case.")
        elif sample_id in seen_sample_ids:
            failures.append(f"{RETRIEVAL_CHUNKS_PATH} {query_id} contains duplicate {field_name} id: {sample_id}")
        else:
            seen_sample_ids.add(sample_id)

        rel_file = sample.get("file")
        if not isinstance(rel_file, str) or not rel_file:
            failures.append(f"{RETRIEVAL_CHUNKS_PATH} {query_id} {field_name} {sample_id} missing file.")
        else:
            sample_path = root / rel_file
            try:
                sample_path.resolve().relative_to(root.resolve())
            except ValueError:
                failures.append(
                    f"{RETRIEVAL_CHUNKS_PATH} {query_id} {field_name} {sample_id} file must stay under repo root."
                )
            if not sample_path.exists() or not sample_path.is_file():
                failures.append(
                    f"{RETRIEVAL_CHUNKS_PATH} {query_id} {field_name} {sample_id} file missing: {rel_file}"
                )
            elif not sample_path.read_text(encoding="utf-8").strip():
                failures.append(
                    f"{RETRIEVAL_CHUNKS_PATH} {query_id} {field_name} {sample_id} file is empty: {rel_file}"
                )

        expected_status = sample.get("expected_status")
        if expected_status not in ALLOWED_ANSWER_SAMPLE_STATUSES:
            failures.append(
                f"{RETRIEVAL_CHUNKS_PATH} {query_id} {field_name} {sample_id} expected_status must be one of "
                f"{', '.join(ALLOWED_ANSWER_SAMPLE_STATUSES)}."
            )


def check_answer_contracts(query_id: str, contracts: object, field_name: str, failures: list[str]) -> None:
    if not isinstance(contracts, dict) or not contracts:
        failures.append(f"{RETRIEVAL_CHUNKS_PATH} {query_id} {field_name} must be a non-empty mapping.")
        return

    for key, contract in contracts.items():
        if not isinstance(key, str) or not re.fullmatch(r"[a-z0-9][a-z0-9_]*", key):
            failures.append(f"{RETRIEVAL_CHUNKS_PATH} {query_id} {field_name} key must be snake_case.")
            continue
        if not isinstance(contract, dict):
            failures.append(f"{RETRIEVAL_CHUNKS_PATH} {query_id} {field_name}.{key} must be a mapping.")
            continue
        if not isinstance(contract.get("description"), str) or not contract["description"]:
            failures.append(f"{RETRIEVAL_CHUNKS_PATH} {query_id} {field_name}.{key}.description must be a string.")
        if not is_non_empty_string_list(contract.get("required_terms")):
            failures.append(f"{RETRIEVAL_CHUNKS_PATH} {query_id} {field_name}.{key}.required_terms must be a list.")
        forbidden_terms = contract.get("forbidden_terms", [])
        if forbidden_terms and not is_non_empty_string_list(forbidden_terms):
            failures.append(
                f"{RETRIEVAL_CHUNKS_PATH} {query_id} {field_name}.{key}.forbidden_terms "
                "must be a list when present."
            )
        required_term_groups = contract.get("required_term_groups", [])
        if required_term_groups:
            if not isinstance(required_term_groups, list):
                failures.append(
                    f"{RETRIEVAL_CHUNKS_PATH} {query_id} {field_name}.{key}.required_term_groups "
                    "must be a list when present."
                )
            else:
                for index, group in enumerate(required_term_groups):
                    if not isinstance(group, dict):
                        failures.append(
                            f"{RETRIEVAL_CHUNKS_PATH} {query_id} "
                            f"{field_name}.{key}.required_term_groups[{index}] must be a mapping."
                        )
                        continue
                    label = group.get("label")
                    if not isinstance(label, str) or not re.fullmatch(r"[a-z0-9][a-z0-9_]*", label):
                        failures.append(
                            f"{RETRIEVAL_CHUNKS_PATH} {query_id} "
                            f"{field_name}.{key}.required_term_groups[{index}].label must be snake_case."
                        )
                    if not is_non_empty_string_list(group.get("terms")):
                        failures.append(
                            f"{RETRIEVAL_CHUNKS_PATH} {query_id} "
                            f"{field_name}.{key}.required_term_groups[{index}].terms "
                            "must be a non-empty string list."
                        )
        required_slots = contract.get("required_slots", [])
        if required_slots:
            if not isinstance(required_slots, list):
                failures.append(
                    f"{RETRIEVAL_CHUNKS_PATH} {query_id} {field_name}.{key}.required_slots "
                    "must be a list when present."
                )
                continue
            for index, slot in enumerate(required_slots):
                if not isinstance(slot, dict):
                    failures.append(
                        f"{RETRIEVAL_CHUNKS_PATH} {query_id} {field_name}.{key}.required_slots[{index}] "
                        "must be a mapping."
                    )
                    continue
                label = slot.get("label")
                if not isinstance(label, str) or not re.fullmatch(r"[a-z0-9][a-z0-9_]*", label):
                    failures.append(
                        f"{RETRIEVAL_CHUNKS_PATH} {query_id} {field_name}.{key}.required_slots[{index}].label "
                        "must be snake_case."
                    )
                if not is_non_empty_string_list(slot.get("terms")):
                    failures.append(
                        f"{RETRIEVAL_CHUNKS_PATH} {query_id} {field_name}.{key}.required_slots[{index}].terms "
                        "must be a non-empty string list."
                    )


def check_retrieval_queries(
    root: Path,
    queries: object,
    chunk_ids: set[str],
    failures: list[str],
) -> None:
    if not isinstance(queries, list) or not queries:
        failures.append(f"{RETRIEVAL_CHUNKS_PATH} must contain a non-empty queries list.")
        return

    seen_query_ids: set[str] = set()
    for item in queries:
        if not isinstance(item, dict):
            failures.append(f"{RETRIEVAL_CHUNKS_PATH} contains a non-mapping query.")
            continue

        query_id = item.get("id")
        if not isinstance(query_id, str) or not re.fullmatch(r"SRQ-\d{2}", query_id):
            failures.append(f"{RETRIEVAL_CHUNKS_PATH} contains a query without an SRQ-XX id.")
            continue
        if query_id in seen_query_ids:
            failures.append(f"{RETRIEVAL_CHUNKS_PATH} contains duplicate query id: {query_id}")
        seen_query_ids.add(query_id)

        if not isinstance(item.get("query"), str) or not item["query"]:
            failures.append(f"{RETRIEVAL_CHUNKS_PATH} {query_id} query must be a string.")

        needs = item.get("needs")
        if not is_non_empty_string_list(needs):
            failures.append(f"{RETRIEVAL_CHUNKS_PATH} {query_id} needs must be a list.")
        else:
            needs_list = cast(list[str], needs)
            invalid_needs = [need for need in needs_list if need not in ALLOWED_RETRIEVAL_NEEDS]
            if invalid_needs:
                failures.append(f"{RETRIEVAL_CHUNKS_PATH} {query_id} has invalid needs: {invalid_needs}")

        non_chunk_needs = item.get("non_chunk_needs", [])
        if non_chunk_needs:
            if not is_non_empty_string_list(non_chunk_needs):
                failures.append(f"{RETRIEVAL_CHUNKS_PATH} {query_id} non_chunk_needs must be a list.")
            else:
                non_chunk_needs_list = cast(list[str], non_chunk_needs)
                invalid_non_chunk_needs = [
                    need for need in non_chunk_needs_list if need not in ALLOWED_RETRIEVAL_NON_CHUNK_NEEDS
                ]
                if invalid_non_chunk_needs:
                    failures.append(
                        f"{RETRIEVAL_CHUNKS_PATH} {query_id} has invalid non_chunk_needs: "
                        f"{invalid_non_chunk_needs}"
                    )
                missing_non_chunk_needs = [
                    need for need in non_chunk_needs_list if not contains_membership(needs, need)
                ]
                if missing_non_chunk_needs:
                    failures.append(
                        f"{RETRIEVAL_CHUNKS_PATH} {query_id} non_chunk_needs are not listed in needs: "
                        f"{missing_non_chunk_needs}"
                    )

        answer_boundary_contracts = item.get("answer_boundary_contracts", {})
        if answer_boundary_contracts:
            if not isinstance(answer_boundary_contracts, dict):
                failures.append(f"{RETRIEVAL_CHUNKS_PATH} {query_id} answer_boundary_contracts must be a mapping.")
            elif not non_chunk_needs:
                failures.append(
                    f"{RETRIEVAL_CHUNKS_PATH} {query_id} answer_boundary_contracts requires non_chunk_needs."
                )
            else:
                invalid_contract_keys = [
                    key
                    for key in answer_boundary_contracts
                    if not isinstance(key, str) or not contains_membership(non_chunk_needs, key)
                ]
                if invalid_contract_keys:
                    failures.append(
                        f"{RETRIEVAL_CHUNKS_PATH} {query_id} has answer boundary contracts outside "
                        f"non_chunk_needs: {invalid_contract_keys}"
                    )
                for key, contract in answer_boundary_contracts.items():
                    if not isinstance(contract, dict):
                        failures.append(
                            f"{RETRIEVAL_CHUNKS_PATH} {query_id} answer_boundary_contracts.{key} must be a mapping."
                        )
                        continue
                    if not isinstance(contract.get("description"), str) or not contract["description"]:
                        failures.append(
                            f"{RETRIEVAL_CHUNKS_PATH} {query_id} answer_boundary_contracts.{key}.description "
                            "must be a string."
                        )
                    if not is_non_empty_string_list(contract.get("required_terms")):
                        failures.append(
                            f"{RETRIEVAL_CHUNKS_PATH} {query_id} answer_boundary_contracts.{key}.required_terms "
                            "must be a list."
                        )
                    forbidden_terms = contract.get("forbidden_terms", [])
                    if forbidden_terms and not is_non_empty_string_list(forbidden_terms):
                        failures.append(
                            f"{RETRIEVAL_CHUNKS_PATH} {query_id} answer_boundary_contracts.{key}.forbidden_terms "
                            "must be a list when present."
                        )

        if "answer_boundary_samples" in item:
            if not answer_boundary_contracts:
                failures.append(
                    f"{RETRIEVAL_CHUNKS_PATH} {query_id} answer_boundary_samples requires "
                    "answer_boundary_contracts."
                )
            check_answer_samples(
                root,
                query_id,
                item.get("answer_boundary_samples"),
                "answer_boundary_samples",
                failures,
            )

        answer_contracts = item.get("answer_contracts", {})
        if answer_contracts:
            check_answer_contracts(query_id, answer_contracts, "answer_contracts", failures)

        if "answer_contract_samples" in item:
            if not answer_contracts:
                failures.append(
                    f"{RETRIEVAL_CHUNKS_PATH} {query_id} answer_contract_samples requires answer_contracts."
                )
            check_answer_samples(
                root,
                query_id,
                item.get("answer_contract_samples"),
                "answer_contract_samples",
                failures,
            )

        keywords = item.get("keywords")
        if not isinstance(keywords, dict):
            failures.append(f"{RETRIEVAL_CHUNKS_PATH} {query_id} keywords must be a mapping.")
        else:
            for field in ("classical", "modern"):
                if not is_non_empty_string_list(keywords.get(field)):
                    failures.append(f"{RETRIEVAL_CHUNKS_PATH} {query_id} keywords.{field} must be a list.")

        expected_sources_value = item.get("expected_sources")
        if not is_non_empty_string_list(expected_sources_value):
            failures.append(f"{RETRIEVAL_CHUNKS_PATH} {query_id} expected_sources must be a list.")
        else:
            expected_sources = cast(list[str], expected_sources_value)
            for rel_path in expected_sources:
                normalized = rel_path.rstrip("/")
                if not (root / normalized).exists():
                    failures.append(f"{RETRIEVAL_CHUNKS_PATH} {query_id} source missing: {rel_path}")

        expected_chunk_ids_value = item.get("expected_chunk_ids")
        if not is_non_empty_string_list(expected_chunk_ids_value):
            failures.append(f"{RETRIEVAL_CHUNKS_PATH} {query_id} expected_chunk_ids must be a list.")
        else:
            expected_chunk_ids = cast(list[str], expected_chunk_ids_value)
            missing = [chunk_id for chunk_id in expected_chunk_ids if chunk_id not in chunk_ids]
            if missing:
                failures.append(f"{RETRIEVAL_CHUNKS_PATH} {query_id} unknown expected chunks: {missing}")


def validate_retrieval_chunks(root: Path, failures: list[str], warnings: list[str], strict_yaml: bool) -> None:
    data = load_yaml_for_validation(root, RETRIEVAL_CHUNKS_PATH, failures, warnings, strict_yaml)
    if data is None:
        return
    if not isinstance(data, dict):
        failures.append(f"{RETRIEVAL_CHUNKS_PATH} must be a mapping.")
        return
    if data.get("version") != 1:
        failures.append(f"{RETRIEVAL_CHUNKS_PATH} version must be 1.")

    source = data.get("source")
    if not isinstance(source, str) or not (root / source).exists():
        failures.append(f"{RETRIEVAL_CHUNKS_PATH} source must reference an existing local file.")
    if not isinstance(data.get("purpose"), str) or not data["purpose"]:
        failures.append(f"{RETRIEVAL_CHUNKS_PATH} purpose must be a non-empty string.")

    chunks = data.get("chunks")
    if not isinstance(chunks, list) or not chunks:
        failures.append(f"{RETRIEVAL_CHUNKS_PATH} must contain a non-empty chunks list.")
        return

    chunk_ids: set[str] = set()
    for item in chunks:
        if not isinstance(item, dict):
            failures.append(f"{RETRIEVAL_CHUNKS_PATH} contains a non-mapping chunk.")
            continue

        chunk_id = item.get("chunk_id")
        if not isinstance(chunk_id, str) or not chunk_id:
            failures.append(f"{RETRIEVAL_CHUNKS_PATH} contains a chunk without a string id.")
            continue
        if chunk_id in chunk_ids:
            failures.append(f"{RETRIEVAL_CHUNKS_PATH} contains duplicate chunk id: {chunk_id}")
        chunk_ids.add(chunk_id)

        chunk_type = item.get("chunk_type")
        if chunk_type not in ALLOWED_RETRIEVAL_CHUNK_TYPES:
            failures.append(f"{RETRIEVAL_CHUNKS_PATH} {chunk_id} has invalid chunk_type: {chunk_type}")

        source_file = item.get("source_file")
        if not isinstance(source_file, str) or not (root / source_file).exists():
            failures.append(f"{RETRIEVAL_CHUNKS_PATH} {chunk_id} source_file must exist.")
            continue

        start_line = item.get("start_line")
        end_line = item.get("end_line")
        if not isinstance(start_line, int) or not isinstance(end_line, int) or start_line < 1 or end_line < start_line:
            failures.append(f"{RETRIEVAL_CHUNKS_PATH} {chunk_id} line range is invalid.")
            continue

        lines = (root / source_file).read_text(encoding="utf-8").splitlines()
        if end_line > len(lines):
            failures.append(f"{RETRIEVAL_CHUNKS_PATH} {chunk_id} line range exceeds source length.")
            continue

        snippet = item.get("text")
        if not isinstance(snippet, str) or not snippet:
            failures.append(f"{RETRIEVAL_CHUNKS_PATH} {chunk_id} text must be a string.")
        else:
            selected = "\n".join(lines[start_line - 1 : end_line])
            if snippet not in selected:
                failures.append(f"{RETRIEVAL_CHUNKS_PATH} {chunk_id} text is not present in source range.")

        metadata = item.get("metadata")
        section_label = metadata.get("section_label") if isinstance(metadata, dict) else None
        for field in ("citation", "passage_citation"):
            value = item.get(field)
            if not isinstance(value, str) or source_file not in value or f":{start_line}" not in value:
                failures.append(f"{RETRIEVAL_CHUNKS_PATH} {chunk_id} {field} must include the local line anchor.")
            if (
                isinstance(value, str)
                and isinstance(section_label, str)
                and section_label
                and section_label not in value
            ):
                failures.append(f"{RETRIEVAL_CHUNKS_PATH} {chunk_id} {field} must include metadata.section_label.")

        check_retrieval_chunk_metadata(
            chunk_id,
            chunk_type,
            item.get("metadata"),
            failures,
            source_file=source_file,
            start_line=start_line,
            end_line=end_line,
            source_lines=lines,
        )

    check_retrieval_queries(root, data.get("queries"), chunk_ids, failures)


_retrieval_line_text_hash = retrieval_line_text_hash
_retrieval_section_label = retrieval_section_label
_check_agama_section_metadata = check_agama_section_metadata
_check_agama_passage_provenance = check_agama_passage_provenance
_check_retrieval_chunk_metadata = check_retrieval_chunk_metadata
_check_answer_samples = check_answer_samples
_check_answer_contracts = check_answer_contracts
_check_retrieval_queries = check_retrieval_queries
_contains_membership = contains_membership
_check_retrieval_chunks_yaml = validate_retrieval_chunks
