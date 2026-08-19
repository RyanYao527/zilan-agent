# zilan_contract Release Checklist

This checklist keeps the public `zilan_contract` package surface reproducible. It is for deterministic contract checks
only; it does not change provider routes or platform validation status.

## Scope

- Public API unchanged unless a separately designed compatibility PR says otherwise.
- Schema v1 boundary unchanged: exact required terms, forbidden terms, and required slots.
- No regex, fuzzy matching, semantic similarity, nested boolean logic, or schema v2 expansion.
- Do not claim semantic grading, doctrinal grading, medical correctness, legal advice, or LLM-judge behavior.
- no provider calls; package checks must run locally without API keys.

## Pre-Release Checks

Run from a clean source checkout:

```bash
python -m pytest tests/test_zilan_contract_public_results.py tests/test_zilan_contract_answer_contracts.py -q
python -m pytest tests/test_zilan_contract_cli.py tests/test_zilan_contract_examples.py -q
python -m pytest tests/test_zilan_contract_installed_smoke.py tests/test_zilan_contract_wheel_smoke.py tests/test_packaging_metadata.py -q
python scripts/validate_zilan_repo.py --strict-yaml
python -m ruff check scripts tests zilan_contract
python -m mypy
```

Run the installed-package validation path when packaging behavior changes:

```bash
python -m pytest tests/test_zilan_contract_installed_smoke.py tests/test_zilan_contract_wheel_smoke.py -q
```

## Release Notes Boundary

- State that `zilan_contract` is a deterministic output-contract checker.
- State that the public API is unchanged when the release only touches docs, examples, or validation evidence.
- Record any fixture/schema behavior change with a test name and a rollback path.
- Do not promote OpenAI API, Claude Code, Codex, DeepSeek, GLM, Qwen, or OpenAI-compatible provider status from package
  smoke tests.

## Rollback

For a docs-only productization PR, rollback is removal of this checklist update and related quickstart/changelog lines.
For package-surface changes, rollback must also restore affected tests, examples, and fixture package data.
