# 2026-07-06 Claude Code SRQ-09 Cognitive Practice Boundary Spot Review

| Field | Value |
|---|---|
| Date | 2026-07-06 |
| Scenario | SRQ-09 cognitive-analysis / vipassana practice-boundary spot review, plus broad ZC-03 work-feedback spot check |
| Route / provider | Claude Code UTF-8 stdin |
| Tool version | Claude Code 2.1.195 |
| System prompt | `agents/zilan-claude-code.md` from `main` at `7bbaa62` |
| Repository base | `7bbaa62` (`Add SRQ-09 cognitive practice boundary fixture (#62)`) |
| Branch | `srq09-runtime-spot-review` |
| Source location | Raw Claude JSON and extracted answer Markdown kept local only under `C:\tmp\zilan-srq09-spot-review-20260706` |
| Redaction note | No secrets are included here. Raw JSON, session identifiers, and full transcripts are not committed. |
| Runtime log entry | `docs/runtime-validation-log.md#2026-07-06-claude-code-srq-09-cognitive-practice-boundary-spot-review` |

## Commands Or Prompts

Command shape:

```powershell
$OutputEncoding = [System.Text.UTF8Encoding]::new($false)
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)
$sys = Get-Content -Raw -Encoding UTF8 agents\zilan-claude-code.md
$prompt | claude -p --output-format json --system-prompt $sys --add-dir .
```

Prompts:

```text
SRQ-09: 收到批评后，我如何区分事实、受、想心所和后续反应？
ZC-03: 孜澜，用摄类学和心类学解释“收到批评后我很受挫”的认知过程。
```

Contract review commands:

```powershell
python scripts\reasoning_contract_runner.py --query-id SRQ-09 --answer-file C:\tmp\zilan-srq09-spot-review-20260706\SRQ-09.answer.md --json
python scripts\reasoning_contract_runner.py --query-id SRQ-09 --answer-file C:\tmp\zilan-srq09-spot-review-20260706\ZC-03.answer.md --json
```

## Output Excerpts

SRQ-09 direct answer excerpt:

```text
耳根 + 声尘 + 耳识 → 触 → 作意 → 受 → 想 → 思 → 后续心所链
...
| ③ 受 | 受心所 | 领纳苦乐舍 | 纯粹的不适感——身体的紧、热、收缩，尚未"知道这是什么" |
| ④ 想 | 想心所 | 取相、安立名言 | "他在批评我""他说我做得不好""这是攻击" |
| ⑤ 思 | 思心所 | 策动心朝向所缘造作 | 策动后续善或不善心所 |
...
[边界] 以上拆解基于心类学框架的文本逻辑分析，非亲证体验。受·想·思的实时区分需要持续的止观训练才能稳定做到；初修阶段能将"后续反应"延迟哪怕几秒已经是很大的进步。观禅实操建议在有经验的善知识指导下进行。
```

ZC-03 broad answer excerpt:

```text
触（批评声音 → 耳根 → 耳识三者和合，建立感知连接）
  ↓
作意（注意力被锁定到这条批评上）
  ↓
受（立即标记为苦受——这里已经启动业力惯性）
  ↓
想（取相安立名言：将"对某件事的不同意见"错误分类为"对我价值的否定"）
...
"被批评 = 我/我的工作没有价值"属于颠倒知...
当前状态：颠倒知（受挫时）→ 犹豫识... → 用正因推理建立比量
...
[边界] 以上分析基于文本逻辑框架，属于物力比量层面的推理。受挫感当下的实时截断需要反复串习才能从比量转化为日常自动调用——这是需要亲证的部分。
```

## Contract Results

| Answer | Reviewed Against | Result | Notes |
|---|---|---:|---|
| `SRQ-09.answer.md` | `SRQ-09` / `cognitive_practice_boundary` | `fail` | The answer covers the five-universal chain and gives a practice boundary, with no forbidden terms. It misses required explicit terms `颠倒知`, `慧`, `无瞋`, `行舍`, `缘摄受`, `三相印证`, and `非心理治疗`, and misses the `cognitive_quality` slot. |
| `ZC-03.answer.md` | `SRQ-09` / `cognitive_practice_boundary` | `fail` | The broader work-feedback answer covers the cognitive-quality slot (`颠倒知`, `犹豫识`, `比量`) and corrective factors (`无瞋`, `行舍`), with no forbidden terms. It misses required explicit terms `慧`, `名色分别`, `缘摄受`, `三相印证`, `非心理治疗`, and `善知识指导`, and misses the `vipassana_mapping` slot. |

## Interpretation

This is a target-gap review, not a platform regression. Both runtime answers are substantively useful: they distinguish `触`, `作意`, `受`, `想`, and `思`, and avoid forbidden therapeutic or attainment claims. The gap is explicitness stability: SRQ-09 requires the answer to surface cognitive-quality, vipassana mapping, corrective mental factors, and non-clinical practice-boundary terms in the same response.

Follow-up work should tighten the SRQ-09 / cognitive-practice boundary prompt contract so direct and broad work-feedback answers explicitly include:

- `颠倒知` / `犹豫识` / `比量` as the cognitive-quality downgrade and repair path
- `念` / `慧` / `无瞋` / `行舍` as corrective mental factors
- `名色分别` / `缘摄受` / `三相印证` as vipassana mapping terms
- `非心理治疗` / `善知识指导` as practice-boundary terms

## Known Limits

- This is a two-prompt target-contract spot review, not a full ZC-01 through ZC-06 platform rerun.
- It does not validate native OpenAI API or any OpenAI-compatible provider route.
- `reasoning_contract_runner.py` and `semantic_answer_contract_review.py` are minimum explicitness checks, not doctrinal judges.
- Raw Claude JSON and full answer files remain local only under `C:\tmp\zilan-srq09-spot-review-20260706`.
- No platform validation status changes follow from this review.