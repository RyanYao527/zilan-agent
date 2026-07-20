# 2026-07-14 Claude Code SRQ-04 / ZC-04 Agama Boundary Spot Review

| Field | Value |
|---|---|
| Date | 2026-07-14 |
| Scenario | Agama citation-boundary spot review for `SRQ-04` plus a compact `ZC-04`-style no-self Agama search |
| Route / provider | Claude Code UTF-8 stdin |
| Tool version | Claude Code 2.1.204 |
| System prompt | `agents/zilan-claude-code.md` from `main` at `512a333` |
| Repository base | `512a333` (`Preserve Agama section titles in citations (#117)`) |
| Branch | `srq04-agama-runtime-spot-review` |
| Source location | Raw Claude JSON and extracted answer Markdown kept local only under `C:\tmp\zilan-srq04-zc04-spot-review-20260714` |
| Redaction note | No secrets are included here. Raw JSON, session identifiers, and full transcripts are not committed. |
| Runtime log entry | `docs/runtime-validation-log.md#2026-07-14-claude-code-srq-04--zc-04-agama-citation-boundary-spot-review` |

## Commands Or Prompts

Command shape:

```powershell
$OutputEncoding = [System.Text.UTF8Encoding]::new($false)
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)
[Console]::InputEncoding = [System.Text.UTF8Encoding]::new($false)
$sys = Get-Content -Raw -Encoding UTF8 -LiteralPath 'agents\zilan-claude-code.md'
$prompt | claude -p --output-format json --system-prompt $sys --add-dir . --dangerously-skip-permissions
```

Prompt set:

```text
SRQ-04:
孜澜，请查四阿含中关于无我的经文，并说明检索范围与待校勘边界。请至少给出代表性阿含证据，引用时注明经名、CBETA 编号、卷数或段落标题、本地 context/agama 文件行号，并明确说明这只是代表性检索，不是穷尽校勘。

ZC-04 exact:
请 spawn 一个 zilan agent，查四阿含中关于无我的经文，并做初步归类分析。

ZC-04 compact spot review:
请按 ZC-04 的任务意图执行一次精简 runtime spot review：spawn 一个 zilan agent，查四阿含中关于无我的经文，并做初步归类分析。不要写文件；只输出最多 6 条代表性证据。每条证据必须注明经名、CBETA 编号、卷数或段落标题、context/agama/...:行号。本回答开头说明检索范围，结尾说明这些只是代表性初步证据且仍待校勘，不是穷尽校勘或出版级定本。
```

The exact `ZC-04` prompt timed out after 304 seconds and produced no saved answer file. The compact rerun keeps the same Agama-search intent but bounds output length for spot-review purposes.

## Output Excerpts

Direct `SRQ-04` answer:

```text
检索对象：四阿含 Markdown 纯文本正文（`context/agama/T00*-*.md`），不检索 `context/agama/_source/` 中的 CBETA TEI P5 XML 底本。
...
| 雜阿含經 | T02n0099 | `context/agama/T0099-za-agama.md` | 53 处 |
...
声明：以下为代表性引文，并非穷尽检索。待校勘：本地 Markdown 是工作语料；出版级或义理定案需回到 CBETA XML-P5、平行译本或巴利对应文本校验。
...
—《長阿含經》(T01n0001) 卷 1, （一）第一分初大本經第一, `context/agama/T0001-chang-agama.md:881`
—《長阿含經》(T01n0001) 卷 10, （一三）佛說長阿含第二分大緣方便經第九, `context/agama/T0001-chang-agama.md:4005`
```

Compact `ZC-04`-style answer:

```text
检索目标：四阿含 Markdown 正文（`T0001` 长阿含、`T0026` 中阿含、`T0099` 杂阿含、`T0125` 增壹阿含），排除 `_source/` 源文件
...
—《雜阿含經》(T02n0099) 卷 1,（九）, `context/agama/T0099-za-agama.md:147`
—《長阿含經》(T01n0001) 卷 10, 大緣方便經第九, `context/agama/T0001-chang-agama.md:3995-4005`
...
以上 6 条是从约 300 条命中中选取的代表性初步证据...
本地 Markdown 文本为工作语料，仍待校勘——出版级引文或义理定案需回到 CBETA XML-P5、平行译本或巴利对应文本复核。
本报告不构成校勘确认，不作为出版级定本使用。
```

## Contract Review Commands

```powershell
python scripts\semantic_answer_contract_review.py --query-id SRQ-04 --answer-file C:\tmp\zilan-srq04-zc04-spot-review-20260714\SRQ-04.answer.md --json
python scripts\semantic_answer_contract_review.py --query-id SRQ-04 --answer-file C:\tmp\zilan-srq04-zc04-spot-review-20260714\ZC-04-compact.answer.md --json
```

## Contract Results

| Answer | Reviewed Against | Result | Notes |
|---|---|---:|---|
| `SRQ-04.answer.md` | `SRQ-04` / `agama_citation_boundary` | `pass` | Required terms and slots all present, including search scope, `CBETA`, `T02n0099`, local `context/agama/` anchors, representative-status language, and `待校勘`; no forbidden terms present. Manual excerpt review also confirms title-bearing `長阿含經` citations preserve paragraph titles where available. |
| `ZC-04-compact.answer.md` | `SRQ-04` / `agama_citation_boundary` | `fail` | Required terms and slots all present, including CBETA/local anchors, representative-status language, local line anchors, section markers or titles, and collation boundary language. Mechanical review fails only because the negated boundary phrase `不构成校勘确认` contains forbidden term `校勘确认`. |

## Standalone Answer Excerpts

| Case | Answer excerpt | Reviewed against | Result |
|---|---|---|---|
| `SRQ-04` | `docs/runtime-evidence/2026-07-14-claude-code-srq-04-agama-boundary-spot-answer.md` | `SRQ-04` | `pass` in `docs/runtime-evidence/2026-07-20-compact-zc-04-answer-excerpt-progression-batch.md` |
| compact `ZC-04` before wording fix | `docs/runtime-evidence/2026-07-14-claude-code-zc-04-compact-spot-answer.md` | `SRQ-04` | `fail` in `docs/runtime-evidence/2026-07-20-compact-zc-04-answer-excerpt-progression-batch.md` |
## Findings

- Direct `SRQ-04` remains stable after Agama `section_title` citation metadata work.
- The compact `ZC-04`-style answer covers the intended citation-boundary slots but exposes a shallow-contract nuance: forbidden collation-overclaim terms are currently matched literally even when they occur in a negated boundary statement.
- This is target-contract evidence only. It does not change Claude Code, Codex, OpenAI API, or provider-route status.

## Known Limits

- This is a target-contract spot review, not a full ZC-01 through ZC-06 platform rerun.
- The exact broad `ZC-04` prompt timed out and did not produce a saved answer; the compact rerun is documented separately.
- The answer-contract helper is a minimum explicitness check and does not understand negation scope.
- Raw Claude JSON and full answer files remain local only under `C:\tmp\zilan-srq04-zc04-spot-review-20260714`.