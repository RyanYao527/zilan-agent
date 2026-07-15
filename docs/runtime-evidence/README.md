# Runtime Evidence Excerpts

> Last updated: 2026-07-14

This directory stores small, redacted validation excerpts that support entries in `docs/runtime-validation-log.md`.

Use this directory for:

- command-output excerpts from clean install or CI-adjacent smoke tests
- short transcript excerpts that demonstrate a specific platform behavior
- redacted live-provider response summaries
- generated report file summaries when the full report is too large or private

Do not use this directory for:

- API keys, tokens, cookies, or account metadata
- raw provider payloads with private request IDs or account identifiers
- large unredacted transcripts
- private user content unrelated to a validation case

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
- `2026-06-18-claude-code-agama-contract-fix-review.md`
- `2026-06-18-claude-code-madhyamaka-contract-fix-review.md`
- `2026-06-18-claude-code-post-contract-full-rerun.md`
- `2026-06-18-claude-code-post-contract-target-review.md`
- `2026-07-14-claude-code-srq-04-zc-04-agama-boundary-spot-review.md`
- `2026-07-14-claude-code-zc-04-agama-boundary-rerun.md`
- `2026-07-14-claude-code-post-prompt-zc-01-zc-06-rerun.md`
- `2026-07-14-claude-code-broad-boundary-postfix-review.md`
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
- limitations
- link back to the relevant `docs/runtime-validation-log.md` entry

Use `docs/validation-evidence.md` as the governing policy.
