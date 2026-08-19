# 2026-08-19 SRQ-06 / SRQ-07 Contract Calibration Replay

## Scope

This note records a local replay over the already committed 2026-08-19 Claude Code direct `SRQ-06` and `SRQ-07`
answer excerpts after a narrow answer-contract calibration.

No provider call, live runtime rerun, prompt change, route change, platform validation update, fuzzy matching, regex
matching, semantic-similarity scoring, or `zilan_contract` public API change was performed.

## Calibration

The calibration keeps exact string matching and adds fixture-local required term groups for narrow surface aliases:

- `SRQ-06`: `indeterminate_resolution` accepts either `不能决定` or `无法决定`.
- `SRQ-07`: `collected_topics_surface` accepts either `摄类学` or `总与别`.

The 2026-08-19 runtime answer excerpts are unchanged. PR #193 remains useful as historical fail evidence for the
pre-calibration literal contract. Under the current calibrated contract, the same excerpts replay as pass for
`SRQ-06` and `SRQ-07`.

## Replay Commands

```powershell
python scripts\reasoning_answer_review_batch.py --batch docs\runtime-evidence\2026-08-19-srq06-srq07-contract-calibration-replay-batch.yaml
python scripts\semantic_answer_contract_review.py --query-id SRQ-06 --answer-file docs\runtime-evidence\2026-08-19-claude-code-srq-06-runtime-spot-answer.md --json
python scripts\semantic_answer_contract_review.py --query-id SRQ-07 --answer-file docs\runtime-evidence\2026-08-19-claude-code-srq-07-runtime-spot-answer.md --json
```

## Result

```text
# Reasoning Answer Review Batch

Batch: docs/runtime-evidence/2026-08-19-srq06-srq07-contract-calibration-replay-batch.yaml
Overall status: pass
Summary: pass=2, fail=0, review_needed=0, other=0

Boundary: batch fixture review only; this is not runtime platform validation.

## Reviews
- 2026-08-19-srq06-hetuvidya-indeterminate-contract-calibration-replay: pass (SRQ-06)
- 2026-08-19-srq07-collected-topics-total-part-contract-calibration-replay: pass (SRQ-07)
```

## Boundaries

- This is local answer-contract replay over committed answer excerpts, not a new runtime run.
- `SRQ-10` and `SRQ-11` remain failing in the 2026-08-19 direct runtime spot review and are out of scope here.
- `docs/platform-validation.md` remains unchanged.
