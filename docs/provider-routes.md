# Provider Route Triage

> Last updated: 2026-06-15

This document records the current state of non-Codex provider routes. It is a triage note, not runtime validation evidence. Platform status remains governed by `agents/openai.yaml` and `docs/platform-validation.md`.

## Current Route Summary

| Route | Current status | 2026-06-15 triage | Next action |
|---|---|---|---|
| OpenAI API | `harness-ready` | Dry-run Responses API harness exists and is covered by tests. `OPENAI_API_KEY` was not present in the local environment during this triage. | Run `scripts/openai_api_harness.py --live` with `OPENAI_API_KEY`, then record evidence. |
| DeepSeek | `config-only` | Provider metadata exists. No native DeepSeek harness or `DEEPSEEK_API_KEY` was present. Claude Code local model usage is not the same as native DeepSeek route validation. | Add a native harness or document a blocked state with reproducible provider details. |
| GLM | `config-only` | Provider metadata exists. No GLM harness or `ZHIPUAI_API_KEY` was present. | Add a minimal harness or keep as metadata only. |
| Qwen | `config-only` | Provider metadata exists. No Qwen harness or `DASHSCOPE_API_KEY` was present. | Add a minimal harness or keep as metadata only. |

## Local Credential Probe

The 2026-06-15 triage checked only whether common environment variables existed. It did not read or print secret values.

| Variable | Present |
|---|---|
| `OPENAI_API_KEY` | no |
| `DEEPSEEK_API_KEY` | no |
| `ZHIPUAI_API_KEY` | no |
| `DASHSCOPE_API_KEY` | no |

## DeepSeek Caveat

`AGENT_UPGRADE_PORTABLE.md` documents an Anthropic-compatible endpoint issue observed during earlier Claude Code agent-spawn attempts. That caveat should not be treated as native DeepSeek API validation and should not be generalized beyond the documented route.

The current conservative interpretation is:

- Claude Code route: validated through Claude Code CLI on 2026-06-12, but blocked again in the 2026-06-15 wake-word noninteractive rerun; track that separately from native DeepSeek validation.
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
