# 2026-07-06 Claude Code SRQ-09 Boundary Fix Spot Review

| Field | Value |
|---|---|
| Date | 2026-07-06 |
| Scenario | SRQ-09 cognitive-analysis / vipassana practice-boundary prompt-contract fix, plus broad ZC-03 work-feedback spot check |
| Route / provider | Claude Code UTF-8 stdin |
| Tool version | Claude Code 2.1.195 |
| System prompt | `agents/zilan-claude-code.md` from this PR branch |
| Repository base | `01c998e` (`Record SRQ-09 runtime spot review (#63)`) plus this PR's prompt-contract changes |
| Branch | `srq09-cognitive-practice-boundary-prompt` |
| Source location | Raw Claude JSON and extracted answer Markdown kept local only under `C:\tmp\zilan-srq09-boundary-fix-20260706` |
| Redaction note | No secrets are included here. Raw JSON, session identifiers, and full transcripts are not committed. |
| Runtime log entry | `docs/runtime-validation-log.md#2026-07-06-claude-code-srq-09-boundary-fix-spot-review` |

## Commands Or Prompts

Command shape:

```powershell
$OutputEncoding = [System.Text.UTF8Encoding]::new($false)
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)
$sys = Get-Content -Raw -Encoding UTF8 agents\zilan-claude-code.md
$prompt | claude -p --dangerously-skip-permissions --output-format json --system-prompt $sys --add-dir .
```

The broad `ZC-03` rerun also appended a noninteractive validation instruction to avoid pausing for file-read approval and to complete the prompt directly.

Prompts:

```text
SRQ-09: 收到批评后，我如何区分事实、受、想心所和后续反应？
ZC-03: 孜澜，用摄类学和心类学解释“收到批评后我很受挫”的认知过程。
```

Contract review commands:

```powershell
python scripts\reasoning_contract_runner.py --query-id SRQ-09 --answer-file C:\tmp\zilan-srq09-boundary-fix-20260706\SRQ-09.final.answer.md --json
python scripts\reasoning_contract_runner.py --query-id SRQ-09 --answer-file C:\tmp\zilan-srq09-boundary-fix-20260706\ZC-03.final.answer.md --json
```

## Output Excerpts

SRQ-09 direct answer excerpt:

```text
触 → 作意 → 受 → 想 → 思
...
| 想（"这是否定"） | 颠倒知 | 将局部别法的事误解为整体总法的否定 |
...
| 念 | 在反应生起的刹那记得"五遍行链路" |
| 慧 | 以摄类学总别分析简择：三处数据修正（别法）≠ 整体否定（总法） |
| 无瞋 | 将对方从"伤害者"还原为"提出修正意见的人" |
| 行舍 | 心平等住于事实 |
...
名色分别 ... 缘摄受 ... 三相印证 ... 非心理治疗 ... 善知识指导
```

ZC-03 broad answer excerpt:

```text
触 → 作意 → 受 → 想 → 思
...
此时认知已从颠倒知降级为犹豫识... 进一步引入比量...
...
| 念 | 觉察到受挫感生起时，立即忆念"这只是别法反馈，不是总法否定" |
| 慧 | 以摄类学总别框架简择 |
| 无瞋 | 不将批评视为攻击 |
| 行舍 | 心平等安住 |
...
名色分别 ... 缘摄受 ... 三相印证 ... 非心理治疗 ... 善知识指导
```

## Contract Results

| Answer | Reviewed Against | Result | Notes |
|---|---|---:|---|
| `SRQ-09.final.answer.md` | `SRQ-09` / `cognitive_practice_boundary` | `pass` | Required terms and slots all present, including `触`, `作意`, `受`, `想`, `思`, `颠倒知`, `念`, `慧`, `无瞋`, `行舍`, `名色分别`, `缘摄受`, `三相印证`, `非心理治疗`, and `善知识指导`; no forbidden terms present. |
| `ZC-03.final.answer.md` | `SRQ-09` / `cognitive_practice_boundary` | `pass` | Broad work-feedback answer also preserves the cognitive-quality, corrective-factor, vipassana-mapping, and practice-boundary slots; no forbidden terms present. |

## Interpretation

The previous SRQ-09 runtime spot review found a target explicitness gap. This fix tightens the Skill, Claude Code, Codex, and OpenAI metadata prompts so cognitive-analysis / vipassana practice answers explicitly preserve the corrective-factor terms and the non-therapeutic practice boundary.

## Known Limits

- This is a two-prompt target-contract spot review, not a full ZC-01 through ZC-06 platform rerun.
- It does not validate native OpenAI API or any OpenAI-compatible provider route.
- `reasoning_contract_runner.py` and `semantic_answer_contract_review.py` are minimum explicitness checks, not doctrinal judges.
- `--dangerously-skip-permissions` was used only to prevent noninteractive Claude Code validation from stopping at local file-read approval prompts.
- Raw Claude JSON and full answer files remain local only under `C:\tmp\zilan-srq09-boundary-fix-20260706`.
- No platform validation status changes follow from this review.