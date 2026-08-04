# zilan-contract: Quickstart

> `pip install` the output-contract pattern and use it in your own project — no Buddhist
> knowledge required, no model calls, no API keys.

## Installation

```bash
pip install zilan-agent
# The package name on PyPI is 'zilan-agent', but you import it as 'zilan_contract':
```

Or from source:

```bash
git clone https://github.com/RyanYao527/zilan-agent.git
cd zilan-agent
pip install -e ".[dev]"
```

## 60-second try

```python
from zilan_contract import ContractRunner

runner = ContractRunner()

# Check a known-good Agama citation response
result = runner.check(
    query_id="SRQ-04",
    sample_id="srq04-agama-citation-boundary-pass",
)
print(result.overall_status)  # 'pass'
print(result.passed())        # True

# Check a known-bad response (overclaims scholarly finality)
result = runner.check(
    query_id="SRQ-04",
    sample_id="srq04-agama-citation-boundary-fail",
)
print(result.overall_status)  # 'fail'
print(result.issues()[0].detail)  # Missing required term: ...
```

## CLI example

Use the package CLI when you want a CI-friendly pass/fail check without writing Python glue code:

```bash
zilan-contract check \
  --contract-file docs/examples/zilan-contract/medical-disclaimer.yaml \
  --answer-file docs/examples/zilan-contract/medical-disclaimer-pass.md \
  --json
```

JSON output includes the compact pass/fail summary plus an `issues` array for machine-readable CI annotations.
See `docs/zilan-contract-schema.md` for the full contract schema, exit codes, and report format.

## Core concepts

### Output contract

An output contract is a structured spec with three layers:

| Layer | What it checks | Example |
| --- | --- | --- |
| **Required slots** | Terms that MUST appear | `检索范围`, `CBETA`, disclaimer |
| **Forbidden terms** | Phrases that must NOT appear | `校勘完成`, `guaranteed cure` |
| **Boundary statements** | Qualifiers that must frame the answer | `待校勘`, `consult your doctor` |

### ContractRunner

The main entry point. It runs all contract checks against a response and returns a `ContractResult`.

```python
from zilan_contract import ContractRunner

runner = ContractRunner()

# Option 1: check a built-in sample
result = runner.check(query_id="SRQ-04", sample_id="srq04-agama-citation-boundary-pass")

# Option 2: check your own text
result = runner.check(
    query_id="SRQ-04",
    answer_text="检索范围：只基于本地 context/agama/ … 待校勘。",
)

# Option 3: check from a file
from pathlib import Path
result = runner.check(
    query_id="SRQ-04",
    answer_file=Path("my_response.md"),
)
```

### ContractResult

```python
result.overall_status       # 'pass' | 'fail' | 'review_needed'
result.passed()              # True if pass
result.failed_validators()   # explicit non-pass validator statuses; 'run' is not a failure
result.answer_review_status  # surface-level contract review result
result.validators            # dict of per-domain validator results
result.raw                   # full JSON-compatible dict
```

### AnswerContractRunner

Use `AnswerContractRunner` when you want the domain-neutral required/forbidden/slot checks without SRQ fixtures:

```python
from zilan_contract import AnswerContractRunner

contracts = {
    "legal_boundary": {
        "required_terms": ["not legal advice"],
        "forbidden_terms": ["guaranteed outcome"],
        "required_slots": [
            {"label": "care_path", "terms": ["attorney", "qualified professional"]},
        ],
    }
}
result = AnswerContractRunner().check(
    answer_text="This is not legal advice. Consult an attorney.",
    contracts=contracts,
)
print(result.to_summary())
print(result.to_markdown())
```

### HetuvidyaValidator

Standalone validator for Buddhist-logic three-mark checks. You can use it directly:

```python
from zilan_contract import HetuvidyaValidator

v = HetuvidyaValidator()
result = v.validate(case_id="ZR-01")
print(result["status"])  # 'pass'
print(result["validations"][0]["judgment"]["result"])  # 'positive_reason'
```

## Using your own contracts

The bundled fixtures are Buddhist-logic cases. To define your own contracts
for any domain (medical, legal, financial, etc.):

### 1. Create a contract fixture file

This defines the query and the answer contract. Save as `my_contracts.yaml`:

```yaml
# my_contracts.yaml
queries:
  - id: MED-01
    query: "What should I do for chest pain?"
    needs:
      - medical_disclaimer
    chunks: []
    answer_contracts:
      medical_disclaimer:
        description: "Medical response must include disclaimer and avoid claims of certainty."
        required_terms:
          - "consult"
          - "doctor"
          - "emergency"
          - "not medical advice"
        forbidden_terms:
          - "guaranteed"
          - "definitely"
          - "100%"
        required_slots:
          - label: disclaimer
            terms:
              - "not medical advice"
              - "consult"
```

> **Note:** `required_terms` is a flat list of strings that must appear.
> `required_slots` is a list of labeled groups; each slot passes when at least
> one of its terms appears. Use separate slots for independent constraints.
> `forbidden_terms` is a flat list of strings that must NOT appear.

### 2. Create a reasoning cases file (optional)

If you want to use domain validators, create a cases file. Otherwise
skip this — the answer contract review works without it. Save as
`my_cases.yaml`:

```yaml
# my_cases.yaml
version: 1
cases:
  - id: MED-01
    title: Medical disclaimer check
    contracts:
      - medical_disclaimer
    prompt: "What should I do for chest pain?"
    expected:
      boundary_statement: true
```

### 3. Create pass/fail answer samples

```markdown
<!-- pass_sample.md -->
DISCLAIMER: This is not medical advice. If you have chest pain,
consult your doctor immediately or go to the emergency room.
```

```markdown
<!-- fail_sample.md -->
Turmeric tea is guaranteed to help with chest pain. It definitely works 100%.
```

### 4. Run

```python
from zilan_contract import ContractRunner

runner = ContractRunner(
    fixture_path="my_contracts.yaml",
    cases_path="my_cases.yaml",
)

# Check against your pass sample
result = runner.check(query_id="MED-01", answer_file="pass_sample.md")
assert result.passed()

# Check against your fail sample
result = runner.check(query_id="MED-01", answer_file="fail_sample.md")
assert not result.passed()
```

## What this is NOT

- **Not an LLM judge.** The validators are deterministic string/pattern checks.
  They verify structure, not semantic correctness.
- **Not a grading system.** Pass/fail means "contract satisfied" / "contract violated,"
  not "good answer" / "bad answer."
- **Not a replacement for human review.** It catches structural errors so humans
  can focus on substance — like a linter for LLM outputs.

## Installed package fixture boundary

When installed from PyPI, `zilan_contract` uses bundled fixtures under `zilan_contract/fixtures/`. These fixtures include deterministic contract YAML and answer samples, but not the full repository `context/agama/` corpus. Agama local source-anchor checks therefore report `not_applicable` in installed-package mode. Run from a source checkout with the repository fixtures when you need local CBETA/context line-anchor validation.

## Direct CLI access

The library wraps the existing CLI scripts. You can also call them directly:

```bash
python scripts/reasoning_contract_runner.py \
  --query-id SRQ-04 \
  --sample-id srq04-agama-citation-boundary-pass \
  --json
```

## Where to go next

- Full zilan-agent docs: [github.com/RyanYao527/zilan-agent](https://github.com/RyanYao527/zilan-agent)
- Architecture overview: `ARCHITECTURE.md`
- Output contract design: `docs/architecture/reasoning-contract.md`
- Bundled package fixtures: `zilan_contract/fixtures/`
- Source fixture mirrors: `tests/reasoning_cases.yaml`, `tests/fixtures/`
