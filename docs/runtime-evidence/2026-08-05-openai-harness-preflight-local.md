# 2026-08-05 OpenAI Harness Preflight Local Evidence

| Field | Value |
|---|---|
| Date | 2026-08-05 |
| Scenario | Local provider preflight smoke for the OpenAI / OpenAI-compatible harness |
| Route / provider | Native OpenAI API preflight and Volcengine OpenAI-compatible preflight |
| Repository commit | `9cad22796d61b500d9705d1da9a7fe70a6f321b7` before this documentation-only evidence branch |
| Source location | `scripts/openai_api_harness.py --preflight` |
| Redaction note | No API key values, bearer tokens, provider response IDs, account IDs, or request payloads were printed or committed. |
| Standalone answer excerpt | not applicable |
| Runtime log entry | not applicable; preflight-only provider/smoke evidence with no prompt, request body, provider response, or platform-status change |

## Commands Or Prompts

```powershell
python scripts\openai_api_harness.py --preflight --json
python scripts\openai_api_harness.py --provider-route volcengine_openai_compatible --preflight --json
```

No ZC prompt was run. The harness did not build a regression-case request body.

## Output Excerpts

Native OpenAI API preflight:

```json
{
  "mode": "preflight",
  "provider_route": null,
  "validation_route": "openai_api",
  "validation_status": "harness-ready",
  "validation_scope": "scripts/openai_api_harness.py builds OpenAI Responses API requests from agents/openai.yaml and regression cases; dry-run is tested, live --live execution still requires OPENAI_API_KEY evidence.",
  "model": "gpt-5.5",
  "api_surface": "responses",
  "base_url": "https://api.openai.com/v1",
  "endpoint": "https://api.openai.com/v1/responses",
  "api_key_env": "OPENAI_API_KEY",
  "api_key_present": false,
  "status_boundary": "Preflight does not call native OpenAI API and does not change platform validation status; native OpenAI remains governed by docs/platform-validation.md."
}
```

Volcengine OpenAI-compatible preflight:

```json
{
  "mode": "preflight",
  "provider_route": "volcengine_openai_compatible",
  "validation_route": "volcengine_openai_compatible",
  "validation_status": "tested",
  "validation_scope": "ZC-01 through ZC-03 live runs passed through Volcengine OpenAI-compatible chat-completions with provider route volcengine_openai_compatible, model ark-code-latest, base URL https://ark.cn-beijing.volces.com/api/coding/v3, and provider-specific VOLCENGINE_OPENAI_API_KEY. This does not validate native OpenAI API.",
  "model": "ark-code-latest",
  "api_surface": "chat-completions",
  "base_url": "https://ark.cn-beijing.volces.com/api/coding/v3",
  "endpoint": "https://ark.cn-beijing.volces.com/api/coding/v3/chat/completions",
  "api_key_env": "VOLCENGINE_OPENAI_API_KEY",
  "api_key_present": false,
  "status_boundary": "Provider-route preflight does not call the provider, does not validate native OpenAI API, and does not change platform validation status."
}
```

## Provider Preflight Output

| Field | Native OpenAI API | Volcengine OpenAI-Compatible |
|---|---|---|
| provider_route | `null` | `volcengine_openai_compatible` |
| validation_route | `openai_api` | `volcengine_openai_compatible` |
| validation_status | `harness-ready` | `tested` |
| model | `gpt-5.5` | `ark-code-latest` |
| api_surface | `responses` | `chat-completions` |
| base_url | `https://api.openai.com/v1` | `https://ark.cn-beijing.volces.com/api/coding/v3` |
| endpoint | `https://api.openai.com/v1/responses` | `https://ark.cn-beijing.volces.com/api/coding/v3/chat/completions` |
| api_key_env | `OPENAI_API_KEY` | `VOLCENGINE_OPENAI_API_KEY` |
| api_key_present | `false` | `false` |
| status_boundary | Native OpenAI remains governed by `docs/platform-validation.md`. | Provider-route preflight does not validate native OpenAI API. |

## Standalone Answer Excerpts

Not applicable. This file is not an answer excerpt and must not be used as `answer_file` input for contract or batch review.

## Result

| Check / case | Result | Notes |
|---|---|---|
| Native OpenAI preflight | `pass` | Route resolved to the Responses API endpoint. `OPENAI_API_KEY` was absent, so live validation was not attempted. |
| Volcengine-compatible preflight | `pass` | Route resolved to the configured chat-completions endpoint. `VOLCENGINE_OPENAI_API_KEY` was absent in this shell, so no live expansion was attempted. |
| Platform status | `not-run` | No change to `agents/openai.yaml` or `docs/platform-validation.md`. Native OpenAI API remains `harness-ready`; Volcengine remains `tested` only for the previously recorded ZC-01 through ZC-03 live scope. |

## Limitations

- Preflight did not call OpenAI, Volcengine, or any other provider.
- Preflight did not construct or send a ZC request body.
- `api_key_present: false` is a local shell observation only; it is not a provider failure.
- This evidence does not grade answer quality and does not promote any route to `tested`.
