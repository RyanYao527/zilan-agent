# 2026-06-18 Claude Code Post-Contract Full Rerun

## Summary

| Field | Value |
|---|---|
| Date | 2026-06-18 |
| Route | Claude Code UTF-8 stdin |
| Tool version | Claude Code 2.1.169 |
| System prompt | `agents/zilan-claude-code.md` |
| Repository base | `3b14473` (`Tighten Madhyamaka prasanga output contract (#48)`) |
| Branch | `codex/claude-post-contract-full-rerun-20260618` |
| Prompt set | `ZC-01` through `ZC-06` from `tests/regression_cases.yaml` |
| Transcript status | Compact evidence committed here; raw Claude JSON and answer Markdown kept local only under `C:\tmp\zilan-claude-post-contract-full-rerun-20260618` |
| Platform status effect | No status promotion. This refreshes Claude Code `tested` evidence after the Agama and Madhyamaka output-contract changes. |

## Command Shape

```powershell
$OutputEncoding = [System.Text.UTF8Encoding]::new($false)
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)
$sp = Get-Content -Raw -Encoding UTF8 -LiteralPath 'agents\zilan-claude-code.md'
$prompt | claude -p --safe-mode --output-format json --permission-mode bypassPermissions --allowedTools Read,Grep,Glob,Bash,Write --system-prompt "$sp"
```

## Local Output Inventory

| Case | Session ID | Answer chars | Duration |
|---|---|---:|---:|
| `ZC-01` | `b1733d0d-b06a-499a-89d4-a75f60ee81bf` | 1153 | 38.6s |
| `ZC-02` | `51f22289-7002-46ec-8dfe-cfb71b9c203a` | 1319 | 31.1s |
| `ZC-03` | `34dcb5f8-56bc-45d5-b565-e9b2a6c44a3a` | 4551 | 80.3s |
| `ZC-04` | `9c3dd1f7-9019-4372-9d26-94fe1bc5f77a` | 5313 | 218.1s |
| `ZC-05` | `d74a4216-040d-426f-a306-dbf68c804ad8` | 5359 | 134.5s |
| `ZC-06` | `c0f9a521-90d6-4892-856e-64a7acf3aaef` | 653 | 416.9s |

## Case Results

| Case | Result | Review note |
|---|---:|---|
| `ZC-01` | `pass` | Directly answered the work-feedback scenario, separated the event from self-worth, used the five-mental-factor chain and bounded practice guidance. |
| `ZC-02` | `pass` | Explained `因三相` with `遍是宗法性`, `同品定有性`, and `异品遍无性`. |
| `ZC-03` | `pass` | Combined Collected Topics and cognitive-analysis framing, including `不周遍`, `受`, `想`, `瞋`, and a practice / clinical boundary. The answer covered labeling/categorization behavior even if not every regression keyword appears as a literal phrase. |
| `ZC-04` | `pass` | Produced an Agama no-self search and preliminary classification with CBETA identifiers, local Markdown line anchors, representative evidence, and collation boundaries. Note: some local references used shorter file anchors instead of the full `context/agama/` prefix; this case was not reviewed against `SRQ-04`. |
| `ZC-05` | `pass` | Broad cross-domain answer preserved Agama evidence and Madhyamaka prasaṅga boundaries after the prompt-contract fixes. Mechanical contract review passed both `SRQ-03` and `SRQ-04`. |
| `ZC-06` | `pass` | Generated the requested long report and wrote it to `~/.claude/skills/zilan-agent/reports/阿含无我观法门研究报告.md`. Local file check confirmed the report exists; it was not committed to the repository. |

## Contract Review Commands

```powershell
python scripts\semantic_answer_contract_review.py --query-id SRQ-03 --answer-file C:\tmp\zilan-claude-post-contract-full-rerun-20260618\ZC-05.answer.md --json
python scripts\semantic_answer_contract_review.py --query-id SRQ-04 --answer-file C:\tmp\zilan-claude-post-contract-full-rerun-20260618\ZC-05.answer.md --json
```

## Contract Results

| Answer | Contract | Result | Missing required terms | Present forbidden terms |
|---|---|---:|---|---|
| `ZC-05.answer.md` | `SRQ-03` Madhyamaka prasaṅga boundary | `pass` | none | none |
| `ZC-05.answer.md` | `SRQ-04` Agama citation boundary | `pass` | none | none |

## ZC-06 File Output

Claude Code reported:

> 研究报告已完成并写入 `~/.claude/skills/zilan-agent/reports/阿含无我观法门研究报告.md`。

The generated report file existed at review time and was 31,760 bytes. The answer summary stated:

- search scope covered four Agama Markdown corpora: `T01n0001`, `T01n0026`, `T02n0099`, and `T02n0125`
- the report listed 19 representative citations with CBETA IDs, fascicle information, and local line anchors
- the report marked a `待校勘` boundary for CBETA XML-P5 or parallel-text verification

## Limitations

- This validates the local Claude Code CLI route with repository `agents/zilan-claude-code.md` loaded as the system prompt and UTF-8 stdin used for Chinese prompts.
- It does not validate native OpenAI API or any OpenAI-compatible provider route.
- Background auto-spawn behavior was not separately audited; ZC-04 through ZC-06 used explicit spawn-style prompts through the loaded Claude Code agent prompt.
- Raw JSON and full answer files remain local only to avoid committing large runtime payloads.
- `semantic_answer_contract_review.py` is a minimum explicitness check, not doctrinal grading.
