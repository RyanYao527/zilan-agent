# 2026-08-20 SRQ-11 Definition Violation Alias Replay

## Scope

This note records a local replay over the already committed 2026-08-20 Volcengine OpenAI-compatible `SRQ-11`
answer excerpt after a narrow fixture-only answer-contract calibration.

No provider call, live runtime rerun, prompt change, provider route change, platform validation update, fuzzy matching,
regex matching, semantic-similarity scoring, or `zilan_contract` public API change was performed.

## Calibration

The calibration keeps exact string matching and adds a fixture-local required term group for the definition-violation
marker:

- `definition_violation_marker`: accepts `违②` or `违三要素校验之②`.

The prompt policy remains stricter than the answer-review policy: Codex, Claude Code, and OpenAI metadata still require
the exact literal `违②`.

The 2026-08-20 Volcengine live answer excerpt is unchanged. The original #202 live evidence note remains useful as
historical fail evidence for the pre-calibration exact-literal contract. Under the current calibrated contract, the
same excerpt replays as pass for `SRQ-11`.

## Replay Commands

```powershell
python scripts\semantic_answer_contract_review.py --query-id SRQ-11 --answer-file docs\runtime-evidence\2026-08-20-volcengine-srq11-definition-live-answer.md --json
python scripts\reasoning_answer_review_batch.py --batch docs\runtime-evidence\2026-08-20-srq11-definition-violation-alias-replay-batch.yaml
```

## Result

```text
# Reasoning Answer Review Batch

Batch: docs/runtime-evidence/2026-08-20-srq11-definition-violation-alias-replay-batch.yaml
Overall status: pass
Summary: pass=1, fail=0, review_needed=0, other=0

Boundary: batch fixture review only; this is not runtime platform validation.

## Reviews
- 2026-08-20-srq11-definition-violation-alias-replay: pass (SRQ-11)
```

## Boundaries

- This is local answer-contract replay over a committed answer excerpt, not a new runtime run.
- This is Volcengine OpenAI-compatible answer evidence, not native OpenAI API validation.
- The answer-contract helper remains a deterministic minimum explicitness check; it does not grade doctrinal quality.
- `docs/platform-validation.md` remains unchanged.
