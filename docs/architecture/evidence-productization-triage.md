# Evidence Productization Triage

> Date: 2026-08-18

This note records a developer-facing productization triage pass. It adds local evidence visibility and release
guardrails without changing provider routes, prompt contracts, runtime validation status, or public `zilan_contract`
APIs.

## What Changed

- `docs/runtime-evidence/evidence_manifest.yaml` is the machine-readable v1 index for high-value SRQ/ZC/ZR evidence.
- `scripts/srq_coverage_report.py` produces a local Markdown or JSON SRQ/ZR evidence coverage report.
- `scripts/zilanlib/validation/runtime_evidence.py` validates manifest shape, file references, evidence classes,
  answer-file safety, review statuses, and `platform_status_change: false`.
- `docs/zilan-contract-release-checklist.md` documents deterministic package-surface release checks.

## Boundaries

- No provider calls, live runtime calls, vector DB, FastAPI, UI, or LLM judge.
- No changes to `docs/platform-validation.md`, `agents/openai.yaml`, or agent prompts.
- Local replay, fixture pass, manifest status, and manual collation notes are not platform validation evidence.
- `scripts/search_agama.py` remains the stable Agama search baseline.

## Rollback

Rollback is narrow: remove the SRQ coverage CLI and module, remove `evidence_manifest.yaml`, revert manifest validation,
revert the added tests, and remove the related docs/changelog entries. Existing Markdown runtime evidence navigation,
provider route metadata, platform validation status, and `zilan_contract` public APIs remain intact.
