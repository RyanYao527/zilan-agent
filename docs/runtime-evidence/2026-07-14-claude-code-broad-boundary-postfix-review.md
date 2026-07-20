# 2026-07-14 Claude Code Broad Boundary Postfix Review

| Field | Value |
|---|---|
| Date | 2026-07-14 |
| Scenario | Runtime spot review after broad boundary prompt hardening in #124 |
| Route / provider | Claude Code UTF-8 stdin |
| Tool version | Claude Code 2.1.204 |
| System prompt | `agents/zilan-claude-code.md` from `main` at `c6b686c` |
| Repository base | `c6b686c` (`Harden broad boundary prompt slots (#124)`) |
| Branch | `post-broad-boundary-runtime-review` |
| Source location | Raw Claude JSON and extracted answer Markdown kept local only under `C:\tmp\zilan-claude-broad-boundary-postfix-20260714` |
| Redaction note | No secrets are included here. Raw JSON, session identifiers, and full transcripts are not committed. |
| Runtime log entry | `docs/runtime-validation-log.md#2026-07-14-claude-code-broad-boundary-postfix-review` |

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
| `ZC-04` | Broad `四阿含` `无我` survey and preliminary classification prompt. |
| `ZC-05` | Broad `应成论式` analysis of `诸法无我`, connecting Agama, `摄类学`, `因明`, and `观禅`. |

The first combined two-case command hit its total timeout after `ZC-04` completed and before `ZC-05` started. No residual `claude` process remained. `ZC-05` was then run separately with the same command shape.

## Runtime Results

| Case | Claude subtype | Duration ms | Turns | Answer chars | Result | Notes |
|---|---:|---:|---:|---:|---|---|
| `ZC-04` | `success` | 13518 | 1 | 1008 | `partial` | Runtime succeeded, but strict `SRQ-04` answer-contract review still fails on missing `检索范围`, `T02n0099`, and `search_scope`. |
| `ZC-05` | `success` | 34935 | 1 | 3207 | `pass` | Broad cross-domain answer now passes `SRQ-03`, `SRQ-04`, and `SRQ-08` after fixture conflict correction described below. |

## Contract Results

| Answer | Reviewed Against | Result | Notes |
|---|---|---:|---|
| `ZC-04.answer.md` | `SRQ-04` / `agama_citation_boundary` | `fail` | Missing required terms `T02n0099` and `检索范围`; missing `search_scope` slot. It does include `CBETA`, `context/agama/`, `代表性`, and `待校勘`. |
| `ZC-05.answer.md` | `SRQ-04` / `agama_citation_boundary` | `pass` | Required Agama citation-boundary terms and slots are present. |
| `ZC-05.answer.md` | `SRQ-03` / `madhyamaka_prasanga_boundary` | `pass` | Passed after `SRQ-03` forbidden terms were narrowed from bare `断灭` to the nihilistic phrase `断灭的结论`; this avoids conflict with the `SRQ-08` requirement to mention `断灭` as a boundary term. |
| `ZC-05.answer.md` | `SRQ-08` / `madhyamaka_nihilism_boundary` | `pass` | Required `只破自性有`, `断灭`, `二谛`, and `不成立` slots are present; no forbidden nihilism phrases are present. |

## Standalone Answer Excerpts

| Case | Answer excerpt | Reviewed against | Result |
|---|---|---|---|
| `ZC-05` | `docs/runtime-evidence/2026-07-14-claude-code-zc-05-broad-boundary-postfix-answer.md` | `SRQ-04`, `SRQ-03`, `SRQ-08` | `pass` in `docs/runtime-evidence/2026-07-20-latest-zc-answer-excerpt-review-batch.md` |

## Output Excerpts

```text
ZC-04: reported a complete report with 16 代表性 sutra citations, CBETA IDs, local line anchors, a classification map, and a 待校勘 statement; it cited `context/agama/` paths but still omitted `检索范围` and `T02n0099` in the main response.
ZC-05: retained `检索范围`, `context/agama/`, `T02n0099`, `对方承许`, `自性有`, `归谬`, `只破自性有`, `非断灭`, `二谛`, `不成立`, and `待校勘` boundary wording in the main response.
```

## Findings

- #124 materially improved broad `ZC-05`: it now preserves Agama citation-boundary slots and Madhyamaka nihilism-boundary slots in the main response.
- `SRQ-03` and `SRQ-08` had a shallow contract conflict: `SRQ-03` forbade the bare word `断灭`, while `SRQ-08` requires it as a boundary term. This PR narrows `SRQ-03` to forbid the phrase `断灭的结论` instead.
- Broad `ZC-04` still needs a separate prompt or fixture follow-up. It reports that the agent produced a complete report and mentions representative evidence, CBETA, local anchors, and collation boundaries, but it still omits the literal `检索范围` and `T02n0099` slots in the main answer.
- This evidence does not change Claude Code, Codex, native OpenAI API, or OpenAI-compatible provider-route status.

## Known Limits

- Raw Claude JSON and full answer Markdown remain local only under `C:\tmp\zilan-claude-broad-boundary-postfix-20260714`.
- This is a two-case runtime spot review, not a full ZC-01 through ZC-06 platform rerun.
- The answer-contract helper is a minimum explicitness check and does not grade doctrinal correctness, retrieval completeness, or platform behavior.
