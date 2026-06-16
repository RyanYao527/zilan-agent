# 2026-06-16 Volcengine OpenAI-Compatible ZC-02 Live Evidence

## Summary

| Field | Value |
|---|---|
| Date | 2026-06-16 |
| Route | Volcengine OpenAI-compatible |
| Harness | `scripts/openai_api_harness.py` |
| Mode | `live` |
| API surface | `chat-completions` |
| Model | `ark-code-latest` |
| Base URL | `https://ark.cn-beijing.volces.com/api/coding/v3` |
| Endpoint | `https://ark.cn-beijing.volces.com/api/coding/v3/chat/completions` |
| API key env | `VOLCENGINE_OPENAI_API_KEY` |
| Case | ZC-02 |
| Prompt | `孜澜，什么是因三相？` |
| Repository base | Post-PR #23 `main` at `a04bbe0`; evidence committed on `codex/volcengine-live-evidence` |
| Evidence source | User-supplied local PowerShell harness output |

## Redaction Note

- The API key value was not shared and is not committed.
- The provider response ID is redacted.
- The full request and full response payload are not committed because the request embeds a large local context bundle and provider metadata.
- This evidence supports only the Volcengine OpenAI-compatible route, not native OpenAI API validation.

## Command Shape

```powershell
$env:OPENAI_BASE_URL = "https://ark.cn-beijing.volces.com/api/coding/v3"
$env:OPENAI_MODEL = "ark-code-latest"
$env:OPENAI_API_SURFACE = "chat-completions"
$env:OPENAI_API_KEY_ENV = "VOLCENGINE_OPENAI_API_KEY"
$env:VOLCENGINE_OPENAI_API_KEY = "[redacted]"
python scripts\openai_api_harness.py --case ZC-02 --live --json
```

## Output Excerpts

```text
mode: live
model: ark-code-latest
case_id: ZC-02
endpoint: https://ark.cn-beijing.volces.com/api/coding/v3/chat/completions
base_url: https://ark.cn-beijing.volces.com/api/coding/v3
api_surface: chat-completions
api_key_env: VOLCENGINE_OPENAI_API_KEY
response_id: [redacted]
```

Output summary:

- Defined `因三相` as the three-part validity check for a `正因`, not as "three causes".
- Covered `遍是宗法性`, `同品定有性`, and `异品遍无性`.
- Used the example `声，应是无常，以所作性故`.
- Cited local context files `context/因明推理引擎.md` and `context/摄类学工具箱.md`.
- Stated that `同品定有性` is an existence condition in this local framework.

## Result

| Case | Result | Notes |
|---|---|---|
| ZC-02 | `pass` | The live response matched the expected concept explanation and cited the expected local context files. |

## Limitations

- This is a single-case live run for Volcengine OpenAI-compatible `chat-completions`.
- It does not validate native OpenAI API, OpenAI Responses API, or `OPENAI_API_KEY`.
- It does not validate ZC-01, ZC-03, ZC-04, ZC-05, or ZC-06 on Volcengine.
- It does not validate Agama-search tooling or file-output behavior in a live compatible-provider call.

See `docs/runtime-validation-log.md` for the corresponding validation-log entry.
