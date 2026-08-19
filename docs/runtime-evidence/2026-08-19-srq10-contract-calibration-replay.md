# 2026-08-19 SRQ-10 Contract Calibration Replay

## Scope

This note records a local replay over the already committed 2026-08-19 Claude Code direct `SRQ-10` answer excerpt
after a narrow fixture-only answer-contract calibration.

No provider call, live runtime rerun, prompt change, route change, platform validation update, fuzzy matching, regex
matching, semantic-similarity scoring, or `zilan_contract` public API change was performed.

## Calibration

The calibration keeps exact string matching and adds fixture-local required term groups for narrow cognitive-analysis
surface aliases:

- `attribution_error_surface`: accepts `错误归因` or `错误地投射`.
- `motive_inference_surface`: accepts `动机推断`, `他人心相续里的动机`, or `间接推断`.
- `affliction_surface`: accepts `忿`, `恼`, `厌烦`, or `反向攻击`.
- `non_harm_surface`: accepts `不害` or `不把对方固化成一个"敌人"标签`.

The 2026-08-19 runtime answer excerpt is unchanged. PR #193 remains useful as historical fail evidence for the
pre-calibration literal contract. Under the current calibrated contract, the same excerpt replays as pass for
`SRQ-10`.

## Replay Commands

```powershell
python scripts\reasoning_answer_review_batch.py --batch docs\runtime-evidence\2026-08-19-srq10-contract-calibration-replay-batch.yaml
python scripts\semantic_answer_contract_review.py --query-id SRQ-10 --answer-file docs\runtime-evidence\2026-08-19-claude-code-srq-10-runtime-spot-answer.md --json
```

## Result

```text
# Reasoning Answer Review Batch

Batch: docs/runtime-evidence/2026-08-19-srq10-contract-calibration-replay-batch.yaml
Overall status: pass
Summary: pass=1, fail=0, review_needed=0, other=0

Boundary: batch fixture review only; this is not runtime platform validation.

## Reviews
- 2026-08-19-srq10-cognitive-caregiving-contract-calibration-replay: pass (SRQ-10)
```

## Boundaries

- This is local answer-contract replay over a committed answer excerpt, not a new runtime run.
- `SRQ-11` remains failing in the 2026-08-19 direct runtime spot review and is intentionally out of scope here.
- `docs/platform-validation.md` remains unchanged.
