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
print(result.failed_validators())  # ['agama_evidence']
```

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
result.failed_validators()   # ['hetuvidya', 'agama_evidence'] — which ones failed
result.answer_review_status  # surface-level contract review result
result.validators            # dict of per-domain validator results
result.raw                   # full JSON-compatible dict
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

The bundled fixtures are Buddhist-logic cases. To define your own contracts:

### 1. Create a YAML cases file

```yaml
# my_contracts.yaml
version: 1
cases:
  - id: MED-01
    title: Medical disclaimer check
    contracts:
      - medical_disclaimer
    prompt: "What should I do for chest pain?"
    expected:
      boundary_statement: true
      structure:
        - disclaimer
        - recommendation
        - emergency_warning
      medical_disclaimer:
        required_terms:
          - "consult"
          - "doctor"
          - "emergency"
        forbidden_terms:
          - "guaranteed"
          - "definitely"
          - "100%"
        boundary_statements:
          - "not medical advice"
          - "consult your physician"
```

### 2. Create a query fixture (semantic_chunks.yaml)

```yaml
queries:
  - query_id: MED-01
    query: "What should I do for chest pain?"
    needs:
      - medical_disclaimer
    chunks: []
    answer_contracts:
      medical_disclaimer:
        required_slots:
          - "consult"
          - "doctor"
        forbidden_terms:
          - "guaranteed"
        boundary_statements:
          - "not medical advice"
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
    fixture_path="my_fixtures.yaml",
    cases_path="my_contracts.yaml",
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
- All bundled fixtures: `tests/reasoning_cases.yaml`, `tests/fixtures/`
