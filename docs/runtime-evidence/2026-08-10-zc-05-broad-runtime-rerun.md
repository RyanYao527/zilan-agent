# 2026-08-10 ZC-05 Broad Runtime Rerun

## Scope

This note records a targeted Claude Code runtime rerun for broad `ZC-05` after the CBETA anchor / candidate-map evidence
PR was merged. It captures one new standalone answer excerpt and replays it against the integrated `SRQ-01`, `SRQ-03`,
`SRQ-04`, and `SRQ-08` answer contracts.

This is not a full `ZC-01` through `ZC-06` platform rerun. It does not change `docs/platform-validation.md`, does not
validate native OpenAI API, and does not validate any OpenAI-compatible provider route.

## Runtime Command Shape

```powershell
$OutputEncoding = [System.Text.UTF8Encoding]::new($false)
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)
[Console]::InputEncoding = [System.Text.UTF8Encoding]::new($false)
$sys = Get-Content -Raw -Encoding UTF8 -LiteralPath 'agents\zilan-claude-code.md'
$prompt = '请 spawn 一个 zilan agent，用应成论式分析诸法无我，并串联阿含、摄类学、因明和观禅。'
$prompt | claude -p --output-format json --system-prompt $sys --add-dir . --dangerously-skip-permissions
```

Raw Claude JSON and the extracted local answer file are kept local only under
`C:\tmp\zilan-zc05-runtime-rerun-20260810`. The committed standalone excerpt is
`docs/runtime-evidence/2026-08-10-claude-code-zc-05-broad-runtime-rerun-answer.md`.

## Runtime Result

| Field | Value |
|---|---|
| Runtime | Claude Code UTF-8 stdin |
| Tool version | Claude Code 2.1.220 |
| System prompt | `agents/zilan-claude-code.md` from `main` after #189 |
| Branch | `codex/broad-zc05-runtime-rerun` |
| Claude subtype | `success` |
| Turns | 1 |
| Provider/model note | Claude Code local configuration reported `deepseek-v4-pro[1m]`; this is Claude Code route evidence, not native provider validation. |
| Redaction note | No secrets are included here. Raw JSON, session metadata, token/cost details, and full unredacted local paths are not committed. |

## Replay Commands

```powershell
python scripts\reasoning_answer_review_batch.py --batch docs\runtime-evidence\2026-08-10-zc-05-broad-runtime-rerun-batch.yaml
python scripts\semantic_answer_contract_review.py --query-id SRQ-01 --answer-file docs\runtime-evidence\2026-08-10-claude-code-zc-05-broad-runtime-rerun-answer.md
python scripts\semantic_answer_contract_review.py --query-id SRQ-03 --answer-file docs\runtime-evidence\2026-08-10-claude-code-zc-05-broad-runtime-rerun-answer.md
python scripts\semantic_answer_contract_review.py --query-id SRQ-04 --answer-file docs\runtime-evidence\2026-08-10-claude-code-zc-05-broad-runtime-rerun-answer.md
python scripts\semantic_answer_contract_review.py --query-id SRQ-08 --answer-file docs\runtime-evidence\2026-08-10-claude-code-zc-05-broad-runtime-rerun-answer.md
```

## Contract Results

```text
# Reasoning Answer Review Batch

Batch: docs/runtime-evidence/2026-08-10-zc-05-broad-runtime-rerun-batch.yaml
Overall status: pass
Summary: pass=4, fail=0, review_needed=0, other=0

Boundary: batch fixture review only; this is not runtime platform validation.

## Reviews
- 2026-08-10-zc-05-broad-rerun-srq-01-integrated: pass (SRQ-01)
- 2026-08-10-zc-05-broad-rerun-srq-03-prasanga: pass (SRQ-03)
- 2026-08-10-zc-05-broad-rerun-srq-04-agama: pass (SRQ-04)
- 2026-08-10-zc-05-broad-rerun-srq-08-nihilism: pass (SRQ-08)
```

## Findings

- The new broad `ZC-05` answer preserves the integrated `SRQ-01` surfaces: `阿含证据`, `代表性检索`, `因明校验`, `我所`,
  `触`, `作意`, `受`, `想`, `思`, and `不等于修证`.
- The same answer now preserves the strict `SRQ-03` / `SRQ-08` slots that were missing in the 2026-08-06 spot review:
  `不立自宗`, `二谛`, and `proposition_decomposition`.
- `SRQ-04` remains passing and includes `CBETA`, `T02n0099`, `context/agama/` anchors, representative-search language,
  and `待校勘`.
- Because `SRQ-03` and `SRQ-08` both pass, no follow-up prompt-hardening PR is needed for this runtime result.

## Boundary

This is targeted runtime evidence for one broad `ZC-05` Claude Code invocation. It does not prove all future broad
answers will pass, does not grade doctrinal correctness, does not prove publication-level Agama collation, and does not
change platform validation status.
