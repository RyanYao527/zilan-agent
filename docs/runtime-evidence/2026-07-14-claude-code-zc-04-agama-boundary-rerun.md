# 2026-07-14 Claude Code Compact ZC-04 Agama Boundary Rerun

| Field | Value |
|---|---|
| Date | 2026-07-14 |
| Scenario | Compact `ZC-04` Agama citation-boundary rerun after Agama collation-boundary prompt wording was tightened |
| Route / provider | Claude Code UTF-8 stdin |
| Tool version | Claude Code 2.1.204 |
| System prompt | `agents/zilan-claude-code.md` from `main` at `25bdb5d` |
| Repository base | `25bdb5d` (`Tighten Agama collation boundary wording (#119)`) |
| Branch | `zc04-agama-boundary-rerun` |
| Source location | Raw Claude JSON and extracted answer Markdown kept local only under `C:\tmp\zilan-zc04-boundary-rerun-20260714` |
| Redaction note | No secrets are included here. Raw JSON, session identifiers, and full transcripts are not committed. |
| Runtime log entry | `docs/runtime-validation-log.md#2026-07-14-claude-code-compact-zc-04-agama-boundary-rerun` |

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
请按 ZC-04 的任务意图执行一次精简 runtime spot review：spawn 一个 zilan agent，查四阿含中关于无我的经文，并做初步归类分析。不要写文件；只输出最多 6 条代表性证据。每条证据必须注明经名、CBETA 编号、卷数或段落标题、context/agama/...:行号。本回答开头说明检索范围，结尾说明这些只是代表性初步证据且仍待校勘，不是穷尽校勘或出版级定本。
```

Contract review command:

```powershell
python scripts\semantic_answer_contract_review.py --query-id SRQ-04 --answer-file C:\tmp\zilan-zc04-boundary-rerun-20260714\ZC-04-compact-rerun.answer.md --json
```

## Output Excerpt

```text
检索范围
- 检索文件：`context/agama/T0001-chang-agama.md`（长阿含）、`T0026-zhong-agama.md`（中阿含）、`T0099-za-agama.md`（杂阿含）、`T0125-ekottarika-agama.md`（增壹阿含）。排除 `context/agama/_source/`。
...
六条代表性证据
《雜阿含經》(T02n0099) 卷 1,（九）, `context/agama/T0099-za-agama.md:147`
《雜阿含經》(T02n0099) 卷 1,（二四）罗睺罗所问经, `context/agama/T0099-za-agama.md:463`
《中阿含經》(T01n0026) 卷 42,（一六二）根本分别品分别六界经第一, `context/agama/T0026-zhong-agama.md:13975`
《長阿含經》(T01n0001) 卷 10,（一三）第二分大缘方便经第九, `context/agama/T0001-chang-agama.md:3995`
...
以上六条为本地 Markdown 语料中初步检索的代表性证据，不代表四阿含"无我"主题的全量穷举。
待校勘：本地 Markdown 是工作语料；出版级或义理定案需回到 CBETA XML-P5、平行译本...复核。本次检索未作校勘定案，不能作为定本使用。
```

## Contract Results

| Answer | Reviewed Against | Result | Notes |
|---|---|---:|---|
| `ZC-04-compact-rerun.answer.md` | `SRQ-04` / `agama_citation_boundary` | `pass` | Required terms and slots are present, including search scope, representative-status language, `CBETA`, `T02n0099`, local `context/agama/` anchors, local line numbers, paragraph markers/titles, `待校勘`, and publication-level boundary language. No forbidden terms were present. |

## Findings

- The compact `ZC-04` rerun now passes the `SRQ-04` answer contract after the prompt wording change in #119.
- The answer uses the preferred boundary wording `未作校勘定案，不能作为定本使用`, avoiding the prior shallow forbidden-term false trigger.
- This is target-contract evidence only. It does not change Claude Code, Codex, OpenAI API, or provider-route status.

## Known Limits

- This is a compact target-contract rerun, not a full ZC-01 through ZC-06 platform rerun.
- It validates the current Claude Code CLI route with repository prompt loaded through UTF-8 stdin; it does not validate native OpenAI API or any OpenAI-compatible provider route.
- The answer-contract helper is a minimum explicitness check and does not grade doctrinal correctness or retrieval completeness.
- Raw Claude JSON and the full answer file remain local only under `C:\tmp\zilan-zc04-boundary-rerun-20260714`.