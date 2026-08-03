from __future__ import annotations

import argparse
from pathlib import Path

from zilanlib.validation import agama_corpus as agama_corpus_validation
from zilanlib.validation import agent_prompts as agent_prompt_validation
from zilanlib.validation import platform as platform_validation
from zilanlib.validation import public_docs as public_docs_validation
from zilanlib.validation import reasoning_cases as reasoning_cases_validation
from zilanlib.validation import regression_cases as regression_cases_validation
from zilanlib.validation import repository_metadata as repository_metadata_validation
from zilanlib.validation import retrieval_chunks as retrieval_chunks_validation
from zilanlib.validation import runtime_evidence as runtime_evidence_validation
from zilanlib.yaml_io import (
    is_non_empty_int_list,
    is_non_empty_string_list,
    load_yaml_for_validation,
)

ROOT = Path(__file__).resolve().parents[1]

_load_yaml = load_yaml_for_validation
_is_non_empty_string_list = is_non_empty_string_list
_is_non_empty_int_list = is_non_empty_int_list
REQUIRED_FILES = repository_metadata_validation.REQUIRED_FILES
REQUIRED_CONTEXT_FILES = repository_metadata_validation.REQUIRED_CONTEXT_FILES

GENERATED_AGAMA_FILES = agama_corpus_validation.GENERATED_AGAMA_FILES


REGRESSION_CASES = repository_metadata_validation.REGRESSION_CASES
REGRESSION_CASES_PATH = regression_cases_validation.REGRESSION_CASES_PATH
REASONING_CASES_PATH = reasoning_cases_validation.REASONING_CASES_PATH
RETRIEVAL_CHUNKS_PATH = retrieval_chunks_validation.RETRIEVAL_CHUNKS_PATH
README_FILES = public_docs_validation.README_FILES
PUBLIC_STYLE_BOUNDARY_FILES = public_docs_validation.PUBLIC_STYLE_BOUNDARY_FILES
HIGH_RISK_PUBLIC_FRAGMENTS = public_docs_validation.HIGH_RISK_PUBLIC_FRAGMENTS
PLATFORM_VALIDATION_DOC = platform_validation.PLATFORM_VALIDATION_DOC
RUNTIME_VALIDATION_LOG_DOC = runtime_evidence_validation.RUNTIME_VALIDATION_LOG_DOC
RUNTIME_EVIDENCE_INDEX_DOC = runtime_evidence_validation.RUNTIME_EVIDENCE_INDEX_DOC
RUNTIME_EVIDENCE_NAV_INDEX_DOC = runtime_evidence_validation.RUNTIME_EVIDENCE_NAV_INDEX_DOC
RUNTIME_EVIDENCE_TEMPLATE_DOC = runtime_evidence_validation.RUNTIME_EVIDENCE_TEMPLATE_DOC
RUNTIME_EVIDENCE_CLEAN_INSTALL_DOC = runtime_evidence_validation.RUNTIME_EVIDENCE_CLEAN_INSTALL_DOC
RUNTIME_EVIDENCE_MOCK_INSTALL_DOC = runtime_evidence_validation.RUNTIME_EVIDENCE_MOCK_INSTALL_DOC
MAINTENANCE_ROADMAP_DOC = public_docs_validation.MAINTENANCE_ROADMAP_DOC
INSTALLATION_DOC = public_docs_validation.INSTALLATION_DOC
VALIDATION_EVIDENCE_DOC = public_docs_validation.VALIDATION_EVIDENCE_DOC
PROVIDER_ROUTES_DOC = public_docs_validation.PROVIDER_ROUTES_DOC
CHANGELOG_DOC = public_docs_validation.CHANGELOG_DOC
THIRD_PARTY_NOTICES_DOC = public_docs_validation.THIRD_PARTY_NOTICES_DOC
PORTABLE_UPGRADE_DOC = public_docs_validation.PORTABLE_UPGRADE_DOC
VERSION_SOURCES = repository_metadata_validation.VERSION_SOURCES
ALLOWED_VALIDATION_STATUSES = platform_validation.ALLOWED_VALIDATION_STATUSES
ALLOWED_REASONING_CONTRACTS = reasoning_cases_validation.ALLOWED_REASONING_CONTRACTS
ALLOWED_HETUVIDYA_RESULTS = reasoning_cases_validation.ALLOWED_HETUVIDYA_RESULTS
ALLOWED_REASONING_CHECK_STATUSES = reasoning_cases_validation.ALLOWED_REASONING_CHECK_STATUSES
ALLOWED_RETRIEVAL_CHUNK_TYPES = retrieval_chunks_validation.ALLOWED_RETRIEVAL_CHUNK_TYPES
ALLOWED_RETRIEVAL_NEEDS = retrieval_chunks_validation.ALLOWED_RETRIEVAL_NEEDS
ALLOWED_RETRIEVAL_NON_CHUNK_NEEDS = retrieval_chunks_validation.ALLOWED_RETRIEVAL_NON_CHUNK_NEEDS
ALLOWED_ANSWER_SAMPLE_STATUSES = retrieval_chunks_validation.ALLOWED_ANSWER_SAMPLE_STATUSES
RETRIEVAL_HASH_ALGORITHM = retrieval_chunks_validation.RETRIEVAL_HASH_ALGORITHM
RETRIEVAL_SOURCE_SCRIPT = retrieval_chunks_validation.RETRIEVAL_SOURCE_SCRIPT
RETRIEVAL_SOURCE_HASH_SCOPE = retrieval_chunks_validation.RETRIEVAL_SOURCE_HASH_SCOPE
RETRIEVAL_LINE_TEXT_HASH_SCOPE = retrieval_chunks_validation.RETRIEVAL_LINE_TEXT_HASH_SCOPE
PLATFORM_VALIDATION_LABELS = platform_validation.PLATFORM_VALIDATION_LABELS
AGENT_PROMPT_REQUIRED_FRAGMENTS = agent_prompt_validation.AGENT_PROMPT_REQUIRED_FRAGMENTS


_hash_file = agama_corpus_validation.hash_file


_check_paths = repository_metadata_validation.check_paths
_check_version_consistency = repository_metadata_validation.check_version_consistency
_check_regression_matrix = repository_metadata_validation.check_regression_matrix
validate_repository_metadata = repository_metadata_validation.validate_repository_metadata

_check_regression_cases_yaml = regression_cases_validation.validate_regression_cases
validate_regression_cases = regression_cases_validation.validate_regression_cases

_retrieval_line_text_hash = retrieval_chunks_validation.retrieval_line_text_hash
_check_agama_passage_provenance = retrieval_chunks_validation.check_agama_passage_provenance
_check_retrieval_chunk_metadata = retrieval_chunks_validation.check_retrieval_chunk_metadata
_check_answer_samples = retrieval_chunks_validation.check_answer_samples
_check_answer_contracts = retrieval_chunks_validation.check_answer_contracts
_check_retrieval_queries = retrieval_chunks_validation.check_retrieval_queries
_check_retrieval_chunks_yaml = retrieval_chunks_validation.validate_retrieval_chunks
validate_retrieval_chunks = retrieval_chunks_validation.validate_retrieval_chunks

_check_hetuvidya_contract = reasoning_cases_validation.check_hetuvidya_contract
_check_collected_topics_contract = reasoning_cases_validation.check_collected_topics_contract
_check_cognitive_analysis_contract = reasoning_cases_validation.check_cognitive_analysis_contract
_check_madhyamaka_prasanga_contract = reasoning_cases_validation.check_madhyamaka_prasanga_contract
_check_agama_evidence_contract = reasoning_cases_validation.check_agama_evidence_contract
_check_reasoning_cases_yaml = reasoning_cases_validation.validate_reasoning_cases
validate_reasoning_cases = reasoning_cases_validation.validate_reasoning_cases

_check_agent_prompts = agent_prompt_validation.validate_agent_prompts
validate_agent_prompts = agent_prompt_validation.validate_agent_prompts


_get_validation_mapping = platform_validation.get_validation_mapping
_check_agent_validation_entries = platform_validation.check_agent_validation_entries
_parse_markdown_table_rows = platform_validation.parse_markdown_table_rows
_check_platform_validation_doc = platform_validation.check_platform_validation_doc
_check_readme_platform_validation_links = public_docs_validation.check_readme_platform_validation_links
validate_platform_metadata = platform_validation.validate_platform_metadata
_check_yaml = platform_validation.validate_platform_yaml_metadata
validate_platform_yaml_metadata = platform_validation.validate_platform_yaml_metadata


_check_third_party_notices = public_docs_validation.check_third_party_notices
_check_skill_script_inventory = public_docs_validation.check_skill_script_inventory
_check_public_style_boundaries = public_docs_validation.check_public_style_boundaries
_check_public_docs = public_docs_validation.validate_public_docs
validate_public_docs = public_docs_validation.validate_public_docs


_check_runtime_validation_log = runtime_evidence_validation.check_runtime_validation_log
_runtime_evidence_rel_path_from_ref = runtime_evidence_validation.runtime_evidence_rel_path_from_ref
_runtime_evidence_refs_from_text = runtime_evidence_validation.runtime_evidence_refs_from_text
_markdown_section = runtime_evidence_validation.markdown_section
_runtime_evidence_summary_only_refs = runtime_evidence_validation.runtime_evidence_summary_only_refs
_check_runtime_evidence_index_references = runtime_evidence_validation.check_runtime_evidence_index_references
_check_runtime_evidence_batch_manifests = runtime_evidence_validation.check_runtime_evidence_batch_manifests
_check_runtime_evidence_docs = runtime_evidence_validation.check_runtime_evidence_docs
validate_runtime_evidence = runtime_evidence_validation.validate_runtime_evidence
_check_portable_upgrade_doc = public_docs_validation.check_portable_upgrade_doc


_check_agama_search = agama_corpus_validation.validate_agama_search
validate_agama_search = agama_corpus_validation.validate_agama_search
_run_build_agama = agama_corpus_validation.run_build_agama
_check_generated_agama = agama_corpus_validation.validate_generated_agama
validate_generated_agama = agama_corpus_validation.validate_generated_agama


def run_checks(
    root: Path = ROOT,
    *,
    check_generated: bool = False,
    strict_yaml: bool = False,
) -> tuple[list[str], list[str]]:
    failures: list[str] = []
    warnings: list[str] = []
    root = root.resolve()

    _check_paths(root, failures)
    _check_version_consistency(root, failures)
    _check_regression_matrix(root, failures)
    _check_regression_cases_yaml(root, failures, warnings, strict_yaml)
    _check_reasoning_cases_yaml(root, failures, warnings, strict_yaml)
    _check_retrieval_chunks_yaml(root, failures, warnings, strict_yaml)
    _check_agent_prompts(root, failures)
    _check_readme_platform_validation_links(root, failures)
    _check_third_party_notices(root, failures)
    _check_skill_script_inventory(root, failures)
    _check_public_style_boundaries(root, failures)
    validate_runtime_evidence(root, failures)
    _check_portable_upgrade_doc(root, failures)
    _check_yaml(root, failures, warnings, strict_yaml)
    _check_agama_search(root, failures)
    if check_generated:
        _check_generated_agama(root, failures)
    return failures, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate zilan-agent repository invariants.")
    parser.add_argument("--root", type=Path, default=ROOT, help="Repository root.")
    parser.add_argument(
        "--check-generated",
        action="store_true",
        help="Rebuild Agama Markdown and fail if generated files change.",
    )
    parser.add_argument(
        "--strict-yaml",
        action="store_true",
        help="Fail when PyYAML is unavailable instead of warning.",
    )
    args = parser.parse_args()

    failures, warnings = run_checks(
        args.root,
        check_generated=args.check_generated,
        strict_yaml=args.strict_yaml,
    )
    for warning in warnings:
        print(f"WARN: {warning}")
    if failures:
        print("zilan-agent validation failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("zilan-agent validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
