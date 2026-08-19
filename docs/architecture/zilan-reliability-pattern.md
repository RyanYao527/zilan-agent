# Zilan Reliability Pattern

> Date: 2026-08-19
> Scope: developer-facing methodology only. This note does not change provider routes, runtime validation status,
> prompt contracts, or the public `zilan_contract` API.

The Zilan reliability pattern is a small, reusable way to keep LLM output quality work inspectable without turning
every review into a live provider run. It separates three questions that often get mixed together:

1. What explicit output surfaces must be preserved?
2. What evidence exists for a specific prompt, fixture, answer excerpt, or manual review?
3. Which gaps should be fixed next?

The pattern is intentionally deterministic. It can flag missing terms, forbidden claims, boundary slots, fixture
coverage, and evidence status. It cannot decide doctrinal correctness, medical correctness, legal correctness, or
overall semantic quality.

## Pattern Layers

| Layer | Repository surface | Responsibility |
| --- | --- | --- |
| Output contract | `zilan_contract` | Checks required terms, forbidden phrases, and boundary slots with deterministic rules. It is not an LLM judge or semantic grader. |
| Evidence manifest | `docs/runtime-evidence/evidence_manifest.yaml` | Records machine-readable evidence entries, evidence class, related cases, answer-file safety, platform-status boundaries, and review statuses. |
| Coverage report | `scripts/srq_coverage_report.py` | Builds local Markdown or JSON triage from SRQ fixtures, ZR reasoning links, answer samples, and manifest evidence. |
| Human evidence | `docs/runtime-evidence/index.md` and dated notes | Preserves reviewer-readable runtime excerpts, batch reviews, summary notes, and manual collation context. |
| Platform validation | `agents/openai.yaml` and `docs/platform-validation.md` | Records platform tested status only when dated runtime evidence meets the platform-validation policy. |

## Evidence Boundaries

The pattern works because evidence classes are not interchangeable:

| Evidence type | What it can support | What it cannot support |
| --- | --- | --- |
| Fixture pass | Local contract and validator behavior over checked-in samples | Runtime quality or provider status |
| Local replay | Current contract behavior over a committed answer excerpt | A new runtime pass |
| Standalone answer excerpt | Review of one captured answer | General platform status unless policy requirements are also met |
| Batch manifest/report | Reproducible grouped local review | New generated output |
| Manual collation | Human-reviewed source-boundary or parallel-text evidence | Automated citation correctness or publication-ready collation |
| Provider smoke | Narrow provider behavior evidence | Broad tested status unless the validation record is complete |

When evidence is incomplete, the conservative states are part of the product: `runtime_pending`, `not_reviewed`,
`manual_review_required`, and `fail` are more useful than silently treating unclear work as passed.

## Applying The Pattern

Use this sequence before changing a prompt, route, contract, or evidence claim:

1. Run `python scripts\srq_coverage_report.py --json` to identify the current weakest SRQ/ZR surfaces.
2. Inspect the relevant fixture in `tests/fixtures/retrieval_chunks/semantic_chunks.yaml`.
3. Check whether the gap is a contract collision, a missing prompt slot, a weak retrieval fixture, or missing evidence.
4. Make the narrowest change that addresses only that class of gap.
5. Record the evidence using the correct class in `docs/runtime-evidence/evidence_manifest.yaml`.
6. Keep local replay, fixture pass, manual collation, provider smoke, and runtime pass separate in the written record.
7. Do not update platform status unless `docs/platform-validation.md` evidence standards are fully met.

For package users, the reusable part is `zilan_contract`: define an output contract, run it against generated text,
and treat failures as deterministic review signals. The Zilan repository adds the evidence manifest and coverage report
around that package so maintainers can decide what to improve next.

## Portable Domains

The same shape works in domains where an answer must preserve explicit safety or compliance surfaces:

- medical disclaimers that must include escalation and non-diagnosis boundaries;
- legal summaries that must include jurisdiction and non-advice boundaries;
- financial analysis that must include risk and non-personalized-advice boundaries;
- compliance workflows that must include audit scope, exception handling, and evidence limits.

The point is not to replace domain experts. The point is to make omissions visible before an expert spends time on
the answer.

## Non-Goals

- No provider calls or live runtime execution.
- No vector database, embedding retrieval, FastAPI service, UI layer, or LLM judge.
- No regex, fuzzy matching, Unicode normalization, semantic similarity, or schema v2 behavior.
- No platform status promotion from fixture pass, local replay, manifest entries, or manual collation.
- No changes to `scripts/search_agama.py`, which remains the stable Agama Markdown search baseline.

## Rollback

This document is descriptive. If the reliability-pattern framing becomes misleading, rollback is limited to removing
this note and its README, roadmap, and changelog references. Existing validators, evidence files, platform metadata,
and `zilan_contract` APIs remain unaffected.
