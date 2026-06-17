from pathlib import Path

import validate_zilan_repo
from validate_zilan_repo import (
    _check_agent_prompts,
    _check_platform_validation_doc,
    _check_portable_upgrade_doc,
    _check_public_style_boundaries,
    _check_reasoning_cases_yaml,
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
