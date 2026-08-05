# Runtime Evidence Excerpts

> Last updated: 2026-08-05

This directory stores small, redacted validation excerpts that support entries in `docs/runtime-validation-log.md` or preflight-only provider/smoke handoff notes.

Use [`index.md`](index.md) to find evidence by class, case ID, contract ID, and whether a file is safe to pass as `--answer-file`.

Use this directory for:

- command-output excerpts from clean install or CI-adjacent smoke tests
- provider preflight outputs that record route resolution without a live provider call
- short transcript excerpts that demonstrate a specific platform behavior
- standalone answer excerpt files for contract-reviewable runtime answers
- redacted live-provider response summaries
- generated report file summaries when the full report is too large or private

Do not use this directory for:

- API keys, tokens, cookies, or account metadata
- raw provider payloads with private request IDs or account identifiers
- large unredacted transcripts
- private user content unrelated to a validation case
- provider preflight output as an `answer_file` input
- summary-only evidence as `answer_file` input for batch or contract review

## Answer Excerpt Capture

Use a standalone answer excerpt when the committed file is intended to be reviewed with `--answer-file` or included in `scripts/reasoning_answer_review_batch.py`. The excerpt should contain the model answer text needed for the contract claim, not the human-written validation summary.

A summary-only evidence must not be used as answer_file input. Summary files can cite contract results, list missing terms, or explain limitations, but they are not mechanically equivalent to the original answer. If raw transcripts stay local, either commit a compact standalone answer excerpt or mark the evidence as summary-only.

Prefer names such as:

```text
YYYY-MM-DD-route-case-answer.md
YYYY-MM-DD-route-scenario-case-answer.md
```

## Naming

Use dated, route-specific filenames:

```text
YYYY-MM-DD-route-or-scenario.md
```

Examples:

- `2026-06-15-clean-install-smoke.md`
- `2026-06-15-mock-claude-install-smoke.md`
- `2026-06-15-codex-v245-runtime-rerun.md`
- `2026-06-16-claude-code-utf8-rerun.md`
- `2026-06-16-volcengine-openai-compatible-zc-01-zc-03-live.md`
- `2026-06-16-volcengine-openai-compatible-zc-02-live.md`
- `2026-08-05-openai-harness-preflight-local.md`
- `2026-06-18-claude-code-agama-contract-fix-review.md`
- `2026-06-18-claude-code-madhyamaka-contract-fix-review.md`
- `2026-06-18-claude-code-post-contract-full-rerun.md`
- `2026-06-18-claude-code-post-contract-target-review.md`
- `2026-07-14-claude-code-srq-04-zc-04-agama-boundary-spot-review.md`
- `2026-07-14-claude-code-zc-04-agama-boundary-rerun.md`
- `2026-07-14-claude-code-post-prompt-zc-01-zc-06-rerun.md`
- `2026-07-14-claude-code-broad-boundary-postfix-review.md`
- `2026-07-14-claude-code-zc-04-post-126-agama-slot-rerun.md`
- `2026-06-XX-openai-api-zc-02-live.md`
- `2026-06-XX-claude-code-zc-04-excerpt.md`

## Required Fields

Each evidence excerpt should include:

- date
- repository commit
- route or scenario
- command or prompt set
- redaction note
- compact output excerpts
- status boundary for provider preflight output, when applicable
- standalone answer excerpt status when the file is intended for `answer_file` review
- limitations
- link back to the relevant `docs/runtime-validation-log.md` entry, or mark the field not applicable for preflight-only provider/smoke evidence

Use `docs/validation-evidence.md` as the governing policy.
