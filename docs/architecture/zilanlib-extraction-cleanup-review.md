# zilanlib Extraction Cleanup Review

> Last updated: 2026-08-03
> Status: P1 validation cleanup closeout, not runtime validation.

This note closes the P1 `validate_zilan_repo.py` cleanup that followed the earlier `zilanlib` extraction sweep. The validator is now split by responsibility while preserving the root command as the stable local and CI entrypoint.

This review does not change provider status, platform validation status, runtime evidence, prompts, or doctrinal claims. Platform status remains governed by `agents/openai.yaml` and `docs/platform-validation.md`.

## Scope

Reviewed surfaces:

- `scripts/validate_zilan_repo.py`
- `scripts/zilanlib/validation/`
- `scripts/zilanlib/repository.py`
- `scripts/zilanlib/yaml_io.py`
- `tests/test_validate_zilan_repo.py`
- `docs/maintenance-roadmap.md`
- `CHANGELOG.md`

No provider calls, transcript reviews, Codex/Claude Code reruns, or native OpenAI live validation runs were executed for this review.

## Current Classification

| Script group | Current state | Cleanup decision |
|---|---|---|
| Semantic retrieval and answer review | `semantic_context_bundle.py`, `semantic_role_coverage.py`, `semantic_answer_boundary_review.py`, `semantic_answer_contract_review.py`, and `semantic_retrieval_dry_run.py` are stable CLI wrappers over `scripts/zilanlib/semantic/`. | No further split needed before the next release. |
| Agama search and fixture helpers | `search_agama.py`, `semantic_fixture_candidates.py`, and `semantic_fixture_review.py` expose stable CLI and compatibility surfaces over `scripts/zilanlib/agama/`. | Preserve the root scripts because downstream docs, prompts, and smoke tests reference them directly. |
| Reasoning validators | `hetuvidya_validator.py`, `collected_topics_analyzer.py`, `madhyamaka_critique_engine.py`, `cognitive_analysis_mapper.py`, and `agama_evidence_checker.py` are stable CLI wrappers over `scripts/zilanlib/reasoning/`. | Extraction target is complete for the current fixture-only validators. |
| Reasoning contract runner | `reasoning_contract_runner.py` is a stable CLI wrapper over `scripts/zilanlib/reasoning/contract_runner.py`, while preserving text rendering and CLI error handling at the root entrypoint. | Keep as the user-facing local runner. |
| Shared validator output | `reasoning_validator_output.py` is a compatibility shim over `scripts/zilanlib/reasoning/validator_output.py`. | Keep the shim until older imports are no longer useful. |
| Repository validation CLI | `validate_zilan_repo.py` is now the stable CLI and compatibility-alias layer. It delegates orchestration to `scripts/zilanlib/validation/suite.py` and keeps `run_checks` as a compatibility alias. | Cleanup is complete for the current P1 scope. Keep the root command stable for local and CI checks. |
| Repository validation modules | `scripts/zilanlib/validation/` now owns repository metadata, platform YAML metadata, public docs, runtime evidence, regression cases, reasoning cases, retrieval chunks, agent prompts, Agama corpus checks, and suite orchestration. | Continue adding tests inside the relevant module instead of rebuilding a large root validator. |
| OpenAI/API provider harness | `openai_api_harness.py` still contains harness request construction, provider routing, and optional live-call logic. | Defer extraction until native OpenAI live validation or multi-provider harness work creates a concrete need. |
| Agama corpus generation | `build_agama_context.py` still contains CBETA XML-to-Markdown generation logic. | Defer extraction; it is a narrow corpus-generation pipeline with idempotency coverage and high churn risk. |
| Installation smoke | `mock_install_smoke.py` still contains mock install setup and validation logic. | Defer extraction; it is a small operational smoke-test entrypoint. |

## Validation Cleanup Result

The validation cleanup split the old root validator into focused modules:

- `scripts/zilanlib/validation/repository_metadata.py`: required paths, version consistency, and regression matrix inventory.
- `scripts/zilanlib/validation/platform.py`: platform metadata, platform-validation table checks, and Codex YAML status guard.
- `scripts/zilanlib/validation/public_docs.py`: README links, third-party notices, Skill script inventory, public style boundaries, and portable upgrade docs.
- `scripts/zilanlib/validation/runtime_evidence.py`: runtime validation log, evidence index references, and batch manifest safety.
- `scripts/zilanlib/validation/regression_cases.py`: `tests/regression_cases.yaml` schema checks.
- `scripts/zilanlib/validation/reasoning_cases.py`: `tests/reasoning_cases.yaml` schema and reasoning contract checks.
- `scripts/zilanlib/validation/retrieval_chunks.py`: semantic retrieval chunk fixture validation.
- `scripts/zilanlib/validation/agent_prompts.py`: agent prompt contract checks.
- `scripts/zilanlib/validation/agama_corpus.py`: Agama search and generated corpus checks.
- `scripts/zilanlib/validation/suite.py`: validation suite orchestration.

`scripts/validate_zilan_repo.py` now has a narrow role:

- parse CLI arguments
- expose compatibility aliases for tests and older imports
- delegate `run_checks` to `zilanlib.validation.suite`

`tests/test_validate_zilan_repo.py` guards this boundary with a compatibility alias manifest and a CLI-only structure check.

## Decision

The P1 validation cleanup should stop here.

Reason:

- The repeated invariant logic now lives under focused `scripts/zilanlib/validation/` modules.
- `validate_zilan_repo.py` remains the stable command used by local development and CI.
- The compatibility alias manifest makes future helper moves explicit and testable.
- Further splitting the root entrypoint would mostly increase indirection because it no longer owns validation behavior.

## Recommended Next Work

Highest-ROI next step:

1. Shift from validation-file movement to validation quality.
2. Add targeted tests for the lower-coverage, higher-risk validation modules before changing behavior.
3. Prioritize `reasoning_cases.py` and `retrieval_chunks.py` because they guard contract fixtures and semantic retrieval evidence.

Useful follow-ups:

- Add order-focused tests for `scripts/zilanlib/validation/suite.py` if orchestration changes again.
- Add focused negative-schema tests for `reasoning_cases.py` around malformed contracts and expected-output shape.
- Add focused retrieval fixture tests for missing source references, answer sample status handling, and hash/provenance drift.
- Revisit provider-harness extraction only when live native OpenAI or multi-provider work creates a concrete need.

## What Not To Do Yet

- Do not continue splitting `validate_zilan_repo.py` unless a specific compatibility or CLI issue appears.
- Do not change `docs/platform-validation.md` tested statuses as part of cleanup-only work.
- Do not add provider calls, runtime evidence claims, or platform promotions to validation cleanup PRs.
- Do not add a broad application framework, service layer, or plugin architecture for these scripts.
- Do not move stable root CLI names without a compatibility shim.
- Do not split `build_agama_context.py` unless the corpus-generation workflow itself changes.

## Rollback

This closeout is documentation plus changelog text. Rollback is limited to restoring the previous review wording and changelog entry. The code-level validation cleanup is protected separately by tests and can be reverted PR-by-PR if a compatibility issue appears.
