# 2026-06-15 Codex v2.4.5 Runtime Rerun Evidence

| Field | Value |
|---|---|
| Date | 2026-06-15 |
| Scenario | Codex v2.4.5 runtime rerun |
| Route / provider | Codex current session with parent-observed sub-agent runs |
| Repository commit | Branch `codex/runtime-rerun-20260615`; merged as PR #20 |
| Source location | Parent-session runtime summary recorded in `docs/runtime-validation-log.md` |
| Redaction note | Full transcripts are not committed; this file preserves only agent IDs, output summaries, and non-secret file paths. |
| Runtime log entry | `docs/runtime-validation-log.md#2026-06-15-codex-v245-runtime-rerun-and-claude-code-blocker` |

## Commands Or Prompts

```text
ZC-01 through ZC-06 from CODEX_REGRESSION_TESTS.md and tests/regression_cases.yaml.
ZC-04 through ZC-06 used explicit "spawn a zilan agent" wording.
```

## Output Excerpts

```text
ZC-04 parent-observed agent ID:
019eca67-84a4-7913-a06c-b89b7b5f82bf

ZC-05 parent-observed agent ID:
019eca67-b025-7e81-a216-c1c6d24f695e

ZC-06 parent-observed agent ID:
019eca67-da7e-73b2-aa12-1804163e8878

ZC-06 file output:
C:\tmp\zilan-validation-20260615-ZC06.md
```

## Result

| Check / case | Result | Notes |
|---|---|---|
| ZC-01 through ZC-03 | `pass` | Parent session confirmed expected lightweight and cross-domain behavior after public-doc depersonalization. |
| ZC-04 through ZC-06 | `pass` | Parent-observed sub-agent completions reported local Markdown context, `_source` exclusion, citations, and boundaries. |
| Repository checks | `pass` | `ruff`, `pytest`, and repository validation passed during the recorded session. |

## Limitations

- This excerpt supports the runtime log but does not replace the full operator transcript.
- Sub-agent outputs are represented by parent-observed summaries and agent IDs, not full response bodies.
