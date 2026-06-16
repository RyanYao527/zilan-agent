# 2026-06-16 Volcengine OpenAI-Compatible ZC-01 And ZC-03 Live Evidence

## Summary

| Field | Value |
|---|---|
| Date | 2026-06-16 |
| Route | Volcengine OpenAI-compatible |
| Harness | `scripts/openai_api_harness.py` |
| Mode | `live` |
| Provider route | `volcengine_openai_compatible` |
| API surface | `chat-completions` |
| Model | `ark-code-latest` |
| Base URL | `https://ark.cn-beijing.volces.com/api/coding/v3` |
| Endpoint | `https://ark.cn-beijing.volces.com/api/coding/v3/chat/completions` |
| API key env | `VOLCENGINE_OPENAI_API_KEY` |
| Cases | ZC-01, ZC-03 |
| Repository base | Post-PR #26 `main` at `6913178`; evidence committed on `codex/volcengine-zc01-zc03-evidence` |
| Evidence source | User-supplied local PowerShell harness output |

## Redaction Note

- The API key value was not shared and is not committed.
- Provider response IDs are redacted.
- Full request and full response payloads are not committed because the requests embed large local context bundles and provider metadata.
- This evidence supports only the Volcengine OpenAI-compatible route, not native OpenAI API validation.

## Command Shape

```powershell
$env:VOLCENGINE_OPENAI_API_KEY = "[redacted]"
python scripts\openai_api_harness.py --case ZC-01 --provider-route volcengine_openai_compatible --live --json
python scripts\openai_api_harness.py --case ZC-03 --provider-route volcengine_openai_compatible --live --json
```

## Output Excerpts

```text
mode: live
model: ark-code-latest
provider_route: volcengine_openai_compatible
api_surface: chat-completions
base_url: https://ark.cn-beijing.volces.com/api/coding/v3
endpoint: https://ark.cn-beijing.volces.com/api/coding/v3/chat/completions
api_key_env: VOLCENGINE_OPENAI_API_KEY
response_id: [redacted]
```

### ZC-01 Output Summary

- Prompt: `孜澜，我今天收到工作反馈后心里很难受。`
- Reference files: `SKILL.md`, `context/心类学认知分析.md`, `context/南传观禅指南.md`.
- The response separated "work feedback" from "self-worth being negated".
- It described the chain `收到反馈 → 苦受 → 想心所归类为被否定 → 瞋/羞耻/委屈 → 意识补叙事`.
- It used a practical observation flow: mark bodily sensations, mark mental events, downgrade the self-negating thought to a thought, and build a fact table.
- It cited the local context files and stayed within lightweight practice support.

### ZC-03 Output Summary

- Prompt: `孜澜，用摄类学和心类学解释“收到批评后我很受挫”的认知过程。`
- Reference files: `SKILL.md`, `context/摄类学工具箱.md`, `context/心类学认知分析.md`.
- The response explicitly split the case into fact, interpretation, self-evaluation, and feeling layers.
- It used Collected Topics / Buddhist logic to reject the hidden inference `被批评 → 我无价值` as `不周遍`.
- It used the mental-factor chain `触 → 作意 → 受 → 想 → 思`.
- It included the expected concepts `概念标签`, `受`, `想`, `瞋`, and a boundary that the advice is not a substitute for therapy or clinical evaluation.

## Result

| Case | Result | Notes |
|---|---|---|
| ZC-01 | `pass` | Lightweight daily-practice support matched the expected feedback/reflection scenario and cited the expected local context files. |
| ZC-03 | `pass` | Cross-domain explanation matched the expected Collected Topics plus cognitive-analysis structure and stated boundaries. |

## Limitations

- This validates only ZC-01 and ZC-03 on the Volcengine OpenAI-compatible `chat-completions` route.
- Together with `2026-06-16-volcengine-openai-compatible-zc-02-live.md`, this covers ZC-01 through ZC-03 only.
- It does not validate native OpenAI API, OpenAI Responses API, or `OPENAI_API_KEY`.
- It does not validate ZC-04, ZC-05, ZC-06, deeper Agama-search, sub-agent routing, or file-output cases on Volcengine.

See `docs/runtime-validation-log.md` for the corresponding validation-log entry.
