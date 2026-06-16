# OpenAI API Harness

> Last updated: 2026-06-16

This repository includes a minimal OpenAI / OpenAI-compatible API harness for Zilan. It loads `agents/openai.yaml`, selects a regression case from `tests/regression_cases.yaml`, bundles the expected local context files, and builds either a Responses API request or an OpenAI-compatible Chat Completions request.

The harness is dry-run by default so CI does not require secrets:

```powershell
python scripts/openai_api_harness.py --case ZC-02 --json
```

To run a live request, set `OPENAI_API_KEY` and opt in explicitly:

```powershell
$env:OPENAI_API_KEY = "..."
python scripts/openai_api_harness.py --case ZC-02 --live --json
```

Optional knobs:

```powershell
python scripts/openai_api_harness.py --case ZC-03 --model gpt-5.5 --json
python scripts/openai_api_harness.py --prompt "孜澜，什么是因三相？" --json
python scripts\openai_api_harness.py --case ZC-02 --base-url "https://api.openai.com/v1" --api-surface responses --json
```

OpenAI-compatible provider dry-run, for example a Volcengine-compatible route:

```powershell
$env:OPENAI_BASE_URL = "https://<provider-openai-compatible-base-url>/v1"
$env:OPENAI_MODEL = "<provider-model-id>"
$env:OPENAI_API_SURFACE = "chat-completions"
$env:OPENAI_API_KEY_ENV = "VOLCENGINE_OPENAI_API_KEY"
python scripts\openai_api_harness.py --case ZC-02 --json
```

Live compatible-provider run:

```powershell
$env:VOLCENGINE_OPENAI_API_KEY = "..."
python scripts\openai_api_harness.py --case ZC-02 --live --json
```

## Status

- Default mode: dry-run request construction, covered by pytest.
- Live mode: implemented, but not run by CI. Native OpenAI remains `harness-ready` until a dated `OPENAI_API_KEY` run is recorded; Volcengine-compatible ZC-02 live evidence is recorded separately under the provider route.
- Native OpenAI default: Responses API request with developer and user messages, `model`, `input`, and low reasoning effort.
- Compatible provider option: Chat Completions request with system and user messages, `model`, and `messages`.
- Credential boundary: `OPENAI_API_KEY` is required only with `--live` by default. Compatible routes can set `OPENAI_API_KEY_ENV` or `--api-key-env` to use a provider-specific environment variable.
- Status boundary: a Volcengine or other OpenAI-compatible live run must not upgrade native OpenAI API status to `tested`.

## Documentation Basis

The implementation follows OpenAI's current Responses API guidance:

- Latest model guidance names GPT-5.5 as the current latest model family: <https://developers.openai.com/api/docs/guides/latest-model.md>
- The text generation guide shows `responses.create` with `model`, `reasoning`, message-style `input`, and `response.output_text`: <https://developers.openai.com/api/docs/guides/text>
- The Responses API reference documents text `input` accepted by the create response endpoint: <https://developers.openai.com/api/docs/api-reference/responses/create.md>
- The API overview requires Bearer authentication and recommends loading API keys from server-side environment variables or key management: <https://developers.openai.com/api/docs/overview>

Compatible-provider routes may implement only part of the OpenAI API surface. Prefer `--api-surface chat-completions` unless the provider explicitly supports `POST /v1/responses`.
