# zilan_contract Productization Closeout

> Date: 2026-08-05
> Baseline: v2.5.7 plus post-release PRs #171 through #174
> Scope: package product surface only. This is not provider runtime validation and does not change `docs/platform-validation.md`.

## Closeout Status

The P2 productization sweep is closed for the current `zilan_contract` public surface.

The package now has four stable installed surfaces:

1. Python API: `ContractRunner`, `AnswerContractRunner`, `HetuvidyaValidator`, `ContractResult`, issue helpers, and fixture-path helpers.
2. Module CLI: `python -m zilan_contract.cli check`.
3. Console script: `zilan-contract check` from `[project.scripts]`.
4. Bundled examples and fixtures: domain-neutral medical/legal/financial examples plus the checked-in reasoning and answer-contract samples needed by the public quickstart.

## Completion Criteria

The closeout is considered complete because the repository now guards the failure modes that previously made the package look healthier in-source than after installation:

| Criterion | Evidence |
| --- | --- |
| Public API works after installation | `tests/test_zilan_contract_installed_smoke.py`, `tests/test_zilan_contract_wheel_smoke.py` |
| Bundled answer samples are included | `tests/test_packaging_metadata.py`, `tests/test_zilan_contract_wheel_smoke.py` |
| CLI schema failures are explicit | `tests/test_zilan_contract_cli.py`, `tests/test_zilan_contract_installed_smoke.py` |
| Console script works outside the source checkout | `tests/test_zilan_contract_installed_smoke.py`, `tests/test_zilan_contract_wheel_smoke.py` |
| Wheel build/install works outside the source checkout | `tests/test_zilan_contract_wheel_smoke.py` |
| Schema reference documents public semantics | `docs/zilan-contract-schema.md`, `tests/test_zilan_contract_schema_docs.py` |
| Quickstart examples map to packaged behavior | `docs/zilan-contract-quickstart.md`, installed-package smoke tests |

## Boundaries

This closeout does not claim that `zilan_contract` performs semantic grading or provider validation.

Explicit non-goals:

- no LLM-as-judge behavior;
- no provider calls;
- no native OpenAI API status promotion;
- no Buddhist doctrinal grading;
- no CBETA publication-grade collation;
- no regex, fuzzy matching, Unicode normalization, or semantic similarity in the v2.5.7 schema.

The installed package can verify deterministic output contracts and expose fixture-backed reasoning validator outputs. It cannot prove that a generated answer is doctrinally correct or that a provider route is `tested`.

## Release Guardrail

Before publishing a package release that changes `zilan_contract`, run at minimum:

```powershell
python scripts\validate_zilan_repo.py --check-generated --strict-yaml
python -m pytest tests\test_zilan_contract_installed_smoke.py tests\test_zilan_contract_wheel_smoke.py tests\test_zilan_contract_examples.py tests\test_packaging_metadata.py
python -m ruff check scripts tests zilan_contract
python -m mypy
```

For release-candidate confidence, run full `python -m pytest` and keep the README metrics aligned with the observed test count and coverage.

## Next Work

Allowed next work should stay narrow:

- compatibility maintenance for the current API, CLI, and schema;
- clearer error messages when a real user reports a confusing failure;
- release metadata updates when accumulated `[Unreleased]` entries justify a new tag;
- separate design PRs for any schema v2 features such as regex, case-insensitive matching, or structured boolean logic.

Do not start FastAPI, Web UI, vector retrieval, or broad provider expansion as a direct continuation of this productization closeout. Those belong to separate architecture tracks with their own validation evidence.