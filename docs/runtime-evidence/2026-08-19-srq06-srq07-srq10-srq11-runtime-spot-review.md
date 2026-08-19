# 2026-08-19 SRQ-06 / SRQ-07 / SRQ-10 / SRQ-11 Runtime Spot Review

## Scope

This note records four targeted Claude Code runtime spot answers for SRQ cases that the coverage report previously
flagged as `not_reviewed` or `manual_review_required`.

This is not a full `ZC-01` through `ZC-06` platform rerun. It does not change `docs/platform-validation.md`, does not
validate native OpenAI API, and does not validate any OpenAI-compatible provider route.

## Post-Calibration Note

PR #193 captured the original strict-literal answer-contract result for all four runtime answer excerpts. Later
fixture-local calibrations added exact required-term groups for `SRQ-06`, `SRQ-07`, and `SRQ-10` without changing the
answer text or calling a provider again:

- `SRQ-06`: `不能决定` / `无法决定`
- `SRQ-07`: `摄类学` / `总与别`
- `SRQ-10`: cognitive-analysis aliases for attribution-error, motive-inference, affliction, and non-harm surfaces

Under the current calibrated contract, this same batch now reports `pass=3`, `fail=1`: `SRQ-06`, `SRQ-07`, and
`SRQ-10` pass, while `SRQ-11` still fails. See
`docs/runtime-evidence/2026-08-19-srq06-srq07-contract-calibration-replay.md` and
`docs/runtime-evidence/2026-08-19-srq10-contract-calibration-replay.md` for focused replay notes.

## Runtime Command Shape

Each prompt used Windows PowerShell UTF-8 output and the repository `agents/zilan-claude-code.md` prompt:

```powershell
$OutputEncoding = [System.Text.UTF8Encoding]::new($false)
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)
$system = Get-Content -Raw agents\zilan-claude-code.md
claude -p --append-system-prompt $system --permission-mode dontAsk --max-budget-usd 1 --output-format text <prompt>
```

Prompt set:

- `SRQ-06`: `检验论式：声，应是常，以是所知故。请直接回答，不要写入文件。`
- `SRQ-07`: `用摄类学检验命题：这份报告有三处问题，所以我这个人没有价值。请直接回答，不要写入文件。`
- `SRQ-10`: `家庭照护压力下，我觉得对方在故意为难我，如何用心类学和观禅拆解？请直接回答，不要写入文件。`
- `SRQ-11`: `用摄类学检查定义：瓶的性相是能盛水者。这个定义成立吗？请直接回答，不要写入文件。`

Claude Code printed `[claude-code:unrecognized_model] {"model":"deepseek-v4-pro[1m]","query_source":"sdk"}` before each
answer under the local user configuration, then returned answer text. This is Claude Code route evidence only; it is
not native DeepSeek, native OpenAI API, or OpenAI-compatible provider validation.

## Runtime Result

| Field | Value |
|---|---|
| Runtime | Claude Code CLI |
| Tool version | Claude Code `2.1.234` |
| System prompt | `agents/zilan-claude-code.md` from `main` after #192 |
| Repository base | `8037b95` (`Add SRQ evidence coverage and productization triage`) |
| Branch | `codex/srq-evidence-closeout` |
| Transcript status | Standalone answer excerpts committed under `docs/runtime-evidence/`; raw CLI session metadata is not committed. |
| Repository checks | PR #193 recorded a pre-calibration strict-literal fail for all four cases. Current calibrated replay of the same batch reports `pass=3`, `fail=1`. |
| Overall result | `target-partial`: current calibrated contracts pass for `SRQ-06` / `SRQ-07` / `SRQ-10`; `SRQ-11` still needs prompt or contract follow-up before pass evidence can be recorded. |

No second retry was used after the deterministic contract failures. Keeping the first observed answers avoids
retry-until-pass evidence and makes the missing slots visible.

## Replay Commands

```powershell
python scripts\reasoning_answer_review_batch.py --batch docs\runtime-evidence\2026-08-19-srq06-srq07-srq10-srq11-runtime-spot-review-batch.yaml
python scripts\semantic_answer_contract_review.py --query-id SRQ-06 --answer-file docs\runtime-evidence\2026-08-19-claude-code-srq-06-runtime-spot-answer.md --json
python scripts\semantic_answer_contract_review.py --query-id SRQ-07 --answer-file docs\runtime-evidence\2026-08-19-claude-code-srq-07-runtime-spot-answer.md --json
python scripts\semantic_answer_contract_review.py --query-id SRQ-10 --answer-file docs\runtime-evidence\2026-08-19-claude-code-srq-10-runtime-spot-answer.md --json
python scripts\semantic_answer_contract_review.py --query-id SRQ-11 --answer-file docs\runtime-evidence\2026-08-19-claude-code-srq-11-runtime-spot-answer.md --json
```

## Contract Results

Historical PR #193 pre-calibration result:

```text
# Reasoning Answer Review Batch

Batch: docs/runtime-evidence/2026-08-19-srq06-srq07-srq10-srq11-runtime-spot-review-batch.yaml
Overall status: fail
Summary: pass=0, fail=4, review_needed=0, other=0

Boundary: batch fixture review only; this is not runtime platform validation.

## Reviews
- 2026-08-19-srq06-hetuvidya-indeterminate-runtime-spot: fail (SRQ-06)
  missing: hetuvidya_indeterminate_detection:不能决定
- 2026-08-19-srq07-collected-topics-total-part-runtime-spot: fail (SRQ-07)
  missing: collected_topics_total_part_error:摄类学
- 2026-08-19-srq10-cognitive-caregiving-runtime-spot: fail (SRQ-10)
  missing: cognitive_caregiving_boundary:错误归因, cognitive_caregiving_boundary:动机推断, cognitive_caregiving_boundary:忿, cognitive_caregiving_boundary:恼, cognitive_caregiving_boundary:不害
- 2026-08-19-srq11-collected-topics-definition-runtime-spot: fail (SRQ-11)
  missing: collected_topics_definition_scope_error:性相过宽, collected_topics_definition_scope_error:唯在所表上成立, collected_topics_definition_scope_error:违②, collected_topics_definition_scope_error:definiendum_boundary
```

## Findings

- `SRQ-06` answered the broad Hetuvidya shape and named `不定因`, but missed the required literal `不能决定`.
- `SRQ-07` preserved the total/part and pervasion boundary but missed the literal `摄类学`.
- Current calibrated replay treats the `SRQ-06` answer's `无法决定` and the `SRQ-07` answer's `总与别` as exact
  acceptable surfaces for those two narrow slots.
- Current calibrated replay treats the `SRQ-10` answer's `错误地投射`, `他人心相续里的动机`, `间接推断`, `厌烦`,
  `反向攻击`, and `不把对方固化成一个"敌人"标签` as exact acceptable surfaces for the cognitive-analysis slots.
- `SRQ-11` identified the definition as too broad in ordinary wording, but missed required literal boundary terms
  (`性相过宽`, `唯在所表上成立`, `违②`) and included the shallow forbidden phrase `性相成立` in a heading.

## Boundary

These results close the earlier manifest-side `not_reviewed` / `manual_review_required` ambiguity by recording
contract-reviewable runtime answer excerpts. The current calibrated replay is pass evidence for `SRQ-06` / `SRQ-07` /
`SRQ-10` answer surfaces only; it is not a new runtime run and not platform validation evidence. `SRQ-11` remains fail
evidence. None of these entries downgrade or upgrade platform status, and they do not prove doctrinal quality.
