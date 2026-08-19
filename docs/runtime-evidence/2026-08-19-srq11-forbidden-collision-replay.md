# 2026-08-19 SRQ-11 Forbidden-Collision Replay

## Scope

This note records a local replay over the already committed 2026-08-19 Claude Code direct `SRQ-11` answer excerpt
after a narrow fixture-only forbidden-term calibration.

No provider call, live runtime rerun, prompt change, route change, platform validation update, fuzzy matching, regex
matching, semantic-similarity scoring, or `zilan_contract` public API change was performed.

## Calibration

The calibration keeps exact string matching and narrows the `SRQ-11` forbidden surface from the broad fragment
`性相成立` to the explicit wrong-assertion phrase `这个性相成立`.

This removes the shallow collision with the runtime answer heading `性相成立的标准`. The committed runtime answer excerpt
is unchanged.

## Replay Commands

```powershell
python scripts\reasoning_answer_review_batch.py --batch docs\runtime-evidence\2026-08-19-srq11-forbidden-collision-replay-batch.yaml
python scripts\semantic_answer_contract_review.py --query-id SRQ-11 --answer-file docs\runtime-evidence\2026-08-19-claude-code-srq-11-runtime-spot-answer.md --json
```

## Result

```text
# Reasoning Answer Review Batch

Batch: docs/runtime-evidence/2026-08-19-srq11-forbidden-collision-replay-batch.yaml
Overall status: fail
Summary: pass=0, fail=1, review_needed=0, other=0

Boundary: batch fixture review only; this is not runtime platform validation.

## Reviews
- 2026-08-19-srq11-definition-forbidden-collision-replay: fail (SRQ-11)
  missing: collected_topics_definition_scope_error:性相过宽, collected_topics_definition_scope_error:唯在所表上成立, collected_topics_definition_scope_error:违②, collected_topics_definition_scope_error:definiendum_boundary
```

## Findings

- The previous shallow forbidden collision is cleared: `性相成立的标准` is no longer treated as a forbidden wrong
  assertion.
- The answer still fails the current `SRQ-11` answer contract because it does not explicitly preserve
  `性相过宽`, `唯在所表上成立`, `违②`, and the `definiendum_boundary` slot.
- The coverage report can now distinguish this as an explicit local evidence `fail`, not a vague `partial` coverage
  state.

## Boundaries

- This is local answer-contract replay over a committed answer excerpt, not a new runtime run.
- The result is fail evidence, not runtime pass evidence.
- `docs/platform-validation.md` remains unchanged.
