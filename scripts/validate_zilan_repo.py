from __future__ import annotations

import argparse
from pathlib import Path

from zilanlib.repository import (
    check_regression_matrix,
    check_required_paths,
    check_version_consistency,
)
from zilanlib.text_checks import check_required_fragments
from zilanlib.validation import agama_corpus as agama_corpus_validation
from zilanlib.validation import agent_prompts as agent_prompt_validation
from zilanlib.validation import platform as platform_validation
from zilanlib.validation import reasoning_cases as reasoning_cases_validation
from zilanlib.validation import regression_cases as regression_cases_validation
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
REQUIRED_FILES = (
    "README.md",
    "README.zh.md",
    "README.en.md",
    "SKILL.md",
    "SKILL-en.md",
    "CHANGELOG.md",
    "CODEX_REGRESSION_TESTS.md",
    "AGENT_UPGRADE_PORTABLE.md",
    "docs/platform-validation.md",
    "docs/runtime-validation-log.md",
    "docs/runtime-evidence/README.md",
    "docs/runtime-evidence/index.md",
    "docs/runtime-evidence/evidence-template.md",
    "docs/runtime-evidence/2026-06-15-clean-install-smoke.md",
    "docs/runtime-evidence/2026-06-15-mock-claude-install-smoke.md",
    "docs/runtime-evidence/2026-06-15-codex-v245-runtime-rerun.md",
    "docs/runtime-evidence/2026-06-16-claude-code-utf8-rerun.md",
    "docs/runtime-evidence/2026-06-16-volcengine-openai-compatible-zc-01-zc-03-live.md",
    "docs/runtime-evidence/2026-06-16-volcengine-openai-compatible-zc-02-live.md",
    "docs/maintenance-roadmap.md",
    "docs/installation.md",
    "docs/validation-evidence.md",
    "docs/provider-routes.md",
    "docs/openai-api-harness.md",
    "docs/architecture/reasoning-contract.md",
    "docs/architecture/reasoning-contract-review.md",
    "docs/architecture/semantic-retrieval-interface.md",
    "docs/architecture/zilanlib-extraction-cleanup-review.md",
    "LICENSE",
    "THIRD_PARTY_NOTICES.md",
    "CONTRIBUTING.md",
    "CONTRIBUTING-en.md",
    "agents/openai.yaml",
    "agents/zilan-claude-code.md",
    "agents/zilan-codex.md",
    "scripts/agama_evidence_checker.py",
    "scripts/build_agama_context.py",
    "scripts/cognitive_analysis_mapper.py",
    "scripts/collected_topics_analyzer.py",
    "scripts/hetuvidya_validator.py",
    "scripts/madhyamaka_critique_engine.py",
    "scripts/mock_install_smoke.py",
    "scripts/openai_api_harness.py",
    "scripts/reasoning_contract_runner.py",
    "scripts/reasoning_answer_review.py",
    "scripts/reasoning_answer_review_batch.py",
    "scripts/reasoning_validator_output.py",
    "scripts/search_agama.py",
    "scripts/semantic_answer_boundary_review.py",
    "scripts/semantic_answer_contract_review.py",
    "scripts/semantic_context_bundle.py",
    "scripts/semantic_fixture_candidates.py",
    "scripts/semantic_fixture_review.py",
    "scripts/semantic_retrieval_dry_run.py",
    "scripts/semantic_role_coverage.py",
    "scripts/validate_zilan_repo.py",
    "scripts/zilanlib/__init__.py",
    "scripts/zilanlib/repository.py",
    "scripts/zilanlib/text_checks.py",
    "scripts/zilanlib/validation/__init__.py",
    "scripts/zilanlib/validation/agent_prompts.py",
    "scripts/zilanlib/validation/agama_corpus.py",
    "scripts/zilanlib/validation/platform.py",
    "scripts/zilanlib/validation/regression_cases.py",
    "scripts/zilanlib/validation/reasoning_cases.py",
    "scripts/zilanlib/validation/retrieval_chunks.py",
    "scripts/zilanlib/validation/runtime_evidence.py",
    "scripts/zilanlib/agama/__init__.py",
    "scripts/zilanlib/reasoning/__init__.py",
    "scripts/zilanlib/reasoning/agama_evidence_checker.py",
    "scripts/zilanlib/reasoning/cognitive_analysis_mapper.py",
    "scripts/zilanlib/reasoning/collected_topics_analyzer.py",
    "scripts/zilanlib/reasoning/answer_review.py",
    "scripts/zilanlib/reasoning/answer_review_batch.py",
    "scripts/zilanlib/reasoning/contract_runner.py",
    "scripts/zilanlib/reasoning/hetuvidya_validator.py",
    "scripts/zilanlib/reasoning/madhyamaka_critique_engine.py",
    "scripts/zilanlib/reasoning/validator_output.py",
    "scripts/zilanlib/agama/candidates.py",
    "scripts/zilanlib/agama/fixture_review.py",
    "scripts/zilanlib/agama/search.py",
    "scripts/zilanlib/semantic/__init__.py",
    "scripts/zilanlib/semantic/answer_boundary_review.py",
    "scripts/zilanlib/semantic/answer_contract_review.py",
    "scripts/zilanlib/semantic/context_bundle.py",
    "scripts/zilanlib/semantic/retrieval_dry_run.py",
    "scripts/zilanlib/semantic/role_coverage.py",
    "scripts/zilanlib/yaml_io.py",
    "tests/regression_cases.yaml",
    "tests/reasoning_cases.yaml",
    "tests/fixtures/retrieval_chunks/semantic_chunks.yaml",
)

REQUIRED_CONTEXT_FILES = (
    "context/摄类学工具箱.md",
    "context/因明推理引擎.md",
    "context/心类学认知分析.md",
    "context/中观应成精要.md",
    "context/南传观禅指南.md",
    "context/模因机器视角下的佛教结集与传播.md",
    "context/agama/agama-index.md",
    "context/agama/T0001-chang-agama.md",
    "context/agama/T0026-zhong-agama.md",
    "context/agama/T0099-za-agama.md",
    "context/agama/T0125-ekottarika-agama.md",
    "context/agama/_source/T01n0001.xml",
    "context/agama/_source/T01n0026.xml",
    "context/agama/_source/T02n0099.xml",
    "context/agama/_source/T02n0125.xml",
)

GENERATED_AGAMA_FILES = agama_corpus_validation.GENERATED_AGAMA_FILES


REGRESSION_CASES = runtime_evidence_validation.REGRESSION_CASES
REGRESSION_CASES_PATH = regression_cases_validation.REGRESSION_CASES_PATH
REASONING_CASES_PATH = reasoning_cases_validation.REASONING_CASES_PATH
RETRIEVAL_CHUNKS_PATH = retrieval_chunks_validation.RETRIEVAL_CHUNKS_PATH
README_FILES = ("README.md", "README.zh.md", "README.en.md")
PUBLIC_STYLE_BOUNDARY_FILES = (
    "SKILL.md",
    "SKILL-en.md",
    "README.zh.md",
    "README.en.md",
    "agents/zilan-codex.md",
    "agents/zilan-claude-code.md",
    "CODEX_REGRESSION_TESTS.md",
    "tests/regression_cases.yaml",
    "context/摄类学工具箱.md",
    "context/心类学认知分析.md",
    "context/中观应成精要.md",
    "context/南传观禅指南.md",
)
HIGH_RISK_PUBLIC_FRAGMENTS = (
    "认知带宽受限",
    "育儿耐心溃败",
    "育儿溃败",
    "两性得失计较",
    "两性计较",
    "三大长间隙",
    "职场否定",
    "灵性经验切片",
    "深度沉迷",
    "AI佛乐",
    "AI 佛乐",
    "感觉老婆",
    "11月孩子",
    "11 个月孩子",
    "被领导质疑",
    "带娃",
)
PLATFORM_VALIDATION_DOC = platform_validation.PLATFORM_VALIDATION_DOC
RUNTIME_VALIDATION_LOG_DOC = runtime_evidence_validation.RUNTIME_VALIDATION_LOG_DOC
RUNTIME_EVIDENCE_INDEX_DOC = runtime_evidence_validation.RUNTIME_EVIDENCE_INDEX_DOC
RUNTIME_EVIDENCE_NAV_INDEX_DOC = runtime_evidence_validation.RUNTIME_EVIDENCE_NAV_INDEX_DOC
RUNTIME_EVIDENCE_TEMPLATE_DOC = runtime_evidence_validation.RUNTIME_EVIDENCE_TEMPLATE_DOC
RUNTIME_EVIDENCE_CLEAN_INSTALL_DOC = runtime_evidence_validation.RUNTIME_EVIDENCE_CLEAN_INSTALL_DOC
RUNTIME_EVIDENCE_MOCK_INSTALL_DOC = runtime_evidence_validation.RUNTIME_EVIDENCE_MOCK_INSTALL_DOC
MAINTENANCE_ROADMAP_DOC = "docs/maintenance-roadmap.md"
INSTALLATION_DOC = "docs/installation.md"
VALIDATION_EVIDENCE_DOC = "docs/validation-evidence.md"
PROVIDER_ROUTES_DOC = "docs/provider-routes.md"
CHANGELOG_DOC = "CHANGELOG.md"
THIRD_PARTY_NOTICES_DOC = "THIRD_PARTY_NOTICES.md"
PORTABLE_UPGRADE_DOC = "AGENT_UPGRADE_PORTABLE.md"
VERSION_SOURCES = {
    "pyproject.toml": r'(?m)^version = "([^"]+)"$',
    "README.zh.md": r"\*\*版本\*\*：v([0-9]+\.[0-9]+\.[0-9]+)",
    "README.en.md": r"\*\*Version\*\*: v([0-9]+\.[0-9]+\.[0-9]+)",
    "CHANGELOG.md": r"(?m)^## \[([0-9]+\.[0-9]+\.[0-9]+)\] - ",
    "AGENT_UPGRADE_PORTABLE.md": r"Current project baseline: zilan-agent v([0-9]+\.[0-9]+\.[0-9]+)",
}
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



def _check_paths(root: Path, failures: list[str]) -> None:
    check_required_paths(root, REQUIRED_FILES, REQUIRED_CONTEXT_FILES, failures)


def _check_version_consistency(root: Path, failures: list[str]) -> None:
    check_version_consistency(root, VERSION_SOURCES, failures)


def _check_regression_matrix(root: Path, failures: list[str]) -> None:
    check_regression_matrix(root, "CODEX_REGRESSION_TESTS.md", REGRESSION_CASES, failures)


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
_check_readme_platform_validation_links = platform_validation.check_readme_platform_validation_links
validate_platform_metadata = platform_validation.validate_platform_metadata


def _check_third_party_notices(root: Path, failures: list[str]) -> None:
    notice_text = (root / THIRD_PARTY_NOTICES_DOC).read_text(encoding="utf-8")
    required_notice_fragments = (
        "CBETA XML-P5",
        "https://github.com/cbeta-org/xml-p5",
        "https://www.cbeta.org/copyright.php",
        "context/agama/_source/",
        "context/agama/T0099-za-agama.md",
        "not relicensed under the MIT License",
    )
    check_required_fragments(notice_text, required_notice_fragments, failures, rel_path=THIRD_PARTY_NOTICES_DOC)

    license_text = (root / "LICENSE").read_text(encoding="utf-8")
    check_required_fragments(
        license_text,
        ("Repository License Scope", "CBETA-derived", THIRD_PARTY_NOTICES_DOC),
        failures,
        rel_path="LICENSE",
        message="missing third-party scope fragment",
    )

    for rel_path in README_FILES:
        text = (root / rel_path).read_text(encoding="utf-8")
        if THIRD_PARTY_NOTICES_DOC not in text:
            failures.append(f"{rel_path} should link to {THIRD_PARTY_NOTICES_DOC}.")
        if "CBETA" not in text:
            failures.append(f"{rel_path} should mention CBETA for Agama third-party material.")

def _check_skill_script_inventory(root: Path, failures: list[str]) -> None:
    script_paths = sorted(path.relative_to(root).as_posix() for path in (root / "scripts").rglob("*.py"))
    for rel_path in ("SKILL.md", "SKILL-en.md"):
        text = (root / rel_path).read_text(encoding="utf-8")
        for script_path in script_paths:
            script_name = Path(script_path).name
            if script_path not in text and script_name not in text:
                failures.append(f"{rel_path} missing script inventory entry: {script_path}")

def _check_public_style_boundaries(root: Path, failures: list[str]) -> None:
    for rel_path in PUBLIC_STYLE_BOUNDARY_FILES:
        text = (root / rel_path).read_text(encoding="utf-8")
        for fragment in HIGH_RISK_PUBLIC_FRAGMENTS:
            if fragment in text:
                failures.append(
                    f"{rel_path} contains private/autobiographical public fragment: {fragment}"
                )


_check_runtime_validation_log = runtime_evidence_validation.check_runtime_validation_log
_runtime_evidence_rel_path_from_ref = runtime_evidence_validation.runtime_evidence_rel_path_from_ref
_runtime_evidence_refs_from_text = runtime_evidence_validation.runtime_evidence_refs_from_text
_markdown_section = runtime_evidence_validation.markdown_section
_runtime_evidence_summary_only_refs = runtime_evidence_validation.runtime_evidence_summary_only_refs
_check_runtime_evidence_index_references = runtime_evidence_validation.check_runtime_evidence_index_references
_check_runtime_evidence_batch_manifests = runtime_evidence_validation.check_runtime_evidence_batch_manifests
_check_runtime_evidence_docs = runtime_evidence_validation.check_runtime_evidence_docs
validate_runtime_evidence = runtime_evidence_validation.validate_runtime_evidence
def _check_portable_upgrade_doc(root: Path, failures: list[str]) -> None:
    text = (root / PORTABLE_UPGRADE_DOC).read_text(encoding="utf-8")
    required_fragments = (
        "Skill To Agent Migration Record",
        "Current Architecture",
        "docs/installation.md",
        "docs/platform-validation.md",
        "docs/provider-routes.md",
        "DeepSeek Compatibility Caveat",
        "Do not infer platform support from this file alone",
    )
    check_required_fragments(text, required_fragments, failures, rel_path=PORTABLE_UPGRADE_DOC)


def _check_yaml(root: Path, failures: list[str], warnings: list[str], strict_yaml: bool) -> None:
    validation = validate_platform_metadata(root, failures, warnings, strict_yaml)
    if not validation:
        return

    codex_validation = validation.get("codex")
    if not isinstance(codex_validation, dict) or codex_validation.get("status") != "tested":
        failures.append("agents/openai.yaml should mark validation.codex.status as tested.")


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
