# Zilan Maintenance Deepening Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Improve zilan-agent maintainability without changing runtime behavior, platform validation status, or Buddhist reasoning contracts.

**Architecture:** Keep root scripts as stable CLI entrypoints. Move reusable validation logic into `scripts/zilanlib/validation/` through small reversible extractions, reuse existing YAML helpers, and tighten packaging/test metadata only after behavior-preserving tests pass.

**Tech Stack:** Python 3.10+, PyYAML, pytest, pytest-cov, ruff, mypy, setuptools.

## Global Constraints

- Preserve CLI compatibility for all existing `scripts/*.py` commands.
- Do not change `docs/platform-validation.md` status values in these PRs.
- Do not call providers or add live runtime evidence in maintenance PRs.
- Do not add LangChain, LlamaIndex, vector databases, FastAPI, Docker, or LLM judges.
- Keep each PR behavior-preserving unless its task explicitly updates metadata.
- Run `python scripts/validate_zilan_repo.py --check-generated --strict-yaml`, `python -m pytest`, `python -m ruff check scripts tests`, and `python -m mypy` before merge.

---

## File Structure

- Create: `scripts/zilanlib/validation/__init__.py`
- Create: `scripts/zilanlib/validation/runtime_evidence.py`
- Create later: `scripts/zilanlib/validation/platform.py`
- Create later: `scripts/zilanlib/validation/semantic_fixtures.py`
- Create later: `scripts/zilanlib/validation/agent_prompts.py`
- Modify: `scripts/validate_zilan_repo.py`
- Modify: `scripts/openai_api_harness.py`
- Modify: `tests/test_reasoning_contract_runner.py`
- Modify: `pyproject.toml`
- Create: `scripts/zilanlib/py.typed`
- Optional later: `docs/architecture/terminology-glossary.md`

## Milestone Order

1. PR-A: Extract one self-contained validator family from `validate_zilan_repo.py`.
2. PR-B: Clean high-priority duplication in harness and tests.
3. PR-C: Continue validation-module extraction in two or three narrow PRs.
4. PR-D: Packaging and coverage metadata cleanup.
5. PR-E: Content/retrieval improvements only after maintenance baseline is stable.

---

### Task 1: Extract Runtime Evidence Validation

**Files:**
- Create: `scripts/zilanlib/validation/__init__.py`
- Create: `scripts/zilanlib/validation/runtime_evidence.py`
- Modify: `scripts/validate_zilan_repo.py`
- Test: existing `tests/test_validate_zilan_repo.py`

**Interfaces:**
- Consumes: `root: Path`, `failures: list[str]`, runtime-evidence constants defined in `scripts/zilanlib/validation/runtime_evidence.py`, and `zilanlib.yaml_io.load_yaml_for_validation()` for batch-manifest parsing.
- Produces: `validate_runtime_evidence(root: Path, failures: list[str]) -> None`.

- [ ] **Step 1: Identify the runtime-evidence functions**

  In `scripts/validate_zilan_repo.py`, locate functions and helpers that validate:

  ```text
  docs/runtime-evidence/index.md references
  runtime answer-review batch answer_file safety
  summary-only evidence rejection
  standalone answer excerpt references
  ```

- [ ] **Step 2: Write a focused import-preservation test**

  Add a test to `tests/test_validate_zilan_repo.py` that imports the new module and asserts the public function exists:

  ```python
  def test_runtime_evidence_validator_module_exports_public_function() -> None:
      from zilanlib.validation.runtime_evidence import validate_runtime_evidence

      assert callable(validate_runtime_evidence)
  ```

- [ ] **Step 3: Run the targeted test to verify it fails**

  Run:

  ```powershell
  python -m pytest tests\test_validate_zilan_repo.py::test_runtime_evidence_validator_module_exports_public_function -q
  ```

  Expected: FAIL because `zilanlib.validation.runtime_evidence` does not exist yet.

- [ ] **Step 4: Create the validation package scaffold**

  Create `scripts/zilanlib/validation/__init__.py`:

  ```python
  from __future__ import annotations
  ```

  Create `scripts/zilanlib/validation/runtime_evidence.py` with the public function and a temporary delegation target:

  ```python
  from __future__ import annotations

  from pathlib import Path


  def validate_runtime_evidence(root: Path, failures: list[str]) -> None:
      raise NotImplementedError("runtime evidence validation has not been extracted yet")
  ```

- [ ] **Step 5: Move the smallest complete runtime-evidence check**

  Move exactly one cohesive check from `scripts/validate_zilan_repo.py` into `runtime_evidence.py`. Prefer the newest `docs/runtime-evidence/index.md` reference validation because it is self-contained and has current tests.

  Keep error strings byte-for-byte identical. Keep `validate_zilan_repo.py` calling the moved function from its existing orchestration path.

- [ ] **Step 6: Run targeted validation tests**

  Run:

  ```powershell
  python -m pytest tests\test_validate_zilan_repo.py -q
  python scripts\validate_zilan_repo.py --strict-yaml
  ```

  Expected: PASS.

- [ ] **Step 7: Commit**

  ```powershell
  git add scripts\validate_zilan_repo.py scripts\zilanlib\validation tests\test_validate_zilan_repo.py
  git commit -m "refactor: extract runtime evidence validation"
  ```

---

### Task 2: Reuse Shared YAML Loader In OpenAI Harness

**Files:**
- Modify: `scripts/openai_api_harness.py`
- Test: `tests/test_openai_api_harness.py`

**Interfaces:**
- Consumes: `zilanlib.yaml_io.load_yaml_mapping(path: Path, *, root: Path, error_type: type[ValueError], missing_message: str, missing_file_label: str, parse_label: str, mapping_label: str) -> dict[str, Any]`.
- Produces: no public API change.

- [ ] **Step 1: Write a regression test for mapping enforcement**

  If no test currently covers non-mapping YAML, add:

  ```python
  def test_openai_harness_rejects_non_mapping_yaml(tmp_path: Path) -> None:
      path = tmp_path / "bad.yaml"
      path.write_text("- not\n- mapping\n", encoding="utf-8")

      with pytest.raises(ValueError, match="must contain a YAML mapping"):
          openai_api_harness._load_yaml(path)
  ```

- [ ] **Step 2: Replace local YAML parsing**

  Change `scripts/openai_api_harness.py` imports from:

  ```python
  import yaml
  ```

  to:

  ```python
  from zilanlib.yaml_io import load_yaml_mapping
  ```

  Replace `_load_yaml` with:

  ```python
  def _load_yaml(path: Path) -> dict[str, Any]:
      return load_yaml_mapping(
          path,
          root=ROOT,
          error_type=ValueError,
          missing_message="PyYAML is required to parse YAML files.",
          missing_file_label="Missing YAML file",
          parse_label="Failed to parse YAML file",
          mapping_label="YAML file must contain a mapping",
      )
  ```

- [ ] **Step 3: Run harness tests**

  ```powershell
  python -m pytest tests\test_openai_api_harness.py -q
  python scripts\openai_api_harness.py --case ZC-02 --json
  ```

  Expected: PASS and dry-run JSON is still produced.

- [ ] **Step 4: Commit**

  ```powershell
  git add scripts\openai_api_harness.py tests\test_openai_api_harness.py
  git commit -m "refactor: reuse shared yaml loader in harness"
  ```

---

### Task 3: Replace NOT_APPLICABLE Test Constants With Factories

**Files:**
- Modify: `tests/test_reasoning_contract_runner.py`

**Interfaces:**
- Produces: `not_applicable_validator(...) -> dict[str, object]` test helper.

- [ ] **Step 1: Add the helper**

  Replace repeated `NOT_APPLICABLE_*` dictionaries with:

  ```python
  def not_applicable_validator(
      *,
      validator: str,
      contract_family: str,
      output_schema: str,
      payload_key: str,
  ) -> dict[str, object]:
      return {
          "status": "not_applicable",
          "validator": validator,
          "contract_family": contract_family,
          "output_schema": output_schema,
          "source": "tests/reasoning_cases.yaml",
          "case_ids": [],
          payload_key: [],
          "limitations": [
              "fixture-only validator",
              "does not parse arbitrary natural-language answers",
              "does not call providers or grade doctrine",
          ],
      }
  ```

- [ ] **Step 2: Recreate named expected values through the helper**

  Keep readable names, but compute them:

  ```python
  NOT_APPLICABLE_HETUVIDYA = not_applicable_validator(
      validator="hetuvidya_validator",
      contract_family="hetuvidya",
      output_schema="hetuvidya-validator-output-v0.1",
      payload_key="validations",
  )
  ```

  Repeat for collected topics, Madhyamaka, cognitive analysis, and Agama evidence.

- [ ] **Step 3: Run contract runner tests**

  ```powershell
  python -m pytest tests\test_reasoning_contract_runner.py -q
  ```

  Expected: PASS with no production code change.

- [ ] **Step 4: Commit**

  ```powershell
  git add tests\test_reasoning_contract_runner.py
  git commit -m "test: dry reasoning runner not-applicable expectations"
  ```

---

### Task 4: Narrow Coverage Scope To zilanlib

**Files:**
- Modify: `pyproject.toml`
- Modify: `docs/maintenance-roadmap.md`

**Interfaces:**
- Changes pytest coverage reporting only; no runtime behavior change.

- [ ] **Step 1: Change pytest coverage target**

  In `pyproject.toml`, change:

  ```toml
  addopts = "--cov=scripts --cov-report=term-missing"
  ```

  to:

  ```toml
  addopts = "--cov=scripts/zilanlib --cov-report=term-missing"
  ```

- [ ] **Step 2: Update roadmap wording**

  In `docs/maintenance-roadmap.md`, change the coverage baseline sentence to state that coverage now targets `scripts/zilanlib` rather than all root CLI wrappers. Do not invent a new percentage until a local run reports it.

- [ ] **Step 3: Run pytest**

  ```powershell
  python -m pytest
  ```

  Expected: PASS and coverage report only lists `scripts/zilanlib` modules.

- [ ] **Step 4: Commit**

  ```powershell
  git add pyproject.toml docs\maintenance-roadmap.md
  git commit -m "test: scope coverage to zilanlib"
  ```

---

### Task 5: Add py.typed And Packaging Metadata

**Files:**
- Create: `scripts/zilanlib/py.typed`
- Modify: `pyproject.toml`
- Test: `python -m mypy`

**Interfaces:**
- Makes `zilanlib` package typing metadata explicit.

- [ ] **Step 1: Add marker file**

  Create empty file:

  ```text
  scripts/zilanlib/py.typed
  ```

- [ ] **Step 2: Add project URLs and classifiers**

  Add to `pyproject.toml`:

  ```toml
  classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "Intended Audience :: Religion",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Topic :: Religion",
    "Topic :: Software Development :: Testing",
    "Typing :: Typed",
  ]

  [project.urls]
  Homepage = "https://github.com/RyanYao527/zilan-agent"
  Repository = "https://github.com/RyanYao527/zilan-agent"
  Issues = "https://github.com/RyanYao527/zilan-agent/issues"
  Changelog = "https://github.com/RyanYao527/zilan-agent/blob/main/CHANGELOG.md"
  ```

- [ ] **Step 3: Add explicit package discovery**

  Add:

  ```toml
  [tool.setuptools.packages.find]
  where = ["scripts"]
  include = ["zilanlib*"]
  ```

  Keep `py-modules = []` only if setuptools accepts the combination during build metadata checks; otherwise remove it in the same PR with a note in the changelog.

- [ ] **Step 4: Run metadata and type checks**

  ```powershell
  python -m mypy
  python -m pytest tests\test_validate_zilan_repo.py -q
  ```

  Expected: PASS.

- [ ] **Step 5: Commit**

  ```powershell
  git add pyproject.toml scripts\zilanlib\py.typed
  git commit -m "build: mark zilanlib as typed"
  ```

---

### Task 6: Continue Validation Extraction In Narrow PRs

**Files:**
- Create: `scripts/zilanlib/validation/platform.py`
- Create: `scripts/zilanlib/validation/semantic_fixtures.py`
- Create: `scripts/zilanlib/validation/agent_prompts.py`
- Modify: `scripts/validate_zilan_repo.py`
- Test: `tests/test_validate_zilan_repo.py`

**Interfaces:**
- Each module exposes one public `validate_*` function taking `root`, `failures`, `warnings`, and `strict_yaml` where needed.

- [ ] **Step 1: Extract platform route validation**

  Move `agents/openai.yaml` and `docs/platform-validation.md` consistency checks into `validation/platform.py`.

- [ ] **Step 2: Extract semantic fixture validation**

  Move `tests/fixtures/retrieval_chunks/semantic_chunks.yaml` source-file, line-range, role, answer-contract, and sample-reference checks into `validation/semantic_fixtures.py`.

- [ ] **Step 3: Extract agent prompt validation**

  Move Codex/Claude agent prompt contract checks into `validation/agent_prompts.py`.

- [ ] **Step 4: Run the full local validation set after each extraction**

  ```powershell
  python scripts\validate_zilan_repo.py --check-generated --strict-yaml
  python -m pytest tests\test_validate_zilan_repo.py -q
  python -m ruff check scripts tests
  python -m mypy
  ```

  Expected: PASS.

- [ ] **Step 5: Commit after each module extraction**

  Use one commit per module:

  ```powershell
  git commit -m "refactor: extract platform validation"
  git commit -m "refactor: extract semantic fixture validation"
  git commit -m "refactor: extract agent prompt validation"
  ```

---

### Task 7: Defer Content And Retrieval Enhancements

**Files:**
- Later create: `docs/architecture/terminology-glossary.md`
- Later modify: `context/中观应成精要.md`
- Later create: `docs/architecture/agama-chunk-index.md`

**Interfaces:**
- No code changes in this maintenance milestone.

- [ ] **Step 1: Record the backlog order**

  Update `docs/maintenance-roadmap.md` after Tasks 1-6 to list:

  ```text
  P1: validate_zilan_repo modularization
  P1: harness/test cleanup
  P2: package metadata cleanup
  P2: Sanskrit/Chinese glossary
  P2: Madhyamaka two-truths expansion
  P2: Agama chunk index design
  ```

- [ ] **Step 2: Do not implement content changes in the validation-refactor PRs**

  Keep glossary, Madhyamaka expansion, and Agama chunk-index work as separate PRs after the engineering baseline is stable.

---

## Validation Plan

Run after every PR:

```powershell
python scripts\validate_zilan_repo.py --check-generated --strict-yaml
python -m pytest
python -m ruff check scripts tests
python -m mypy
git diff --check
```

Provider/runtime status must remain unchanged unless a separate runtime-validation PR records dated evidence.

## Rollback Path

Each task is additive or behavior-preserving. If an extraction causes failures, revert that one PR and keep the previous root-level `validate_zilan_repo.py` behavior. Do not revert unrelated reasoning fixtures, runtime evidence, or platform metadata.

## What Not To Do Yet

- Do not split all 1600+ lines of `validate_zilan_repo.py` in one PR.
- Do not rewrite validators into a new framework.
- Do not change answer contracts while doing validation refactors.
- Do not add a vector database for Agama chunking yet.
- Do not mark native OpenAI, DeepSeek, GLM, or Qwen as tested.
- Do not add new Buddhist doctrinal claims in maintenance PRs.

## Self-Review

- Spec coverage: all ten user suggestions are represented. Items 1-7 are engineering tasks; items 8-10 are deferred as separate content/retrieval PRs.
- Placeholder scan: no TBD markers are present.
- Type consistency: all planned validation functions use existing list-based failure/warning sinks and preserve stable root CLI behavior.
