from __future__ import annotations

from pathlib import Path

import validate_zilan_repo
from validate_zilan_repo import (
    _check_agent_prompts,
    _check_platform_validation_doc,
    _check_portable_upgrade_doc,
    _check_public_style_boundaries,
    _check_reasoning_cases_yaml,
    _check_retrieval_chunks_yaml,
    _check_runtime_evidence_docs,
    _check_version_consistency,
    run_checks,
)

ROOT = Path(__file__).resolve().parents[1]


def test_repository_invariants_pass_without_rebuilding_generated_files() -> None:
    failures, _warnings = run_checks(ROOT, check_generated=False, strict_yaml=False)

    assert failures == []


def test_repository_invariants_pass_with_strict_yaml() -> None:
    failures, warnings = run_checks(ROOT, check_generated=False, strict_yaml=True)

    assert failures == []
    assert warnings == []


def test_runtime_evidence_validator_module_exports_public_function() -> None:
    from zilanlib.validation.runtime_evidence import validate_runtime_evidence

    assert callable(validate_runtime_evidence)


def test_platform_validator_module_exports_public_function() -> None:
    from zilanlib.validation.platform import validate_platform_metadata

    assert callable(validate_platform_metadata)


def test_agent_prompt_validator_module_exports_public_function() -> None:
    from zilanlib.validation.agent_prompts import validate_agent_prompts

    assert callable(validate_agent_prompts)


def test_platform_validation_doc_status_mismatch_is_reported(tmp_path: Path) -> None:
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "platform-validation.md").write_text(
        """# Platform Validation Status

| Status | Meaning |
|---|---|
| `tested` | Runtime validation exists. |
| `definition-versioned` | Prompt is versioned. |
| `harness-ready` | Harness exists but live runtime is not tested. |
| `metadata-only` | Metadata exists. |
| `config-only` | Configuration exists. |
| `blocked` | Validation is blocked. |

| Platform route | Status | Last validated | Evidence | Boundary |
|---|---|---|---|---|
| Codex | `config-only` | 2026-06-10 | evidence | boundary |
""",
        encoding="utf-8",
    )
    validation = {
        "codex": {
            "status": "tested",
            "date": "2026-06-10",
            "scope": "ZC-01 through ZC-06 passed.",
        }
    }
    failures: list[str] = []

    _check_platform_validation_doc(tmp_path, validation, failures)

    assert any("status mismatch for Codex" in failure for failure in failures)


def test_agent_prompt_missing_citation_contract_is_reported(tmp_path: Path) -> None:
    agents = tmp_path / "agents"
    agents.mkdir()
    (agents / "zilan-codex.md").write_text(
        """---
runtime: codex-sub-agent
---

### Codex 阿含检索规范
### 引用规范
引用阿含经时必须注明：经名 + CBETA 编号 + 卷数/经号或品名 + 本地文件行号
### 边界与限制
""",
        encoding="utf-8",
    )
    (agents / "zilan-claude-code.md").write_text(
        """### 引用规范
引用阿含经时必须注明：经名 + CBETA 编号 + 卷数
""",
        encoding="utf-8",
    )
    failures: list[str] = []

    _check_agent_prompts(tmp_path, failures)

    assert any("激活与任务合并规则" in failure for failure in failures)
    assert any("search_agama.py --json" in failure for failure in failures)
    assert any("passage_citation" in failure for failure in failures)
    assert any("心类学与观禅实修边界输出契约" in failure for failure in failures)


def test_reasoning_cases_schema_errors_are_reported(tmp_path: Path) -> None:
    docs = tmp_path / "docs" / "architecture"
    docs.mkdir(parents=True)
    (docs / "reasoning-contract.md").write_text("# Reasoning Contract\n", encoding="utf-8")
    context = tmp_path / "context"
    context.mkdir()
    (context / "因明推理引擎.md").write_text("# 因明推理引擎\n", encoding="utf-8")
    tests = tmp_path / "tests"
    tests.mkdir()
    (tests / "reasoning_cases.yaml").write_text(
        """version: 1
source: docs/architecture/reasoning-contract.md
purpose: Test reasoning fixtures.
cases:
  - id: ZR-01
    title: Broken hetuvidya case
    source_regression_cases:
      - ZC-02
    contracts:
      - hetuvidya
    prompt: "检验论式。"
    reference_files:
      - context/因明推理引擎.md
    expected:
      boundary_statement: true
      structure:
        - 有法
      hetuvidya:
        subject: 声
        predicate: 无常
        result: impossible_result
        checks:
          paksa_dharmata: pass
          sapaksa_sattva: pass
""",
        encoding="utf-8",
    )
    failures: list[str] = []
    warnings: list[str] = []

    _check_reasoning_cases_yaml(tmp_path, failures, warnings, strict_yaml=True)

    assert warnings == []
    assert any("expected.hetuvidya.reason" in failure for failure in failures)
    assert any("expected.hetuvidya.result" in failure for failure in failures)
    assert any("checks.vipaksa_asattva" in failure for failure in failures)


def test_retrieval_chunk_schema_errors_are_reported(tmp_path: Path) -> None:
    docs = tmp_path / "docs" / "architecture"
    docs.mkdir(parents=True)
    (docs / "semantic-retrieval-interface.md").write_text("# Semantic Retrieval\n", encoding="utf-8")
    context = tmp_path / "context"
    context.mkdir()
    (context / "sample.md").write_text("line one\nline two\n", encoding="utf-8")
    fixtures = tmp_path / "tests" / "fixtures" / "retrieval_chunks"
    fixtures.mkdir(parents=True)
    (fixtures / "semantic_chunks.yaml").write_text(
        """version: 1
source: docs/architecture/semantic-retrieval-interface.md
purpose: Test retrieval chunks.
chunks:
  - chunk_id: chunk-1
    chunk_type: context_topic
    source_file: context/sample.md
    start_line: 1
    end_line: 1
    citation: "context/sample.md:1"
    passage_citation: "context/sample.md:1"
    text: "missing text"
    metadata:
      topics:
        - sample
      reasoning_roles:
        - invalid_role
queries:
  - id: SRQ-01
    query: "sample query"
    needs:
      - invalid_need
    answer_contracts:
      Bad-Key:
        description: Broken key
        required_terms:
          - sample
      empty_contract:
        description: ""
        required_terms: []
        forbidden_terms: invalid
        required_slots:
          - label: Bad Label
            terms: []
    answer_contract_samples:
      - id: Bad ID
        file: missing-answer.md
        expected_status: maybe
    keywords:
      classical:
        - sample
      modern:
        - sample
    expected_sources:
      - context/sample.md
    expected_chunk_ids:
      - missing-chunk
""",
        encoding="utf-8",
    )
    failures: list[str] = []
    warnings: list[str] = []

    _check_retrieval_chunks_yaml(tmp_path, failures, warnings, strict_yaml=True)

    assert warnings == []
    assert any("text is not present" in failure for failure in failures)
    assert any("invalid reasoning roles" in failure for failure in failures)
    assert any("invalid needs" in failure for failure in failures)
    assert any("answer_contracts key must be snake_case" in failure for failure in failures)
    assert any("answer_contracts.empty_contract.description" in failure for failure in failures)
    assert any("answer_contracts.empty_contract.required_terms" in failure for failure in failures)
    assert any("answer_contracts.empty_contract.forbidden_terms" in failure for failure in failures)
    assert any("answer_contracts.empty_contract.required_slots[0].label" in failure for failure in failures)
    assert any("answer_contracts.empty_contract.required_slots[0].terms" in failure for failure in failures)
    assert any("answer_contract_samples id must be kebab-case" in failure for failure in failures)
    assert any("answer_contract_samples Bad ID file missing" in failure for failure in failures)
    assert any("answer_contract_samples Bad ID expected_status" in failure for failure in failures)
    assert any("unknown expected chunks" in failure for failure in failures)


def test_retrieval_agama_provenance_errors_are_reported(tmp_path: Path) -> None:
    docs = tmp_path / "docs" / "architecture"
    docs.mkdir(parents=True)
    (docs / "semantic-retrieval-interface.md").write_text("# Semantic Retrieval\n", encoding="utf-8")
    context = tmp_path / "context"
    context.mkdir()
    (context / "sample.md").write_text("line one\nline two\n", encoding="utf-8")
    fixtures = tmp_path / "tests" / "fixtures" / "retrieval_chunks"
    fixtures.mkdir(parents=True)
    (fixtures / "semantic_chunks.yaml").write_text(
        """version: 1
source: docs/architecture/semantic-retrieval-interface.md
purpose: Test retrieval chunks.
chunks:
  - chunk_id: agama-bad-provenance
    chunk_type: agama_passage
    source_file: context/sample.md
    start_line: 1
    end_line: 2
    citation: "context/sample.md:1"
    passage_citation: "context/sample.md:1-2"
    text: "line one"
    metadata:
      collection: Sample Agama
      cbeta_id: T02n0099
      juan: 卷 1
      topics:
        - sample
      reasoning_roles:
        - agama_evidence
      matched_lines:
        - 3
      source_hash: "sha256:bad"
      line_text_hash: "sha256:bad"
      provenance:
        source_script: wrong.py
        source_file: context/other.md
        line_range:
          start: 1
          end: 1
        matched_lines:
          - 1
        hash_algorithm: md5
        line_text_hash: "sha256:bad"
        source_hash_scope: wrong_scope
        line_text_hash_scope: wrong_scope
queries:
  - id: SRQ-01
    query: "sample query"
    needs:
      - agama_evidence
    keywords:
      classical:
        - sample
      modern:
        - sample
    expected_sources:
      - context/sample.md
    expected_chunk_ids:
      - agama-bad-provenance
""",
        encoding="utf-8",
    )
    failures: list[str] = []
    warnings: list[str] = []

    _check_retrieval_chunks_yaml(tmp_path, failures, warnings, strict_yaml=True)

    assert warnings == []
    assert any("metadata.source_hash must match source range hash" in failure for failure in failures)
    assert any("metadata.line_text_hash must match source range hash" in failure for failure in failures)
    assert any("metadata.matched_lines must fall within the line range" in failure for failure in failures)
    assert any("metadata.provenance.source_script" in failure for failure in failures)
    assert any("metadata.provenance.source_file" in failure for failure in failures)
    assert any("metadata.provenance.line_range" in failure for failure in failures)
    assert any("metadata.provenance.matched_lines" in failure for failure in failures)
    assert any("metadata.provenance.hash_algorithm" in failure for failure in failures)
    assert any("metadata.provenance.line_text_hash" in failure for failure in failures)
    assert any("metadata.provenance.source_hash_scope" in failure for failure in failures)
    assert any("metadata.provenance.line_text_hash_scope" in failure for failure in failures)


def test_portable_upgrade_doc_missing_current_fragments_is_reported(tmp_path: Path) -> None:
    (tmp_path / "AGENT_UPGRADE_PORTABLE.md").write_text(
        "# Old migration note\n\nThis file still describes only v2.3 setup.",
        encoding="utf-8",
    )
    failures: list[str] = []

    _check_portable_upgrade_doc(tmp_path, failures)

    assert any("Current Architecture" in failure for failure in failures)
    assert any("docs/provider-routes.md" in failure for failure in failures)


def test_runtime_evidence_docs_missing_required_fragments_are_reported(tmp_path: Path) -> None:
    evidence_dir = tmp_path / "docs" / "runtime-evidence"
    evidence_dir.mkdir(parents=True)
    (evidence_dir / "README.md").write_text("# Evidence\n", encoding="utf-8")
    (evidence_dir / "evidence-template.md").write_text("# Template\n", encoding="utf-8")
    (evidence_dir / "2026-06-15-clean-install-smoke.md").write_text(
        "# Clean install\n",
        encoding="utf-8",
    )
    (evidence_dir / "2026-06-15-mock-claude-install-smoke.md").write_text(
        "# Mock install\n",
        encoding="utf-8",
    )
    failures: list[str] = []

    _check_runtime_evidence_docs(tmp_path, failures)

    assert any("Runtime Evidence Excerpts" in failure for failure in failures)
    assert any("mode: dry-run" in failure for failure in failures)
    assert any("Redaction note" in failure for failure in failures)
    assert any("standalone answer excerpt" in failure for failure in failures)
    assert any("summary-only evidence must not be used as answer_file input" in failure for failure in failures)


def test_runtime_evidence_index_missing_referenced_files_are_reported(tmp_path: Path) -> None:
    evidence_dir = tmp_path / "docs" / "runtime-evidence"
    evidence_dir.mkdir(parents=True)
    (evidence_dir / "README.md").write_text(
        """# Runtime Evidence Excerpts

Do not use this directory for:

- standalone answer excerpt
- summary-only evidence must not be used as answer_file input
- docs/validation-evidence.md
""",
        encoding="utf-8",
    )
    (evidence_dir / "index.md").write_text(
        """# Runtime Evidence Index

| Answer excerpt | Runtime source | Reviewed as | Batch/report | Status |
|---|---|---|---|---|
| `missing-answer.md` | test source | `SRQ-04` | test batch | pass |
""",
        encoding="utf-8",
    )
    (evidence_dir / "evidence-template.md").write_text(
        "Redaction note\nOutput Excerpts\nStandalone Answer Excerpts\nLimitations\n",
        encoding="utf-8",
    )
    (evidence_dir / "2026-06-15-clean-install-smoke.md").write_text(
        (
            "2026-06-15 Clean Install Smoke Evidence\n"
            "zilan-agent validation passed.\n"
            "mode: dry-run\n"
            "Found 5 matches\n"
            "No secrets\n"
        ),
        encoding="utf-8",
    )
    (evidence_dir / "2026-06-15-mock-claude-install-smoke.md").write_text(
        (
            "2026-06-15 Mock Claude Install Smoke Evidence\n"
            "mode: mock-claude-install\n"
            "skill:scripts/search_agama.py: pass\n"
            "agent:matches-source: pass\n"
            "Found 1 matches\n"
        ),
        encoding="utf-8",
    )
    failures: list[str] = []

    _check_runtime_evidence_docs(tmp_path, failures)

    assert any(
        "docs/runtime-evidence/index.md references missing runtime evidence file: missing-answer.md"
        in failure
        for failure in failures
    )


def test_runtime_evidence_batch_manifest_rejects_summary_only_answer_file(tmp_path: Path) -> None:
    evidence_dir = tmp_path / "docs" / "runtime-evidence"
    evidence_dir.mkdir(parents=True)
    (evidence_dir / "README.md").write_text(
        """# Runtime Evidence Excerpts

Do not use this directory for:

- standalone answer excerpt
- summary-only evidence must not be used as answer_file input
- docs/validation-evidence.md
""",
        encoding="utf-8",
    )
    (evidence_dir / "index.md").write_text(
        """# Runtime Evidence Index

## Summary-Only Runtime Evidence

| Evidence summary | Scope | Answer excerpt status |
|---|---|---|
| `summary-only.md` | test summary | summary-only |

## Provider And Smoke Evidence

| Evidence file | Scope |
|---|---|
| `smoke.md` | smoke summary |
""",
        encoding="utf-8",
    )
    (evidence_dir / "summary-only.md").write_text("# Summary only\n", encoding="utf-8")
    (evidence_dir / "smoke.md").write_text("# Smoke\n", encoding="utf-8")
    (evidence_dir / "2026-07-20-bad-batch.yaml").write_text(
        """version: 1
reviews:
  - id: bad-summary-only-answer-file
    query_id: SRQ-04
    answer_file: docs/runtime-evidence/summary-only.md
""",
        encoding="utf-8",
    )
    (evidence_dir / "evidence-template.md").write_text(
        "Redaction note\nOutput Excerpts\nStandalone Answer Excerpts\nLimitations\n",
        encoding="utf-8",
    )
    (evidence_dir / "2026-06-15-clean-install-smoke.md").write_text(
        (
            "2026-06-15 Clean Install Smoke Evidence\n"
            "zilan-agent validation passed.\n"
            "mode: dry-run\n"
            "Found 5 matches\n"
            "No secrets\n"
        ),
        encoding="utf-8",
    )
    (evidence_dir / "2026-06-15-mock-claude-install-smoke.md").write_text(
        (
            "2026-06-15 Mock Claude Install Smoke Evidence\n"
            "mode: mock-claude-install\n"
            "skill:scripts/search_agama.py: pass\n"
            "agent:matches-source: pass\n"
            "Found 1 matches\n"
        ),
        encoding="utf-8",
    )
    failures: list[str] = []

    _check_runtime_evidence_docs(tmp_path, failures)

    assert any(
        (
            "docs/runtime-evidence/2026-07-20-bad-batch.yaml review "
            "bad-summary-only-answer-file uses summary-only evidence as answer_file"
        )
        in failure
        for failure in failures
    )

def test_public_style_boundary_private_fragment_is_reported(tmp_path: Path, monkeypatch) -> None:
    (tmp_path / "SKILL.md").write_text("认知带宽受限", encoding="utf-8")
    monkeypatch.setattr(validate_zilan_repo, "PUBLIC_STYLE_BOUNDARY_FILES", ("SKILL.md",))
    failures: list[str] = []

    _check_public_style_boundaries(tmp_path, failures)

    assert any("private/autobiographical public fragment" in failure for failure in failures)


def test_project_version_mismatch_is_reported(tmp_path: Path) -> None:
    (tmp_path / "pyproject.toml").write_text('version = "2.4.3"\n', encoding="utf-8")
    (tmp_path / "README.zh.md").write_text("**版本**：v2.4.3\n", encoding="utf-8")
    (tmp_path / "README.en.md").write_text("**Version**: v2.4.3\n", encoding="utf-8")
    (tmp_path / "CHANGELOG.md").write_text("## [2.4.2] - 2026-06-15\n", encoding="utf-8")
    (tmp_path / "AGENT_UPGRADE_PORTABLE.md").write_text(
        "Current project baseline: zilan-agent v2.4.3\n",
        encoding="utf-8",
    )
    failures: list[str] = []

    _check_version_consistency(tmp_path, failures)

    assert any("Project version mismatch" in failure for failure in failures)
    assert any("CHANGELOG.md=2.4.2" in failure for failure in failures)
