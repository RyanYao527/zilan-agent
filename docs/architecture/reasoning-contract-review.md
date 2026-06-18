# Reasoning Contract Review

> Last updated: 2026-06-17  
> Status: retrospective mapping, not a new runtime validation pass.

This note maps the existing ZC regression family to the new `ZR-*` reasoning-contract fixtures in `tests/reasoning_cases.yaml`. It is an architecture review surface, not platform validation evidence. Platform status remains governed by `docs/platform-validation.md`.

## Scope

Inputs reviewed:

- `tests/regression_cases.yaml`
- `tests/reasoning_cases.yaml`
- `CODEX_REGRESSION_TESTS.md`
- `docs/runtime-validation-log.md`
- `docs/runtime-evidence/2026-06-16-volcengine-openai-compatible-zc-02-live.md`
- `docs/runtime-evidence/2026-06-16-volcengine-openai-compatible-zc-01-zc-03-live.md`

No new Codex, Claude Code, native OpenAI API, or OpenAI-compatible live run was executed for this review.

## Mapping Matrix

| ZC case | Related ZR cases | Review status | Notes |
|---|---|---|---|
| ZC-02 | ZR-01, ZR-03 | Strong coverage for ZR-01; fixture-only coverage for ZR-03 | Existing summaries show the expected `因三相` explanation, the `声，应是无常，以所作性故` example, and local context citations. ZR-03 is an edge-case fixture for `因不成`; it still needs a targeted runtime prompt. |
| ZC-03 | ZR-02 | Strong summary-level coverage | Existing Volcengine-compatible evidence records the hidden inference `被批评 -> 我无价值` as `不周遍` and the chain `触 -> 作意 -> 受 -> 想 -> 思`. This matches the v0 collected-topics and cognitive-analysis contract. |
| ZC-05 | ZR-04, ZR-05, ZR-06 | Partial retrospective coverage | Existing Codex/Claude summaries report cross-domain use of Agama, Collected Topics, Hetuvidya, Madhyamaka, and vipassana with citations and boundaries. The summaries predate the `ZR-*` contract, so they do not prove every structured field in ZR-04/ZR-05/ZR-06 was explicitly satisfied. |

## Immediate Decision

Do not change agent prompt wording in this PR.

Reason:

- ZC-02 and ZC-03 already show the target structures in recent evidence.
- ZC-05 is broad enough that a prompt wording change would require a fresh runtime rerun across Codex and Claude Code.
- Reasoning Contract v0 should first stabilize as schema and review surface before becoming an output-format requirement.

## Post-Merge Runtime Review

Follow-up: `docs/architecture/post-contract-runtime-review.md` records a 2026-06-18 review of existing ZC-02, ZC-03, and ZC-05 evidence summaries against `SRQ-02` through `SRQ-04`. The review found that committed summaries are not transcript-rich enough to prove the newer answer contracts; it does not downgrade any platform status.

After this PR lands, the next runtime review should check:

1. ZC-02 against ZR-01:
   - has explicit 有法 / 所立法 / 因 or a clear equivalent
   - names all three 因三相
   - marks `所作性` as a positive reason for `声无常`
2. A new targeted prompt against ZR-03:
   - asks the model to inspect `声，应是可见，以是色形故`
   - expects `因不成` or an equivalent first-characteristic failure
3. ZC-03 against ZR-02:
   - rejects `被批评 -> 我无价值` as `不周遍`
   - includes the `触 -> 作意 -> 受 -> 想 -> 思` chain
   - states a practice or clinical boundary
4. ZC-05 against ZR-04/ZR-05/ZR-06:
   - separates Agama evidence, prasaṅga reasoning, Hetuvidya checks, Collected Topics relations, practice application, and boundary statements
   - cites local Agama passages with CBETA IDs and local file references when scripture is used
   - marks any publication-level collation as pending CBETA XML or parallel-text verification

## Boundary

This review confirms that the reasoning contract is aligned with existing regression intent. It does not upgrade any platform route, does not prove doctrinal correctness, and does not replace future transcript-backed runtime validation.
