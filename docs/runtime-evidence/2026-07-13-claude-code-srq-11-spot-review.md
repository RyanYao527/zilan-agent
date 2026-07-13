# 2026-07-13 Claude Code SRQ-11 Collected Topics Definition-Scope Spot Review

| Field | Value |
|---|---|
| Date | 2026-07-13 |
| Scenario | SRQ-11 Collected Topics definition-scope spot review for the too-broad defining mark "瓶的性相是能盛水者" |
| Route / provider | Claude Code UTF-8 stdin |
| Tool version | Claude Code 2.1.204 |
| System prompt | `agents/zilan-claude-code.md` from `main` at `4d276f1` |
| Repository base | `4d276f1` (`Add Collected Topics definition-scope fixture (#100)`) |
| Branch | `srq11-runtime-spot-review` |
| Source location | Raw Claude JSON and extracted answer Markdown kept local only under `C:\tmp\zilan-srq11-spot-review-20260713` |
| Redaction note | No secrets are included here. Raw JSON, session identifiers, and full transcripts are not committed. |
| Runtime log entry | `docs/runtime-validation-log.md#2026-07-13-claude-code-srq-11-collected-topics-definition-scope-spot-review` |

## Commands Or Prompts

Command shape:

```powershell
$OutputEncoding = [System.Text.UTF8Encoding]::new($false)
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)
[Console]::InputEncoding = [System.Text.UTF8Encoding]::new($false)
$sys = Get-Content -Raw -Encoding UTF8 -LiteralPath 'agents\zilan-claude-code.md'
$prompt | claude -p --output-format json --system-prompt $sys --add-dir . --dangerously-skip-permissions
```

Prompt:

```text
孜澜，用摄类学检查定义：瓶的性相是能盛水者。这个定义成立吗？
```

Contract review command:

```powershell
python scripts\reasoning_contract_runner.py --query-id SRQ-11 --answer-file C:\tmp\zilan-srq11-spot-review-20260713\SRQ-11.answer.md --json
```

## Output Excerpt

```text
名相：瓶 (bum pa)
所表：瓶 (definiendum)
性相候选：能盛水者 (that which can hold water)

存在大量"能盛水但不是瓶"的反例：

- 碗——能盛水，是碗不是瓶
- 杯——能盛水，是杯不是瓶
- 湖——能盛水，是湖不是瓶
- 桶——能盛水，是桶不是瓶
- 盆——能盛水，是盆不是瓶

根据工具箱的错误类型表：

> **性相过宽** | "能盛水者是瓶之性相"（湖也能盛水）| 违②

此定义属于**性相过宽**（primary error），同时存在**性相过窄**的次生缺陷（不能覆盖破瓶等边缘实例）。
```

## Contract Results

| Answer | Reviewed Against | Result | Notes |
|---|---|---:|---|
| `SRQ-11.answer.md` | `SRQ-11` / `collected_topics_definition_scope_error` | `pass` | Required terms and slots all present, including `摄类学`, `性相`, `所表`, `能盛水者`, `瓶`, `湖`, `性相过宽`, `唯在所表上成立`, `违②`, `错误类型`, and `不成立`; no forbidden terms present. |

## Known Limits

- This is a target-contract spot review, not a full ZC-01 through ZC-06 platform rerun.
- It does not validate native OpenAI API or any OpenAI-compatible provider route.
- The answer-contract helper is a minimum explicitness check rather than a doctrinal judge.
- Raw Claude JSON and the full answer file remain local only under `C:\tmp\zilan-srq11-spot-review-20260713`.
- This evidence does not change platform validation status.
