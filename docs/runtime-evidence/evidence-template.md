# YYYY-MM-DD Scenario Evidence

| Field | Value |
|---|---|
| Date |  |
| Scenario |  |
| Route / provider |  |
| Repository commit |  |
| Source location |  |
| Redaction note |  |
| Standalone answer excerpt | yes / no / not applicable |
| Runtime log entry | `docs/runtime-validation-log.md#...` / not applicable for preflight-only provider/smoke evidence |

## Commands Or Prompts

```text

```

## Output Excerpts

```text

```

## Provider Preflight Output

Use this section only for local route-resolution checks such as `scripts/openai_api_harness.py --preflight`.
Record boolean key presence only; never include API key values.

| Field | Value |
|---|---|
| provider_route |  |
| validation_route |  |
| validation_status |  |
| model |  |
| api_surface |  |
| base_url |  |
| endpoint |  |
| api_key_env |  |
| api_key_present | true / false |
| status_boundary |  |

Preflight is not a live provider run, not an answer transcript, and not platform-status promotion evidence by itself.

## Standalone Answer Excerpts

Use this section when the evidence file itself is not the answer excerpt but points to one or more committed `*-answer.md` files. A summary-only evidence file must not be used as answer_file input for contract or batch review.

| Case | Answer excerpt | Reviewed against | Result |
|---|---|---|---|
|  | `docs/runtime-evidence/YYYY-MM-DD-route-case-answer.md` | `SRQ-XX` | `pass` / `partial` / `fail` |

## Result

| Check / case | Result | Notes |
|---|---|---|
|  | `pass` / `partial` / `fail` / `blocked` |  |

## Limitations

-
