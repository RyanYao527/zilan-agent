# Maintenance Roadmap

> Last updated: 2026-06-18

This roadmap records engineering maintenance state and next priorities for zilan-agent. It is not platform validation evidence. Platform status remains governed by `agents/openai.yaml` and `docs/platform-validation.md`.

## Current Baseline

| Area | Current state |
|---|---|
| CI | GitHub Actions runs repository invariants, generated Agama idempotency checks, pytest, ruff, and Agama search smoke tests. |
| Repository invariants | `scripts/validate_zilan_repo.py` checks required files, context files, YAML shape, regression inventory, platform status consistency, agent prompt contracts, and Agama search behavior. |
| Regression inventory | `CODEX_REGRESSION_TESTS.md` is mirrored by `tests/regression_cases.yaml`; CI validates structure, resources, and case IDs. |
| Reasoning contract | `docs/architecture/reasoning-contract.md` defines the v0 structured reasoning contract; `docs/architecture/reasoning-contract-review.md` maps current ZC evidence to `ZR-*` cases without claiming a new runtime pass; `tests/reasoning_cases.yaml` stores schema-validated seed fixtures. |
| Platform status | `agents/openai.yaml` is the machine-readable source; `docs/platform-validation.md` is the human-readable validation record. Codex is `tested`; Claude Code is `tested` as of 2026-06-16 when Windows PowerShell stdin is forced to UTF-8. |
| Runtime validation | `docs/runtime-validation-log.md` records manual runtime validation sessions and transcript availability. |
| Runtime evidence policy | `docs/validation-evidence.md` defines evidence levels, transcript redaction, and status-promotion rules. |
| Runtime evidence excerpts | `docs/runtime-evidence/` stores small redacted command-output or transcript excerpts that support validation-log entries. |
| Installation docs | `docs/installation.md` separates Codex, Claude Code, and OpenAI API operating paths. |
| Clean install smoke | A 2026-06-15 clean clone from GitHub passed repository checks, pytest, ruff, OpenAI dry-run, and Agama search smoke tests when run sequentially. |
| Mock Claude install | `scripts/mock_install_smoke.py` verifies the Claude Code skill/agent install layout in a temporary mock home without touching the real user profile. |
| OpenAI API harness | `scripts/openai_api_harness.py` builds dry-run or live Responses API requests from `agents/openai.yaml` and regression cases; live native OpenAI runs require `OPENAI_API_KEY`. |
| OpenAI-compatible harness | The same harness can target configurable OpenAI-compatible `chat-completions` endpoints such as Volcengine without upgrading native OpenAI API status; Volcengine ZC-01 through ZC-03 live validation is recorded as of 2026-06-16. |
| Provider route triage | `docs/provider-routes.md` keeps OpenAI API, DeepSeek, GLM, and Qwen route claims conservative until live evidence exists. |
| Agama search | `scripts/search_agama.py` searches Markdown only by default, filters known false positives, supports passage grouping, emits JSON, and provides stable `citation` / `passage_citation` fields. |
| Semantic retrieval fixtures | `tests/fixtures/retrieval_chunks/semantic_chunks.yaml` defines fixture-only chunks and query expectations; repository validation checks source files, line ranges, local citation anchors, reasoning roles, expected chunk IDs, non-chunk answer-boundary contracts, and checked-in answer sample references without introducing embeddings or vector storage. `SRQ-01` now includes reviewed `雜阿含經` / `長阿含經` Agama evidence chunks plus Collected Topics and Madhyamaka prasaṅga context chunks; `practice_boundary` remains a non-chunk answer boundary need. `tests/fixtures/answers/srq01-practice-boundary-pass.md` provides a tiny committed answer sample for boundary review. `scripts/semantic_retrieval_dry_run.py` returns expected chunks for query fixtures as an executable contract proof. `scripts/semantic_fixture_candidates.py` converts `search_agama.py` baseline hits into reviewable `agama_passage` candidates. `scripts/semantic_fixture_review.py` compares generated candidates with checked-in fixtures without overwriting YAML. `scripts/semantic_context_bundle.py` assembles selected chunks into prompt-ready order. `scripts/semantic_role_coverage.py` compares query `needs` with selected chunk roles. `scripts/semantic_answer_boundary_review.py` checks downstream answer text or checked-in samples against non-chunk boundary contracts. |
| Agent prompts | Codex and Claude agent prompts are checked for the Agama citation contract, activation/task merge behavior, and `search_agama.py --json` citation-field preference. |
| Release notes | `CHANGELOG.md` records project-level release changes. |

## Operating Rules

- Run `python scripts/validate_zilan_repo.py --check-generated --strict-yaml`, `python -m pytest`, and `python -m ruff check scripts tests` before merging prompt, context, script, or platform metadata changes.
- Run generated-file checks sequentially rather than in parallel with pytest; `--check-generated` may rebuild committed Agama Markdown during validation.
- Keep platform claims conservative. Do not mark a route `tested` without dated validation evidence in `docs/platform-validation.md`.
- Use local Agama Markdown as a searchable working corpus. Use `_source/` XML only for collation, source verification, or CBETA-specific checks.
- Preserve stable citation output in `search_agama.py`; downstream prompts and regression expectations depend on `citation` and `passage_citation`.
- Prefer small PRs with one maintenance theme each, and keep unrelated content or wording refactors out of engineering PRs.

## Near-Term Priorities

| Priority | Track | Work | Done when |
|---|---|---|---|
| P0 | Runtime validation | Re-run ZC-01 through ZC-06 after prompt or routing changes and append to `docs/runtime-validation-log.md`. | A dated manual validation note records prompts, observed behavior, failures, transcript status, and checks run. |
| P1 | Validation evidence | Replace summarized baselines with transcript-backed Codex and Claude Code sessions where practical. | Runtime results are auditable without relying on chat history. |
| P1 | Claude Code route | Keep the UTF-8 stdin validation protocol visible and rerun exact ZC prompts after prompt, tool, or install-path changes. | Claude Code remains `tested` only while dated evidence documents the exact prompts, encoding setup, known limits, and repository checks. |
| P1 | OpenAI API route | Run the minimal harness in live mode with `OPENAI_API_KEY` and record a dated response summary. | OpenAI API can move from `harness-ready` to `tested` only after live evidence is recorded. |
| P1 | Volcengine compatible route | Expand the 2026-06-16 ZC-01 through ZC-03 live pass to ZC-04 through ZC-06 only if broader provider-route confidence is needed. | Volcengine evidence remains separated from native OpenAI API validation, with provider/model details and limitations recorded. |
| P1 | Provider routes | Add native dry-run/live harnesses for DeepSeek, GLM, and Qwen, or record a concrete blocked state. | Each route has a dated tested or blocked entry with provider/model details and failure modes. |
| P1 | Reasoning quality | Run a post-contract runtime review for ZC-02, ZC-03, and ZC-05 against `tests/reasoning_cases.yaml`; include the ZR-03 targeted edge prompt. | Runtime review can say which `ZR-*` contract each answer satisfied, without replacing manual doctrinal review. |
| P1 | Semantic retrieval | Add a tiny negative answer-boundary sample only if the single committed `SRQ-01` pass sample proves useful for regression review. | Boundary review can compare committed pass/fail sample expectations without inline CLI answer text. |
| P1 | Agama citations | Extract or preserve finer-grained sutra or section markers when present in the Markdown. | Search output can cite representative passages beyond file, line, and fascicle where the source supports it. |
| P2 | Scholarly collation | Add a stricter collation path from Markdown hits back to CBETA XML-P5 and relevant parallels. | Publication-level work has a documented verification route. |
| P2 | Installation docs | Keep install paths and activation expectations current after platform changes. | New users can install the skill or agent without reading implementation history. |
| P2 | Release hygiene | Keep `CHANGELOG.md` updated for user-visible changes. | Changes can be summarized for users without reading merged PRs. |

## Manual Validation Checklist

Use this checklist before changing a platform route from metadata/config status to tested:

1. Record the exact date, provider, model, tool/runtime version, and repository commit.
2. Run the relevant ZC prompts from `CODEX_REGRESSION_TESTS.md` or a documented equivalent.
3. Confirm context loading, citation behavior, boundary statements, and sub-agent routing where applicable.
4. Record failures and follow-up fixes, not only successful final answers.
5. Run the repository checks listed in this document.
6. Update `agents/openai.yaml` and `docs/platform-validation.md` in the same PR.

## Backlog Guardrails

- Do not add broad abstractions unless they protect a real contract already used by prompts, scripts, tests, or documentation.
- Do not treat smoke tests as answer-quality grading. Manual runtime review remains required for agent behavior.
- Do not upgrade scholarly claims beyond the evidence in the local corpus and documented collation route.
