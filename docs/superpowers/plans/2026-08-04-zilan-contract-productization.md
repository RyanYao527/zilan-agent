# zilan_contract Productization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Productize `zilan_contract` as a small, reusable output-contract SDK while keeping Zilan Buddhist reasoning as the flagship domain.

**Architecture:** Keep existing root scripts and `ContractRunner` behavior stable. Add a clearer public API, domain-neutral answer-contract runner, CLI/report surface, and examples without provider calls or platform-status changes. Preserve `zilanlib` as the internal engine and expose only ergonomic package-level entrypoints from `zilan_contract`.

**Tech Stack:** Python 3.10+, PyYAML, pytest, ruff, mypy, setuptools package data.

## Global Constraints

- Do not modify `docs/platform-validation.md` or promote any route to `tested`.
- Do not call provider APIs or add live runtime evidence in productization PRs.
- Preserve current imports: `ContractRunner`, `ContractResult`, `HetuvidyaValidator`, `get_fixture_path`, and `get_cases_path`.
- Do not add dependencies beyond existing `PyYAML>=6.0` unless a later PR proves the need.
- Keep root CLI wrappers stable; add new package API beside them.
- Keep each PR narrow, testable, and reversible.
- Run before merge: `python scripts\validate_zilan_repo.py --check-generated --strict-yaml`, `python -m pytest`, `python -m ruff check scripts tests`, `python -m mypy`.

---

## Current-State Readout

- `zilan_contract` currently exposes a useful but compact API from `zilan_contract/__init__.py`.
- `ContractRunner` wraps the full reasoning contract runner and is best suited to Zilan/SRQ fixtures.
- The quickstart already claims generic medical/legal/financial use, but the easiest API path is still shaped by Zilan retrieval fixtures and reasoning cases.
- Installed-package smoke coverage exists and checks bundled fixtures, third-party notices, and source-anchor boundaries.
- The product gap is not more validator depth. The P1 gap is external-user ergonomics: clear result objects, domain-neutral contract checks, a CLI/report path, and copy-paste examples.

## Productization PR Sequence

| PR | Theme | Expected impact | Risk |
| --- | --- | --- | --- |
| P1-A | Public result ergonomics | Make failures explainable without inspecting `raw`. | Low; additive API. |
| P1-B | Domain-neutral answer-contract runner | Let non-Buddhist projects use required/forbidden/slot checks without SRQ fixtures. | Medium; new public API. |
| P1-C | CLI and report output | Make package usable in CI without Python glue code. | Medium; packaging entrypoint. |
| P1-D | Examples and docs | Prove medical/legal/finance-style generalization with committed examples. | Low; docs + tests. |
| P1-E | Installed package hardening | Ensure public API and CLI work after `pip install --target`. | Low; test coverage. |

---

### Task 1: Public Result Ergonomics

**Files:**
- Create: `zilan_contract/results.py`
- Modify: `zilan_contract/__init__.py`
- Test: `tests/test_zilan_contract_public_results.py`

**Interfaces:**
- Produces: `ContractIssue(source: str, contract_id: str, kind: str, label: str, detail: str)`
- Produces: `ContractResult.issues() -> list[ContractIssue]`
- Produces: `ContractResult.to_summary() -> dict[str, object]`
- Produces: `ContractResult.to_markdown() -> str`
- Preserves: `ContractResult.raw`, `overall_status`, `answer_review_status`, `validators`, `query_id`, `query`, `passed()`, `failed_validators()`

- [x] **Step 1: Write failing public result tests**

```python
from __future__ import annotations

from zilan_contract import ContractRunner, ContractResult
from zilan_contract.results import ContractIssue


def test_contract_result_extracts_answer_contract_issues() -> None:
    result = ContractRunner(source_root=None).check(
        query_id="SRQ-04",
        sample_id="srq04-agama-citation-boundary-fail",
    )

    issues = result.issues()

    assert issues
    assert all(isinstance(issue, ContractIssue) for issue in issues)
    assert any(issue.kind == "missing_required_term" for issue in issues)
    assert any(issue.kind == "present_forbidden_term" for issue in issues)


def test_contract_result_summary_and_markdown_are_stable() -> None:
    result = ContractRunner(source_root=None).check(
        query_id="SRQ-05",
        sample_id="srq05-hetuvidya-non-pervasive-pass",
    )

    assert result.to_summary() == {
        "overall_status": "pass",
        "answer_review_status": "pass",
        "query_id": "SRQ-05",
        "failed_validators": [],
        "issue_count": 0,
    }
    markdown = result.to_markdown()
    assert "# zilan_contract Review" in markdown
    assert "Overall status: pass" in markdown
    assert "Failed validators: none" in markdown


def test_contract_result_import_remains_backward_compatible() -> None:
    result = ContractResult({"overall_status": "pass", "validators": {}})

    assert result.passed() is True
    assert result.failed_validators() == []
```

- [x] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests\test_zilan_contract_public_results.py -q`

Expected: fail because `zilan_contract.results` or `ContractResult.issues` does not exist.

- [x] **Step 3: Move `ContractResult` into `zilan_contract/results.py` and add issue helpers**

Implementation shape:

```python
from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ContractIssue:
    source: str
    contract_id: str
    kind: str
    label: str
    detail: str


class ContractResult:
    def __init__(self, raw: dict[str, Any]):
        self.raw = raw
        self.overall_status: str = str(raw.get("overall_status", "unknown"))
        self.answer_review_status: str = str(raw.get("answer_review_status", "unknown"))
        validators = raw.get("validators", {})
        self.validators: dict[str, Any] = validators if isinstance(validators, dict) else {}
        self.query_id: str | None = raw.get("query_id") if isinstance(raw.get("query_id"), str) else None
        self.query: str | None = raw.get("query") if isinstance(raw.get("query"), str) else None

    def __repr__(self) -> str:
        return f"ContractResult(overall={self.overall_status!r}, review={self.answer_review_status!r})"

    def passed(self) -> bool:
        return self.overall_status == "pass"

    def failed_validators(self) -> list[str]:
        return [name for name, item in self.validators.items() if item.get("status") not in ("pass", "not_applicable")]

    def issues(self) -> list[ContractIssue]:
        review = self.raw.get("answer_contract_review")
        if not isinstance(review, dict):
            return []
        issues: list[ContractIssue] = []
        for item in review.get("reviews", []):
            if not isinstance(item, dict):
                continue
            contract_id = str(item.get("contract_id", ""))
            for term in item.get("missing_required_terms", []):
                issues.append(ContractIssue("answer_contract", contract_id, "missing_required_term", str(term), str(term)))
            for term in item.get("present_forbidden_terms", []):
                issues.append(ContractIssue("answer_contract", contract_id, "present_forbidden_term", str(term), str(term)))
            for label in item.get("missing_required_slots", []):
                issues.append(ContractIssue("answer_contract", contract_id, "missing_required_slot", str(label), str(label)))
        return issues

    def to_summary(self) -> dict[str, object]:
        return {
            "overall_status": self.overall_status,
            "answer_review_status": self.answer_review_status,
            "query_id": self.query_id,
            "failed_validators": self.failed_validators(),
            "issue_count": len(self.issues()),
        }

    def to_markdown(self) -> str:
        failed = ", ".join(self.failed_validators()) or "none"
        lines = [
            "# zilan_contract Review",
            "",
            f"Overall status: {self.overall_status}",
            f"Answer review status: {self.answer_review_status}",
            f"Query ID: {self.query_id or 'none'}",
            f"Failed validators: {failed}",
            "",
            "## Issues",
        ]
        issues = self.issues()
        if not issues:
            lines.append("- none")
        else:
            for issue in issues:
                lines.append(f"- {issue.contract_id}: {issue.kind} `{issue.label}`")
        return "\n".join(lines).rstrip() + "\n"
```

Modify `zilan_contract/__init__.py` to import `ContractResult` from `zilan_contract.results` and remove only the old inline class definition.

- [x] **Step 4: Run targeted tests**

Run:

```powershell
python -m pytest tests\test_zilan_contract_public_results.py tests\test_zilan_contract_installed_smoke.py -q
```

Expected: all selected tests pass.

- [x] **Step 5: Commit**

```powershell
git add zilan_contract\results.py zilan_contract\__init__.py tests\test_zilan_contract_public_results.py
git commit -m "Add public zilan_contract result summaries"
```

---

### Task 2: Domain-Neutral Answer Contract Runner

**Files:**
- Create: `zilan_contract/answer_contracts.py`
- Modify: `zilan_contract/__init__.py`
- Test: `tests/test_zilan_contract_answer_contracts.py`

**Interfaces:**
- Produces: `AnswerContractRunner.check(answer_text: str, contracts: dict[str, object]) -> AnswerContractResult`
- Produces: `AnswerContractRunner.check_file(answer_file: Path, contracts: dict[str, object]) -> AnswerContractResult`
- Produces: `AnswerContractResult.overall_status`, `reviews`, `issues()`, `passed()`, `to_summary()`, `to_markdown()`
- This runner does not require SRQ query fixtures, retrieval chunks, reasoning cases, or local Agama source roots.

- [x] **Step 1: Write failing generic-runner tests**

```python
from __future__ import annotations

from zilan_contract import AnswerContractRunner


CONTRACTS = {
    "medical_disclaimer": {
        "description": "Medical answer must include emergency and advice boundaries.",
        "required_terms": ["not medical advice", "doctor", "emergency"],
        "forbidden_terms": ["guaranteed", "definitely"],
        "required_slots": [
            {"label": "disclaimer", "terms": ["not medical advice"]},
            {"label": "care_path", "terms": ["doctor", "emergency"]},
        ],
    }
}


def test_answer_contract_runner_passes_domain_neutral_answer() -> None:
    result = AnswerContractRunner().check(
        answer_text="This is not medical advice. Call emergency services or consult a doctor.",
        contracts=CONTRACTS,
    )

    assert result.overall_status == "pass"
    assert result.passed() is True
    assert result.issues() == []


def test_answer_contract_runner_reports_missing_and_forbidden_terms() -> None:
    result = AnswerContractRunner().check(
        answer_text="Turmeric tea is guaranteed to help. It definitely works.",
        contracts=CONTRACTS,
    )

    assert result.overall_status == "fail"
    summary = result.to_summary()
    assert summary["issue_count"] == 7
    assert {issue.kind for issue in result.issues()} == {
        "missing_required_term",
        "present_forbidden_term",
        "missing_required_slot",
    }
    assert "medical_disclaimer" in result.to_markdown()
```

- [x] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests\test_zilan_contract_answer_contracts.py -q`

Expected: fail because `AnswerContractRunner` does not exist.

- [x] **Step 3: Implement the generic runner**

Implementation shape:

```python
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from zilan_contract.results import ContractIssue


@dataclass(frozen=True)
class AnswerContractResult:
    overall_status: str
    reviews: list[dict[str, Any]]

    def passed(self) -> bool:
        return self.overall_status == "pass"

    def issues(self) -> list[ContractIssue]:
        issues: list[ContractIssue] = []
        for review in self.reviews:
            contract_id = str(review["contract_id"])
            for term in review["missing_required_terms"]:
                issues.append(ContractIssue("answer_contract", contract_id, "missing_required_term", str(term), str(term)))
            for term in review["present_forbidden_terms"]:
                issues.append(ContractIssue("answer_contract", contract_id, "present_forbidden_term", str(term), str(term)))
            for label in review["missing_required_slots"]:
                issues.append(ContractIssue("answer_contract", contract_id, "missing_required_slot", str(label), str(label)))
        return issues

    def to_summary(self) -> dict[str, object]:
        return {
            "overall_status": self.overall_status,
            "contract_count": len(self.reviews),
            "issue_count": len(self.issues()),
        }

    def to_markdown(self) -> str:
        lines = ["# Answer Contract Review", "", f"Overall status: {self.overall_status}", "", "## Contracts"]
        for review in self.reviews:
            lines.append(f"- {review['contract_id']}: {review['status']}")
        return "\n".join(lines).rstrip() + "\n"


class AnswerContractRunner:
    def check(self, *, answer_text: str, contracts: dict[str, object]) -> AnswerContractResult:
        reviews = [_review_contract(contract_id, contract, answer_text) for contract_id, contract in contracts.items()]
        status = "pass" if reviews and all(review["status"] == "pass" for review in reviews) else "fail"
        return AnswerContractResult(overall_status=status, reviews=reviews)

    def check_file(self, *, answer_file: Path, contracts: dict[str, object]) -> AnswerContractResult:
        return self.check(answer_text=answer_file.read_text(encoding="utf-8"), contracts=contracts)
```

Reuse the existing term/slot semantics from `scripts/zilanlib/semantic/answer_contract_review.py`: required terms must all appear, forbidden terms must not appear, and each required slot passes when at least one slot term appears.

- [x] **Step 4: Export public API**

Modify `zilan_contract/__init__.py`:

```python
from zilan_contract.answer_contracts import AnswerContractResult, AnswerContractRunner
from zilan_contract.results import ContractIssue, ContractResult

__all__ = [
    "AnswerContractResult",
    "AnswerContractRunner",
    "ContractIssue",
    "ContractRunner",
    "ContractResult",
    "HetuvidyaValidator",
    "get_fixture_path",
    "get_cases_path",
    "__version__",
]
```

- [x] **Step 5: Run targeted tests**

Run:

```powershell
python -m pytest tests\test_zilan_contract_answer_contracts.py tests\test_zilan_contract_public_results.py -q
```

Expected: all selected tests pass.

- [x] **Step 6: Commit**

```powershell
git add zilan_contract\answer_contracts.py zilan_contract\__init__.py tests\test_zilan_contract_answer_contracts.py
git commit -m "Add domain-neutral answer contract runner"
```

---

### Task 3: CLI And Report Output

**Files:**
- Create: `zilan_contract/cli.py`
- Modify: `pyproject.toml`
- Test: `tests/test_zilan_contract_cli.py`

**Interfaces:**
- Produces console script: `zilan-contract`
- Produces command: `zilan-contract check --contract-file <path> --answer-file <path> --json`
- Produces command: `zilan-contract check --contract-file <path> --answer-file <path> --markdown`
- Contract file schema: top-level `contracts` mapping using the same required/forbidden/slot fields as `AnswerContractRunner`.

- [x] **Step 1: Write failing CLI tests**

```python
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def test_zilan_contract_cli_check_outputs_json(tmp_path: Path) -> None:
    contract_file = tmp_path / "contracts.yaml"
    answer_file = tmp_path / "answer.md"
    contract_file.write_text(
        """
contracts:
  financial_risk:
    required_terms:
      - not financial advice
      - risk
    forbidden_terms:
      - guaranteed return
    required_slots:
      - label: boundary
        terms:
          - not financial advice
""".strip(),
        encoding="utf-8",
    )
    answer_file.write_text("This is not financial advice. Investment involves risk.", encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "zilan_contract.cli",
            "check",
            "--contract-file",
            str(contract_file),
            "--answer-file",
            str(answer_file),
            "--json",
        ],
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=True,
    )

    data = json.loads(result.stdout)
    assert data["overall_status"] == "pass"
    assert data["issue_count"] == 0


def test_zilan_contract_cli_check_exits_nonzero_on_fail(tmp_path: Path) -> None:
    contract_file = tmp_path / "contracts.yaml"
    answer_file = tmp_path / "answer.md"
    contract_file.write_text(
        "contracts:\n  legal_boundary:\n    required_terms: ['not legal advice']\n",
        encoding="utf-8",
    )
    answer_file.write_text("This is definitive legal advice.", encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "zilan_contract.cli",
            "check",
            "--contract-file",
            str(contract_file),
            "--answer-file",
            str(answer_file),
            "--markdown",
        ],
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=False,
    )

    assert result.returncode == 1
    assert "# Answer Contract Review" in result.stdout
    assert "legal_boundary" in result.stdout
```

- [x] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests\test_zilan_contract_cli.py -q`

Expected: fail because `zilan_contract.cli` does not exist.

- [x] **Step 3: Implement CLI**

Implement `zilan_contract/cli.py` with `argparse`, `json`, and `yaml.safe_load`. The command returns `0` for pass and `1` for fail.

```python
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import yaml

from zilan_contract import AnswerContractRunner


def _load_contracts(path: Path) -> dict[str, object]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("contracts"), dict):
        raise ValueError("Contract file must contain a top-level contracts mapping.")
    return data["contracts"]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="zilan-contract")
    subparsers = parser.add_subparsers(dest="command", required=True)
    check = subparsers.add_parser("check")
    check.add_argument("--contract-file", type=Path, required=True)
    check.add_argument("--answer-file", type=Path, required=True)
    output = check.add_mutually_exclusive_group()
    output.add_argument("--json", action="store_true")
    output.add_argument("--markdown", action="store_true")
    args = parser.parse_args(argv)

    try:
        contracts = _load_contracts(args.contract_file)
        result = AnswerContractRunner().check_file(answer_file=args.answer_file, contracts=contracts)
    except (OSError, ValueError) as exc:
        parser.exit(2, f"zilan-contract failed: {exc}\n")

    if args.json:
        print(json.dumps(result.to_summary(), ensure_ascii=False, indent=2))
    else:
        print(result.to_markdown(), end="")
    return 0 if result.passed() else 1


if __name__ == "__main__":
    raise SystemExit(main())
```

- [x] **Step 4: Add package script entrypoint**

Modify `pyproject.toml`:

```toml
[project.scripts]
zilan-contract = "zilan_contract.cli:main"
```

- [x] **Step 5: Run targeted tests**

Run:

```powershell
python -m pytest tests\test_zilan_contract_cli.py tests\test_packaging_metadata.py -q
```

Expected: selected tests pass after updating `tests/test_packaging_metadata.py` to assert the new `[project.scripts]` entry.

- [x] **Step 6: Commit**

```powershell
git add zilan_contract\cli.py pyproject.toml tests\test_zilan_contract_cli.py tests\test_packaging_metadata.py
git commit -m "Add zilan_contract CLI"
```

---

### Task 4: Domain-Neutral Examples And Documentation

**Files:**
- Create: `docs/examples/zilan-contract/medical-disclaimer.yaml`
- Create: `docs/examples/zilan-contract/medical-disclaimer-pass.md`
- Create: `docs/examples/zilan-contract/medical-disclaimer-fail.md`
- Create: `docs/examples/zilan-contract/legal-boundary.yaml`
- Create: `docs/examples/zilan-contract/financial-risk.yaml`
- Modify: `docs/zilan-contract-quickstart.md`
- Modify: `README.md`
- Modify: `CHANGELOG.md`
- Test: `tests/test_zilan_contract_examples.py`

**Interfaces:**
- Examples use the CLI contract schema from Task 3.
- Examples are docs-only fixtures and are not platform validation evidence.

- [x] **Step 1: Write failing example smoke tests**

```python
from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "docs" / "examples" / "zilan-contract"


def test_medical_disclaimer_examples_are_executable() -> None:
    pass_result = subprocess.run(
        [
            sys.executable,
            "-m",
            "zilan_contract.cli",
            "check",
            "--contract-file",
            str(EXAMPLES / "medical-disclaimer.yaml"),
            "--answer-file",
            str(EXAMPLES / "medical-disclaimer-pass.md"),
            "--json",
        ],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=True,
    )
    assert '"overall_status": "pass"' in pass_result.stdout

    fail_result = subprocess.run(
        [
            sys.executable,
            "-m",
            "zilan_contract.cli",
            "check",
            "--contract-file",
            str(EXAMPLES / "medical-disclaimer.yaml"),
            "--answer-file",
            str(EXAMPLES / "medical-disclaimer-fail.md"),
            "--json",
        ],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=False,
    )
    assert fail_result.returncode == 1
    assert '"overall_status": "fail"' in fail_result.stdout
```

- [x] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests\test_zilan_contract_examples.py -q`

Expected: fail because example files do not exist yet.

- [x] **Step 3: Add examples**

Use this medical example exactly:

```yaml
contracts:
  medical_disclaimer:
    description: "Medical response must include emergency and professional-care boundaries."
    required_terms:
      - "not medical advice"
      - "doctor"
      - "emergency"
    forbidden_terms:
      - "guaranteed"
      - "definitely"
      - "100%"
    required_slots:
      - label: disclaimer
        terms:
          - "not medical advice"
      - label: care_path
        terms:
          - "doctor"
          - "emergency"
```

Pass answer:

```markdown
This is not medical advice. Chest pain can be urgent; contact emergency services
or consult a doctor promptly.
```

Fail answer:

```markdown
This turmeric routine is guaranteed to fix chest pain. It definitely works 100%.
```

- [x] **Step 4: Update quickstart and README**

Add one short section to `docs/zilan-contract-quickstart.md` showing:

```bash
zilan-contract check \
  --contract-file docs/examples/zilan-contract/medical-disclaimer.yaml \
  --answer-file docs/examples/zilan-contract/medical-disclaimer-pass.md \
  --json
```

In `README.md`, keep the Buddhist flagship framing but make the reusable product sentence explicit:

```markdown
`zilan_contract` is the reusable SDK inside this repository: a deterministic
output-contract checker for required terms, forbidden phrases, and boundary
slots. Zilan's Buddhist fixtures are the flagship domain, not a limitation of
the pattern.
```

- [x] **Step 5: Run targeted tests**

Run:

```powershell
python -m pytest tests\test_zilan_contract_examples.py -q
python -m ruff check scripts tests
```

Expected: selected tests and ruff pass.

- [x] **Step 6: Commit**

```powershell
git add docs\examples\zilan-contract docs\zilan-contract-quickstart.md README.md CHANGELOG.md tests\test_zilan_contract_examples.py
git commit -m "Add zilan_contract product examples"
```

---

### Task 5: Installed Package And Public API Hardening

**Files:**
- Modify: `tests/test_zilan_contract_installed_smoke.py`
- Modify: `tests/test_packaging_metadata.py`
- Modify: `docs/maintenance-roadmap.md`
- Modify: `CHANGELOG.md`

**Interfaces:**
- Installed package must support importing `AnswerContractRunner`.
- Installed package must support running `python -m zilan_contract.cli check ...`.
- Console entrypoint metadata must be declared in `pyproject.toml`.

- [x] **Step 1: Add installed-package smoke assertions**

Extend `tests/test_zilan_contract_installed_smoke.py` with a test that installs to `--target`, imports `AnswerContractRunner`, and checks a pass/fail inline contract.

```python
def test_installed_package_exposes_answer_contract_runner(tmp_path: Path) -> None:
    target = _install_package_to_target(tmp_path)
    data = _run_installed_package(
        target,
        tmp_path,
        textwrap.dedent(
            """
            import json
            from zilan_contract import AnswerContractRunner

            contracts = {
                "support_boundary": {
                    "required_terms": ["not therapy", "professional support"],
                    "forbidden_terms": ["guaranteed cure"],
                }
            }
            result = AnswerContractRunner().check(
                answer_text="This is not therapy; consider professional support.",
                contracts=contracts,
            )
            print(json.dumps(result.to_summary(), ensure_ascii=False))
            """
        ),
    )

    assert data["overall_status"] == "pass"
    assert data["issue_count"] == 0
```

- [x] **Step 2: Run installed-package smoke**

Run: `python -m pytest tests\test_zilan_contract_installed_smoke.py -q`

Expected: pass.

- [x] **Step 3: Update roadmap and changelog**

In `docs/maintenance-roadmap.md`, update the community deliverables or coverage baseline row to mention the productized `zilan_contract` API and CLI.

In `CHANGELOG.md` under `[Unreleased] / Added`, add:

```markdown
- Added productized `zilan_contract` public result helpers, a domain-neutral answer-contract runner, CLI/report output, and reusable examples without provider calls or platform-status changes.
```

- [x] **Step 4: Run full baseline**

Run:

```powershell
python scripts\validate_zilan_repo.py --check-generated --strict-yaml
python -m pytest
python -m ruff check scripts tests
python -m mypy
```

Expected: all pass.

- [x] **Step 5: Commit**

```powershell
git add tests\test_zilan_contract_installed_smoke.py tests\test_packaging_metadata.py docs\maintenance-roadmap.md CHANGELOG.md
git commit -m "Harden zilan_contract package product surface"
```

---

## Validation Plan

For every PR:

```powershell
python -m pytest <new-or-targeted-tests> -q
python -m ruff check scripts tests
```

Before merge:

```powershell
python scripts\validate_zilan_repo.py --check-generated --strict-yaml
python -m pytest
python -m ruff check scripts tests
python -m mypy
```

No PR in this P1 sequence should run provider live calls, edit `docs/platform-validation.md`, or change platform tested status.

## Rollback Path

- P1-A rollback: revert `zilan_contract/results.py` and restore inline `ContractResult` in `zilan_contract/__init__.py`.
- P1-B rollback: remove `zilan_contract/answer_contracts.py` and the added exports; existing `ContractRunner` remains unchanged.
- P1-C rollback: remove `zilan_contract/cli.py` and `[project.scripts]`; Python API remains usable.
- P1-D rollback: remove `docs/examples/zilan-contract/` and docs references.
- P1-E rollback: revert installed-package smoke additions and roadmap/changelog wording.

## What Not To Do Yet

- Do not build a web UI or hosted service.
- Do not add LangChain, LlamaIndex, vector databases, FastAPI, Docker, queues, or schedulers.
- Do not turn deterministic contract checks into an LLM judge.
- Do not broaden provider validation in the same PR sequence.
- Do not make Zilan Buddhist fixtures less strict to make generic examples easier.
- Do not change package name or import path during P1; keep `pip install zilan-agent` and `import zilan_contract`.

## Estimated Work

| Item | Realistic effort |
| --- | --- |
| P1-A result ergonomics | 1.5-2.5 hours |
| P1-B domain-neutral runner | 2-3 hours |
| P1-C CLI/report | 2-3 hours |
| P1-D examples/docs | 1.5-2 hours |
| P1-E installed-package hardening and full baseline | 1-2 hours |
| Total P1 productization | 8-12.5 hours |

The work should be split across 3-5 PRs. Stop after each PR if CI reveals unexpected package or fixture coupling.
