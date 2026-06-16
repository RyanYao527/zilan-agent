# 2026-06-16 Claude Code UTF-8 Rerun Evidence

| Field | Value |
|---|---|
| Date | 2026-06-16 |
| Scenario | Claude Code UTF-8 stdin rerun |
| Route / provider | Claude Code CLI 2.1.169; local JSON usage reported `deepseek-v4-pro[1m]` |
| Repository commit | `872b6bd` before merge; released in `v2.4.6` at `985c51c` |
| Source location | Operator transcript summarized in `docs/runtime-validation-log.md` |
| Redaction note | Full JSON responses are not committed; no API keys, account metadata, or private provider headers are included. |
| Runtime log entry | `docs/runtime-validation-log.md#2026-06-16-claude-code-utf-8-stdin-rerun` |

## Commands Or Prompts

```text
$OutputEncoding = [System.Text.UTF8Encoding]::new($false)
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)
$sp = Get-Content -Raw -Encoding UTF8 -LiteralPath 'agents\zilan-claude-code.md'
$prompt | claude -p --safe-mode --output-format json --permission-mode bypassPermissions --allowedTools Read,Grep,Glob,Bash,Write --system-prompt "$sp"
```

The prompt set covered ZC-01 through ZC-06 from `tests/regression_cases.yaml`.

## Output Excerpts

```text
Default PowerShell pipe echo control:
<msg>?????????????????</msg>

UTF-8 PowerShell pipe echo control:
<msg>
孜澜，什么是因三相？请用三点回答。
</msg>

ZC-02 summary:
Covered 遍是宗法性, 同品定有性, 异品遍无性 and connected them to 摄类学.

ZC-06 summary:
Wrote C:\tmp\zilan-claude-validation-20260616-ZC06.md and reported local context/search usage.
```

## Result

| Check / case | Result | Notes |
|---|---|---|
| Encoding control | `pass` | UTF-8 stdin preserved Chinese prompt text; default PowerShell pipe did not. |
| ZC-01 through ZC-06 | `pass` | Case-level summaries are recorded in `docs/runtime-validation-log.md`. |
| File output | `pass` | ZC-06 wrote a report outside the repository at `C:\tmp\zilan-claude-validation-20260616-ZC06.md`. |

## Limitations

- This is a compact evidence excerpt, not a full transcript archive.
- Background auto-spawn behavior was not separately audited.
- Windows PowerShell users must set UTF-8 output encodings before piping Chinese prompts to `claude -p`.
