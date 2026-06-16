# Provider Route Triage

> Last updated: 2026-06-16

This document records the current state of non-Codex provider routes. It is a triage note, not runtime validation evidence. Platform status remains governed by `agents/openai.yaml` and `docs/platform-validation.md`.

## Current Route Summary

| Route | Current status | Triage | Next action |
|---|---|---|---|
| OpenAI API | `harness-ready` | Dry-run Responses API harness exists and is covered by tests. `OPENAI_API_KEY` was not present in the local environment during this triage. | Run `scripts/openai_api_harness.py --live` with `OPENAI_API_KEY`, then record evidence. |
| Volcengine OpenAI-Compatible | `tested` | ZC-01 through ZC-03 passed on 2026-06-16 through the shared harness with `chat-completions`, provider route `volcengine_openai_compatible`, base URL `https://ark.cn-beijing.volces.com/api/coding/v3`, model `ark-code-latest`, and provider-specific `VOLCENGINE_OPENAI_API_KEY`. Evidence is summarized in `docs/runtime-validation-log.md`, `docs/runtime-evidence/2026-06-16-volcengine-openai-compatible-zc-01-zc-03-live.md`, and `docs/runtime-evidence/2026-06-16-volcengine-openai-compatible-zc-02-live.md`. | Use `--provider-route volcengine_openai_compatible` for future dry-run/live calls. Keep native OpenAI API separate; expand this route to ZC-04 through ZC-06 only if broader Volcengine validation is needed. |
| DeepSeek | `config-only` | Provider metadata exists. No native DeepSeek harness or `DEEPSEEK_API_KEY` was present. Claude Code local model usage is not the same as native DeepSeek route validation. | Add a native harness or document a blocked state with reproducible provider details. |
| GLM | `config-only` | Provider metadata exists. No GLM harness or `ZHIPUAI_API_KEY` was present. | Add a minimal harness or keep as metadata only. |
| Qwen | `config-only` | Provider metadata exists. No Qwen harness or `DASHSCOPE_API_KEY` was present. | Add a minimal harness or keep as metadata only. |

## Local Credential Probe

The 2026-06-15 triage checked only whether common environment variables existed. It did not read or print secret values.

| Variable | Present |
|---|---|
| `OPENAI_API_KEY` | no |
| `VOLCENGINE_OPENAI_API_KEY` | provided in the user's local PowerShell session for the 2026-06-16 ZC-02 run; value was not shared or committed |
| `DEEPSEEK_API_KEY` | no |
| `ZHIPUAI_API_KEY` | no |
| `DASHSCOPE_API_KEY` | no |

## DeepSeek Caveat

`AGENT_UPGRADE_PORTABLE.md` documents an Anthropic-compatible endpoint issue observed during earlier Claude Code agent-spawn attempts. That caveat should not be treated as native DeepSeek API validation and should not be generalized beyond the documented route.

The current conservative interpretation is:

- Claude Code route: validated through Claude Code CLI on 2026-06-12 and rerun successfully on 2026-06-16 after identifying the 2026-06-15 failure as a Windows PowerShell UTF-8 stdin issue; track that separately from native DeepSeek validation.
- DeepSeek native route: still `config-only` until a native harness or dated provider run exists.
- DeepSeek Anthropic-compatible route: keep the documented caveat visible if using Claude Code through that compatibility layer.

## Adding A New Provider Harness

A provider harness should:

- load prompt metadata from `agents/openai.yaml` or a similarly versioned provider config
- use `tests/regression_cases.yaml` for prompt selection
- support dry-run by default
- require an explicit `--live` flag for network calls
- fail fast when the required API key is missing
- record response summaries according to `docs/validation-evidence.md`

Do not update a provider to `tested` until the live run is recorded in `docs/runtime-validation-log.md`.

## OpenAI-Compatible Provider Protocol

For a provider such as Volcengine that exposes an OpenAI-compatible route, use provider-specific environment variables so the result cannot be mistaken for native OpenAI API validation:

```powershell
$env:OPENAI_BASE_URL = "https://<provider-openai-compatible-base-url>/v1"
$env:OPENAI_MODEL = "<provider-model-id>"
$env:OPENAI_API_SURFACE = "chat-completions"
$env:OPENAI_API_KEY_ENV = "VOLCENGINE_OPENAI_API_KEY"
$env:VOLCENGINE_OPENAI_API_KEY = "..."
python scripts\openai_api_harness.py --case ZC-02 --provider-route volcengine_openai_compatible --live --json
```

Record a successful run as Volcengine OpenAI-compatible evidence unless the request uses `https://api.openai.com/v1` with an official `OPENAI_API_KEY`.
