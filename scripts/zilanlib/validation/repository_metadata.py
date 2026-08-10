from __future__ import annotations

from pathlib import Path

from zilanlib.repository import (
    check_regression_matrix as check_regression_matrix_inventory,
)
from zilanlib.repository import (
    check_required_paths,
)
from zilanlib.repository import (
    check_version_consistency as check_repository_version_consistency,
)
from zilanlib.validation import runtime_evidence as runtime_evidence_validation

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
    "scripts/zilanlib/validation/public_docs.py",
    "scripts/zilanlib/validation/regression_cases.py",
    "scripts/zilanlib/validation/reasoning_cases.py",
    "scripts/zilanlib/validation/repository_metadata.py",
    "scripts/zilanlib/validation/retrieval_chunks.py",
    "scripts/zilanlib/validation/runtime_evidence.py",
    "scripts/zilanlib/validation/suite.py",
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

VERSION_SOURCES = {
    "pyproject.toml": r'(?m)^version = "([^"]+)"$',
    "README.zh.md": r"\*\*版本\*\*：v([0-9]+\.[0-9]+\.[0-9]+)",
    "README.en.md": r"\*\*Version\*\*: v([0-9]+\.[0-9]+\.[0-9]+)",
    "CHANGELOG.md": r"(?m)^## \[([0-9]+\.[0-9]+\.[0-9]+)\] - ",
    "AGENT_UPGRADE_PORTABLE.md": r"Current project baseline: zilan-agent v([0-9]+\.[0-9]+\.[0-9]+)",
}
REGRESSION_CASES = runtime_evidence_validation.REGRESSION_CASES
REGRESSION_MATRIX_DOC = "CODEX_REGRESSION_TESTS.md"


def validate_repository_metadata(root: Path, failures: list[str]) -> None:
    check_paths(root, failures)
    check_version_consistency(root, failures)
    check_regression_matrix(root, failures)


def check_paths(root: Path, failures: list[str]) -> None:
    check_required_paths(root, REQUIRED_FILES, REQUIRED_CONTEXT_FILES, failures)


def check_version_consistency(root: Path, failures: list[str]) -> None:
    check_repository_version_consistency(root, VERSION_SOURCES, failures)


def check_regression_matrix(root: Path, failures: list[str]) -> None:
    check_regression_matrix_inventory(root, REGRESSION_MATRIX_DOC, REGRESSION_CASES, failures)
