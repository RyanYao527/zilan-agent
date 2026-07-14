# 2026-07-14 Claude Code Post-Prompt ZC-01 To ZC-06 Rerun

| Field | Value |
|---|---|
| Date | 2026-07-14 |
| Scenario | Claude Code full `ZC-01` through `ZC-06` rerun after root-document archival and closing Dharma-seal wording changes |
| Route / provider | Claude Code UTF-8 stdin |
| Tool version | Claude Code 2.1.204 |
| System prompt | `agents/zilan-claude-code.md` from `main` at `b78732a` |
| Repository base | `b78732a` (`docs: update closing dharma seal (#122)`) |
| Branch | `claude-post-prompt-rerun-evidence` |
| Source location | Raw Claude JSON and extracted answer Markdown kept local only under `C:\tmp\zilan-claude-post-prompt-rerun-20260714` |
| Generated report | `ZC-06` wrote `C:\Users\rori9\Desktop\阿含无我观法门研究报告.md`; the report is not committed |
| Redaction note | No secrets are included here. Raw JSON, session identifiers, and full transcripts are not committed. |
| Runtime log entry | `docs/runtime-validation-log.md#2026-07-14-claude-code-post-prompt-zc-01-to-zc-06-rerun` |

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

| Case | Prompt |
|---|---|
| `ZC-01` | `孜澜，我今天收到工作反馈后心里很难受。` |
| `ZC-02` | `孜澜，什么是因三相？` |
| `ZC-03` | `孜澜，用摄类学和心类学解释“收到批评后我很受挫”的认知过程。` |
| `ZC-04` | `请 spawn 一个 zilan agent，查四阿含中关于无我的经文，并做初步归类分析。` |
| `ZC-05` | `请 spawn 一个 zilan agent，用应成论式分析诸法无我，并串联阿含、摄类学、因明和观禅。` |
| `ZC-06` | `请 spawn 一个 zilan agent，生成一份“阿含无我观法门”研究报告并写入文件。` |

## Runtime Results

| Case | Claude subtype | Duration ms | Turns | Answer chars | Result | Notes |
|---|---:|---:|---:|---:|---|---|
| `ZC-01` | `success` | 53390 | 4 | 2716 | `pass` | Lightweight practice support response; no file output. |
| `ZC-02` | `success` | 35109 | 3 | 1405 | `pass` | Explains `因三相` with expected Hetuvidya terminology. |
| `ZC-03` | `success` | 80692 | 3 | 5489 | `pass` | Cross-domain Collected Topics / cognitive-analysis answer; `SRQ-09` contract review passed. |
| `ZC-04` | `success` | 8725 | 1 | 903 | `partial` | Runtime succeeded, but the main answer is a compact summary and fails `SRQ-04` answer-contract review for missing explicit citation-boundary slots. |
| `ZC-05` | `success` | 19240 | 1 | 1727 | `partial` | `SRQ-03` prasaṅga boundary passed; `SRQ-08` nihilism-boundary review failed because explicit `断灭` / `二谛` / `不成立` slots were missing. |
| `ZC-06` | `success` | 4437 | 1 | 372 | `pass` | Main answer reports a generated file. The generated report passes `SRQ-04` answer-contract review. |

## Contract Results

| Answer | Reviewed Against | Result | Notes |
|---|---|---:|---|
| `ZC-03.answer.md` | `SRQ-09` / `cognitive_practice_boundary` | `pass` | Required cognitive-chain, cognitive-quality, corrective-factor, vipassana mapping, and practice-boundary slots are present. |
| `ZC-04.answer.md` | `SRQ-04` / `agama_citation_boundary` | `fail` | Missing required terms `T02n0099`, `context/agama/`, `检索范围`, and `代表性`; missing `search_scope` and `evidence_status` slots. |
| `ZC-05.answer.md` | `SRQ-03` / `madhyamaka_prasanga_boundary` | `pass` | Required prasaṅga terms and slots are present, including opponent premise, contradiction, and no-independent-thesis boundary. |
| `ZC-05.answer.md` | `SRQ-08` / `madhyamaka_nihilism_boundary` | `fail` | Missing required terms `断灭`, `二谛`, and `不成立`; missing `nihilism_error` slot. |
| `阿含无我观法门研究报告.md` | `SRQ-04` / `agama_citation_boundary` | `pass` | Generated report includes `CBETA`, `T02n0099`, local `context/agama/` anchors, search scope, representative-status language, and collation boundary terms. |

## Output Excerpts

```text
ZC-04:
四阿含中统一使用“非我”而非“无我”。
统计总量：杂阿含 177, 增壹阿含 47, 中阿含 35, 长阿含 17, 共 276。
边界：上述引文仍“待校勘”；此为本地 Markdown 语料的工作统计，出版级引用仍需回到 CBETA XML-P5 与平行译本核对。

ZC-05:
对方承许：诸法自性有。归谬：若诸法自性有，则不应依缘起而生灭；但阿含与中观均以缘起说明诸法无我，故自性有与缘起相违。
边界：这不是建立“诸法绝对不存在”的自宗，而是只破“自性有”的执著。

ZC-06:
已生成并写入文件：
C:\Users\rori9\Desktop\阿含无我观法门研究报告.md
```

## Findings

- Claude Code route remains executable through the current UTF-8 stdin protocol: all six invocations returned `success`.
- The post-#121/#122 prompt and public-document wording changes did not break the basic ZC runtime path.
- Strict contract review still exposes two narrow follow-up gaps:
  - broad `ZC-04` main responses should preserve the same explicit `SRQ-04` citation-boundary slots as compact `ZC-04` and `ZC-06` report outputs;
  - broad `ZC-05` responses should explicitly reject the `SRQ-08` nihilism reading with `断灭`, `二谛`, and `不成立` language.
- This evidence does not change Claude Code, Codex, native OpenAI API, or OpenAI-compatible provider-route status.

## Known Limits

- Raw Claude JSON and full answer Markdown remain local only under `C:\tmp\zilan-claude-post-prompt-rerun-20260714`.
- The generated `ZC-06` report is outside the repository and is summarized rather than committed.
- The answer-contract helper is a minimum explicitness check. It does not grade doctrinal correctness, retrieval completeness, or platform behavior.
- One pre-existing `claude.exe` process was observed after the rerun, but it predates this validation run and was not modified.