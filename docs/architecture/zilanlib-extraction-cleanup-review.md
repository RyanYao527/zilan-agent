# zilanlib Extraction Cleanup Review

> Last updated: 2026-07-13  
> Status: architecture cleanup review, not runtime validation.

This note closes the current `zilanlib` extraction sweep. It documents which root-level scripts now act as stable command-line wrappers, which scripts still contain substantive entrypoint logic, and which follow-up work has the highest return.

This review does not change provider status, platform validation status, runtime evidence, prompts, or doctrinal claims. Platform status remains governed by `agents/openai.yaml` and `docs/platform-validation.md`.

## Scope

Reviewed surfaces:

- `scripts/*.py`
- `scripts/zilanlib/`
- `docs/maintenance-roadmap.md`
- `CHANGELOG.md`
- `scripts/validate_zilan_repo.py`

No provider calls, transcript reviews, Codex/Claude Code reruns, or native OpenAI live validation runs were executed for this review.

## Current Classification

| Script group | Current state | Cleanup decision |
|---|---|---|
| Semantic retrieval and answer review | `semantic_context_bundle.py`, `semantic_role_coverage.py`, `semantic_answer_boundary_review.py`, `semantic_answer_contract_review.py`, and `semantic_retrieval_dry_run.py` are stable CLI wrappers over `scripts/zilanlib/semantic/`. | No further split needed before the next release. |
| Agama search and fixture helpers | `search_agama.py`, `semantic_fixture_candidates.py`, and `semantic_fixture_review.py` expose stable CLI and compatibility surfaces over `scripts/zilanlib/agama/`. | Preserve the root scripts because downstream docs, prompts, and smoke tests reference them directly. |
| Reasoning validators | `hetuvidya_validator.py`, `collected_topics_analyzer.py`, `madhyamaka_critique_engine.py`, `cognitive_analysis_mapper.py`, and `agama_evidence_checker.py` are stable CLI wrappers over `scripts/zilanlib/reasoning/`. | Extraction target is complete for the current fixture-only validators. |
| Reasoning contract runner | `reasoning_contract_runner.py` is a stable CLI wrapper over `scripts/zilanlib/reasoning/contract_runner.py`, while preserving text rendering and CLI error handling at the root entrypoint. | Keep as the user-facing local runner. |
| Shared validator output | `reasoning_validator_output.py` is a compatibility shim over `scripts/zilanlib/reasoning/validator_output.py`. | Keep the shim until older imports are no longer useful. |
| Repository validation | `validate_zilan_repo.py` still contains repository invariant checks and remains the canonical validation entrypoint. | Do not split now; the script is intentionally an integration boundary for local and CI checks. |
| OpenAI/API provider harness | `openai_api_harness.py` still contains harness request construction, provider routing, and optional live-call logic. | Defer extraction until native OpenAI live validation or multi-provider harness work creates a concrete need. |
| Agama corpus generation | `build_agama_context.py` still contains CBETA XML-to-Markdown generation logic. | Defer extraction; it is a narrow corpus-generation pipeline with idempotency coverage and high churn risk. |
| Installation smoke | `mock_install_smoke.py` still contains mock install setup and validation logic. | Defer extraction; it is a small operational smoke-test entrypoint. |

## Decision

The current extraction sweep should stop here.

Reason:

- The repeated semantic, Agama fixture, and reasoning-contract helpers now live under `scripts/zilanlib/`.
- Root scripts remain stable user-facing CLIs, which protects documented commands and existing agent prompts.
- The remaining root scripts are either integration entrypoints (`validate_zilan_repo.py`, `openai_api_harness.py`), one-purpose generators (`build_agama_context.py`), or operational smoke tests (`mock_install_smoke.py`).
- Splitting those remaining scripts now would mainly increase indirection without improving reasoning quality, citation integrity, or validation evidence.

## Recommended Next Work

Highest-ROI next step:

1. Prepare release hygiene for the accumulated `zilanlib` extraction series.
2. Cut a new release after checks pass so `CHANGELOG.md`, Git tags, and GitHub Releases match the repository state.

Useful follow-ups after release hygiene:

- Native OpenAI API live validation when `OPENAI_API_KEY` is available.
- A targeted provider-harness extraction only if more providers need shared harness internals.
- A targeted `validate_zilan_repo.py` split only if specific invariant groups become hard to test or maintain.
- Further reasoning fixture expansion only when a concrete contract gap is identified.

## What Not To Do Yet

- Do not add a broad application framework, service layer, or plugin architecture for these scripts.
- Do not move stable root CLI names without a compatibility shim.
- Do not merge provider-compatible live evidence into native OpenAI API validation.
- Do not split `build_agama_context.py` unless the corpus-generation workflow itself changes.

## Rollback

This review is documentation plus repository-invariant registration. Rollback is limited to removing this document and its references from `docs/maintenance-roadmap.md`, `CHANGELOG.md`, and `scripts/validate_zilan_repo.py`.
