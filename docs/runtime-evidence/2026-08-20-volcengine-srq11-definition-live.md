# 2026-08-20 Volcengine SRQ-11 Definition Live Spot

## Scope

This note records one bounded `SRQ-11` live spot through the Volcengine OpenAI-compatible route.

It is provider-route evidence for `volcengine_openai_compatible`, not native OpenAI API evidence. It does not change
`docs/platform-validation.md`, native OpenAI API status, prompt contracts, answer contracts, or provider route metadata.

## Runtime

| Field | Value |
|---|---|
| Date | 2026-08-20 |
| Route | Volcengine OpenAI-compatible |
| Harness | `scripts/openai_api_harness.py` |
| Provider route | `volcengine_openai_compatible` |
| Model | `ark-code-latest` |
| API surface | `chat-completions` |
| Endpoint | `https://ark.cn-beijing.volces.com/api/coding/v3/chat/completions` |
| Case | `ZC-03` with direct `SRQ-11` prompt override |
| Prompt | `用摄类学检查定义：瓶的性相是能盛水者。这个定义成立吗？请直接回答，不要写入文件。` |
| Transcript status | Standalone answer excerpt committed at `docs/runtime-evidence/2026-08-20-volcengine-srq11-definition-live-answer.md` |
| Redaction note | API key value, raw request body, raw response JSON, account data, and provider response ID are not committed. |

## Commands

```powershell
python scripts\openai_api_harness.py --provider-route volcengine_openai_compatible --preflight --json
python scripts\openai_api_harness.py --provider-route volcengine_openai_compatible --case ZC-03 --prompt "用摄类学检查定义：瓶的性相是能盛水者。这个定义成立吗？请直接回答，不要写入文件。" --live --json
python scripts\semantic_answer_contract_review.py --query-id SRQ-11 --answer-file docs\runtime-evidence\2026-08-20-volcengine-srq11-definition-live-answer.md --json
python scripts\reasoning_answer_review_batch.py --batch docs\runtime-evidence\2026-08-20-volcengine-srq11-definition-live-batch.yaml
```

## Result

```text
# Reasoning Answer Review Batch

Batch: docs/runtime-evidence/2026-08-20-volcengine-srq11-definition-live-batch.yaml
Overall status: fail
Summary: pass=0, fail=1, review_needed=0, other=0

Boundary: batch fixture review only; this is not runtime platform validation.

## Reviews
- 2026-08-20-volcengine-srq11-definition-live: fail (SRQ-11)
  missing: collected_topics_definition_scope_error:违②
```

## Findings

- The Volcengine OpenAI-compatible route accepted the live request and returned an answer.
- The answer preserves most `SRQ-11` definition-boundary surfaces, including `摄类学`, `性相`, `所表`,
  `能盛水者`, `瓶`, `湖`, `性相过宽`, `唯在所表上成立`, and `不成立`.
- The answer failed the #202 pre-calibration exact-literal answer contract because it says `违三要素校验之②`
  rather than the then-required literal surface `违②`.
- No forbidden wrong-assertion term is present.

## Boundaries

- This is not native OpenAI API evidence.
- This is not a full Volcengine route rerun; it is one direct `SRQ-11` live spot.
- This is fail evidence, not runtime pass evidence.
- The answer-contract helper is a deterministic minimum explicitness check; it does not grade doctrinal quality.
- `docs/platform-validation.md` and platform tested status remain unchanged.
