# Codex Desktop Handoff: OpenAI Harness Provider Preflight

> Date: 2026-08-05
> Source branch: `codex/openai-harness-preflight`
> Merged PR: #177
> Merge commit: `9cad22796d61b500d9705d1da9a7fe70a6f321b7`
> Status: merged to `main`; local `main...origin/main` clean after merge.

## Purpose

This handoff records the provider/openai_api_harness work completed before returning control to Codex Desktop.

The objective was not to run live OpenAI API validation. The objective was to make the existing OpenAI / OpenAI-compatible harness safer to operate by adding a local preflight mode that exposes the resolved route configuration and validation boundary before any live provider call.

## What Changed

### Harness behavior

`scripts/openai_api_harness.py` now supports:

```powershell
python scripts/openai_api_harness.py --preflight --json
python scripts/openai_api_harness.py --provider-route volcengine_openai_compatible --preflight --json
```

Preflight resolves and reports:

- `provider_route`
- `validation_route`
- `validation_status`
- `validation_scope`
- `model`
- `api_surface`
- `base_url`
- `endpoint`
- `api_key_env`
- `api_key_present`
- `status_boundary`

Preflight intentionally does not:

- build a regression-case request body;
- call OpenAI or any compatible provider;
- print API key values;
- mark any platform route as `tested`;
- change `agents/openai.yaml` or `docs/platform-validation.md`.

### Internal structure

The harness now has a shared route-resolution path:

- `HarnessConfig`
- `_resolve_harness_config(...)`
- `build_preflight(...)`

`run_harness(...)` now reuses the same resolved config for dry-run and live paths. This reduces drift between preflight, dry-run, and live execution.

A previous latent live-path fragility was also covered: live mode now has a no-network unit test that monkeypatches `call_openai(...)` and confirms the resolved endpoint is passed through correctly.

## Files Changed In #177

- `scripts/openai_api_harness.py`
- `tests/test_openai_api_harness.py`
- `docs/openai-api-harness.md`
- `docs/provider-routes.md`
- `CHANGELOG.md`

No changes were made to:

- `agents/openai.yaml`
- `docs/platform-validation.md`

## Validation Already Completed

Local validation completed before merge:

```powershell
python scripts\validate_zilan_repo.py --check-generated --strict-yaml
python -m pytest tests\test_openai_api_harness.py
python -m pytest
python -m ruff check scripts tests
python -m mypy
python scripts\openai_api_harness.py --preflight --json
python scripts\openai_api_harness.py --provider-route volcengine_openai_compatible --preflight --json
```

Observed results:

- `validate_zilan_repo.py`: passed
- harness tests: `13 passed`
- full pytest: `245 passed`
- ruff: passed
- mypy: passed across 62 source files
- GitHub PR checks: passed

## Platform Status Boundary

This work does not change platform validation status.

Current relevant status remains:

- Native OpenAI API: `harness-ready`
- Volcengine OpenAI-Compatible: `tested` for ZC-01 through ZC-03 only

A Volcengine-compatible preflight or live result must not be counted as native OpenAI API validation. Native OpenAI API can only move from `harness-ready` to `tested` after a dated live run using official `OPENAI_API_KEY` and the native OpenAI endpoint is recorded according to `docs/platform-validation.md` and `docs/validation-evidence.md`.

## Recommended Codex Desktop Next Step

Use preflight as the first operation before any provider work:

```powershell
python scripts\openai_api_harness.py --preflight --json
python scripts\openai_api_harness.py --provider-route volcengine_openai_compatible --preflight --json
```

Then choose one narrow path:

1. Native OpenAI API live validation, only if a real `OPENAI_API_KEY` is available.
2. Volcengine-compatible expansion from ZC-01 through ZC-03 to ZC-04 through ZC-06, only if broader Volcengine evidence is useful.
3. Provider route cleanup for DeepSeek / GLM / Qwen, keeping them `config-only` or moving to explicitly `blocked` unless real harness evidence exists.

Preferred next PR if staying conservative:

- Add a small runtime-evidence template section for provider preflight outputs, or
- Add CLI smoke coverage for `--preflight --json` if Desktop wants command-line entrypoint coverage beyond direct function tests.

## Do Not Do Yet

Do not immediately add:

- FastAPI service layer;
- Web UI;
- vector database;
- multi-provider live validation in one PR;
- platform status promotion without dated live evidence;
- broad refactor of provider config outside the harness.

## Quick Verification For Desktop

After pulling current `main`, Codex Desktop can verify it is on the expected state with:

```powershell
git log --oneline -3
git status --short --branch
python scripts\openai_api_harness.py --preflight --json
python scripts\openai_api_harness.py --provider-route volcengine_openai_compatible --preflight --json
```

Expected top commit:

```text
9cad227 feat: add OpenAI harness provider preflight (#177)
```
