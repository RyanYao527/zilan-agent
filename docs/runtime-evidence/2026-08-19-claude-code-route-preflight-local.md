# 2026-08-19 Claude Code Route Preflight

## Scope

This note records a local Claude Code route preflight after the `SRQ-11` post-hardening runtime rerun was blocked.
It is provider/smoke evidence only: no provider call, answer generation, runtime pass, settings edit, or platform-status
change is claimed here.

## Command

```powershell
python scripts\claude_code_route_preflight.py --observed-error-file docs\runtime-evidence\2026-08-19-srq11-definition-runtime-rerun.md --json
```

## Result Summary

| Field | Value |
|---|---|
| Report mode | `claude-code-route-preflight-v1` |
| Route status | `blocked` |
| Claude CLI | available |
| Claude Code version observed by preflight | `2.1.169 (Claude Code)` |
| Settings file | local user `~/.claude/settings.json`, read-only |
| Custom base URL | `https://api.deepseek.com/anthropic` |
| Selected model | `deepseek-v4-pro[1m]` |
| Observed error source | `docs/runtime-evidence/2026-08-19-srq11-definition-runtime-rerun.md` |
| Observed error | `[claude-code:unrecognized_model]` for model `deepseek-v4-pro[1m]` |
| Sensitive values | not printed; the report only records sensitive key names as present |

## Interpretation

- Claude Code CLI is present locally.
- The local route is currently configured through a custom Anthropic-compatible DeepSeek endpoint.
- The recorded `SRQ-11` rerun error shows Claude Code rejected the custom model name before answer generation.
- The next `SRQ-11` runtime attempt should wait until the local Claude Code route is known to accept the selected model.

## Boundaries

- This note is not an answer excerpt and must not be used as `answer_file`.
- This note does not validate native DeepSeek, native OpenAI API, Claude Code answer quality, or platform support.
- `docs/platform-validation.md` remains unchanged.
