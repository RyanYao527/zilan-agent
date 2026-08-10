from __future__ import annotations

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

ROOT = Path(__file__).resolve().parents[3]


def run_checks(
    root: Path = ROOT,
    *,
    check_generated: bool = False,
    strict_yaml: bool = False,
) -> tuple[list[str], list[str]]:
    failures: list[str] = []
    warnings: list[str] = []
    root = root.resolve()

    repository_metadata_validation.check_paths(root, failures)
    repository_metadata_validation.check_version_consistency(root, failures)
    repository_metadata_validation.check_regression_matrix(root, failures)
    regression_cases_validation.validate_regression_cases(root, failures, warnings, strict_yaml)
    reasoning_cases_validation.validate_reasoning_cases(root, failures, warnings, strict_yaml)
    retrieval_chunks_validation.validate_retrieval_chunks(root, failures, warnings, strict_yaml)
    agent_prompt_validation.validate_agent_prompts(root, failures)
    public_docs_validation.check_readme_platform_validation_links(root, failures)
    public_docs_validation.check_third_party_notices(root, failures)
    public_docs_validation.check_skill_script_inventory(root, failures)
    public_docs_validation.check_public_style_boundaries(root, failures)
    runtime_evidence_validation.validate_runtime_evidence(root, failures)
    public_docs_validation.check_portable_upgrade_doc(root, failures)
    platform_validation.validate_platform_yaml_metadata(root, failures, warnings, strict_yaml)
    agama_corpus_validation.validate_agama_search(root, failures)
    if check_generated:
        agama_corpus_validation.validate_generated_agama(root, failures)
    return failures, warnings
