# Runtime Validation Log

> Last updated: 2026-09-02

This log records manual runtime validation evidence for zilan-agent. It complements CI and repository invariant checks; it does not replace `python scripts/validate_zilan_repo.py --check-generated --strict-yaml`, pytest, ruff, or platform status maintenance in `agents/openai.yaml` and `docs/platform-validation.md`.

## Evidence Rules

Every runtime validation entry should record:

- exact date
- runtime or provider
- model or tool version when known
- repository commit or branch
- prompt set used
- case-level result
- observed failures or limitations
- repository checks run after the session
- whether full transcripts are committed, summarized, or unavailable

Use conservative status labels:

| Status | Meaning |
|---|---|
| `pass` | The case met its documented expected behavior in the observed runtime. |
| `partial` | The case mostly worked but had a material gap that should be tracked. |
| `fail` | The case did not meet expected behavior. |
| `blocked` | The case could not be executed because of missing access, tooling, or provider failure. |
| `not-run` | The case remains in scope but was not executed in this session. |

## 2026-09-02 SRQ-04 Citation Anchor / Section Refinement

| Field | Value |
|---|---|
| Runtime | None; local citation/coverage refinement only |
| Provider / model | None |
| Tool version | `scripts/srq_coverage_report.py` and committed CBETA XML-P5 fixture probes |
| Repository commit | after the 2026-09-01 `SRQ-04` reviewer decision ingestion path |
| Prompt set | No prompt execution |
| Transcript status | No answer excerpt. Summary-only citation refinement note committed at `docs/runtime-evidence/2026-09-02-srq04-citation-anchor-section-refinement.md`. |
| Repository checks | The SRQ/ZR coverage report now exposes per-chunk citation anchor details for Agama chunks, including `section_label_status`, `xml_anchor_status`, `anchor_probe_id`, manual boundary status, and candidate-set IDs. |
| Overall result | `manual_review_required`: `agama:T01n0001:juan-3:line-1829` is XML-anchor-located at `T01.0001.0021a` / `0021a18`, but no stable source-derived section label is available. Textual equivalence, source dependence, publication-ready collation, runtime answer pass, and platform validation claims remain unproven. |

### Known Limits

- This is not a runtime run, provider call, local replay, or answer-contract pass.
- This does not modify the candidate map conclusions or the pending reviewer-decision fixture rows.
- `docs/platform-validation.md` and platform tested status remain unchanged.

## 2026-09-01 SRQ-04 Reviewer Decision Ingestion Path

| Field | Value |
|---|---|
| Runtime | None; local reviewer-decision ingestion path only |
| Provider / model | None |
| Tool version | `scripts/srq04_manual_review_packet.py` and `scripts/validate_zilan_repo.py` |
| Repository commit | after the 2026-09-01 `SRQ-04` reviewer decision guard |
| Prompt set | No prompt execution |
| Transcript status | No answer excerpt. Summary-only ingestion-path note committed at `docs/runtime-evidence/2026-09-01-srq04-reviewer-decision-ingestion-path.md`. |
| Repository checks | The packet exposes machine-readable ingestion rules. The collation validator requires dated `docs/runtime-evidence/YYYY-MM-DD-*.md` notes for non-pending reviewer decisions. |
| Overall result | `manual_review_required`: no new human reviewer conclusion was supplied. All three current `SRQ-04` candidate sets remain pending in the reviewer-decision fixture, and textual equivalence, source dependence, publication-ready collation, runtime answer pass, and platform validation claims remain unproven. |

### Known Limits

- This is not a runtime run, provider call, local replay, or answer-contract pass.
- This does not modify the candidate map conclusions.
- `docs/platform-validation.md` and platform tested status remain unchanged.

## 2026-08-21 SRQ-04 Reviewer Decision Intake

| Field | Value |
|---|---|
| Runtime | None; local reviewer-decision intake only |
| Provider / model | None |
| Tool version | `scripts/validate_zilan_repo.py`, `scripts/cbeta_collation_preflight.py`, and `scripts/srq_coverage_report.py` |
| Repository commit | after the 2026-08-20 `SRQ-04` manual semantic-boundary queue |
| Prompt set | No prompt execution |
| Transcript status | No answer excerpt. Summary-only intake note committed at `docs/runtime-evidence/2026-08-21-srq04-reviewer-decision-intake.md`. |
| Repository checks | The collation validator checks `tests/fixtures/collation/srq04_manual_semantic_boundary_decisions.yaml` when present. |
| Overall result | `manual_review_required`: the repository now has a structured place for future human reviewer decisions, but all three current `SRQ-04` candidate sets remain pending and conservative. Textual equivalence, source dependence, publication-ready collation, runtime answer pass, and platform validation claims remain unproven. |

### Known Limits

- This is not a runtime run, provider call, local replay, or answer-contract pass.
- This does not modify the candidate map conclusions.
- `docs/platform-validation.md` and platform tested status remain unchanged.

## 2026-08-20 SRQ-04 Manual Semantic-Boundary Queue

| Field | Value |
|---|---|
| Runtime | None; local evidence queue only |
| Provider / model | None |
| Tool version | `scripts/cbeta_collation_preflight.py` and `scripts/srq_coverage_report.py` |
| Repository commit | after the 2026-08-20 `SRQ-11` definition-violation alias replay merge |
| Prompt set | No prompt execution |
| Transcript status | No answer excerpt. Reviewer queue note committed at `docs/runtime-evidence/2026-08-20-srq04-manual-semantic-boundary-queue.md`. |
| Repository checks | CBETA XML-P5 anchor preflight and SRQ/ZR coverage report should continue to show `SRQ-04` as the only `manual_review_required` case. |
| Overall result | `manual_review_required`: the three existing `SRQ-04` XML-P5 candidate sets remain anchor-located and limited theme-parallel evidence only. Textual equivalence, source dependence, publication-ready collation, runtime answer pass, and platform validation claims remain unproven. |

### Queue Items

| Candidate set | Current boundary | Reviewer task |
|---|---|---|
| `no-self-five-aggregates-and-feeling` | limited theme parallel | Decide whether any evidence supports textual equivalence, source dependence, or publication-ready collation beyond the current theme-parallel note. |
| `long-agama-no-self-verse-and-aggregates` | limited theme parallel | Decide whether the two Long Agama verse contexts remain representative no-self parallels only. |
| `za-agama-and-long-agama-no-self-verse` | limited cross-Agama theme parallel | Decide whether the cross-Agama relation remains representative no-self evidence only. |

### Known Limits

- This is not a runtime run, provider call, local replay, or answer-contract pass.
- This does not modify the candidate map conclusions.
- `docs/platform-validation.md` and platform tested status remain unchanged.

## 2026-08-20 SRQ-11 Definition Violation Alias Replay

| Field | Value |
|---|---|
| Runtime | Local answer-contract replay |
| Provider / model | Reuses the already committed Volcengine OpenAI-compatible `ark-code-latest` answer excerpt; no new provider call |
| Tool version | `scripts/semantic_answer_contract_review.py` and `scripts/reasoning_answer_review_batch.py` |
| Repository commit | after the 2026-08-20 Volcengine `SRQ-11` live spot evidence merge |
| Prompt set | No prompt execution; replay over `docs/runtime-evidence/2026-08-20-volcengine-srq11-definition-live-answer.md` |
| Transcript status | No new transcript. The original answer excerpt is unchanged; replay note is committed at `docs/runtime-evidence/2026-08-20-srq11-definition-violation-alias-replay.md`. |
| Repository checks | Direct `SRQ-11` answer-contract review and batch replay should pass under the calibrated exact `definition_violation_marker` group accepting `违②` or `违三要素校验之②`. |
| Overall result | `pass`: local calibrated replay passes for `SRQ-11`. The original #202 Volcengine live note remains historical pre-calibration exact-contract fail evidence. This is not native OpenAI API evidence and does not change platform status. |

### Contract Results

| Answer excerpt | Reviewed as | Result | Notes |
|---|---|---:|---|
| `2026-08-20-volcengine-srq11-definition-live-answer.md` | `SRQ-11` / `collected_topics_definition_scope_error` | `pass` | The answer matches `definition_violation_marker` through exact surface `违三要素校验之②`; prompt contracts still require generated answers to preserve literal `违②`. |

### Known Limits

- This is local replay over a committed answer excerpt, not a new runtime run.
- This does not modify prompt contracts, provider route metadata, native OpenAI API status, or platform validation status.
- The answer-contract helper remains a deterministic minimum explicitness check, not a doctrinal judge.

## 2026-08-20 Volcengine OpenAI-Compatible SRQ-11 Definition Live Spot

| Field | Value |
|---|---|
| Runtime | OpenAI-compatible harness |
| Provider / model | Volcengine OpenAI-compatible route, `ark-code-latest` |
| Tool version | `scripts/openai_api_harness.py` live mode with `--provider-route volcengine_openai_compatible` |
| Repository commit | post-`SRQ-04` manual collation boundary closeout on `main` |
| Prompt set | Direct `SRQ-11` prompt override on `ZC-03`: `用摄类学检查定义：瓶的性相是能盛水者。这个定义成立吗？请直接回答，不要写入文件。` |
| Transcript status | Standalone answer excerpt committed at `docs/runtime-evidence/2026-08-20-volcengine-srq11-definition-live-answer.md`; compact summary at `docs/runtime-evidence/2026-08-20-volcengine-srq11-definition-live.md`; raw request JSON, provider response ID, API key value, and private account data are not committed. |
| Repository checks | #202 direct `SRQ-11` answer-contract review and batch review both reported fail on missing literal `违②` under the pre-calibration exact-literal contract; broader repository checks ran before PR handoff. |
| Overall result | `target-fail`: the Volcengine OpenAI-compatible route returned an answer, but the #202 pre-calibration exact-literal `SRQ-11` answer contract failed. This is not native OpenAI API evidence and does not change platform status. |

### Contract Results

| Answer excerpt | Reviewed as | Result | Notes |
|---|---|---:|---|
| `2026-08-20-volcengine-srq11-definition-live-answer.md` | `SRQ-11` / `collected_topics_definition_scope_error` | `fail` | #202 pre-calibration review found required definition-boundary surfaces mostly present, but the answer says `违三要素校验之②` rather than the then-required exact literal `违②`; no forbidden wrong-assertion term is present. |

### Known Limits

- This is one direct `SRQ-11` live spot, not a full Volcengine route rerun.
- This evidence validates neither native OpenAI API nor the local Claude Code custom route.
- The answer-contract helper is a deterministic minimum explicitness check, not a doctrinal judge.
- `docs/platform-validation.md` and platform tested status remain unchanged.

## 2026-08-19 Claude Code SRQ-06 / SRQ-07 / SRQ-10 / SRQ-11 Runtime Spot Review

| Field | Value |
|---|---|
| Runtime | Claude Code CLI |
| Provider / model | Claude Code `2.1.234`; the local configuration printed an `unrecognized_model` diagnostic for `deepseek-v4-pro[1m]` before returning answer text. This is Claude Code route evidence, not native DeepSeek, native OpenAI API, or OpenAI-compatible provider validation. |
| Tool version | `claude -p` noninteractive mode with `agents/zilan-claude-code.md` appended as the system prompt |
| Repository base | `8037b95` (`Add SRQ evidence coverage and productization triage`) |
| Branch | `codex/srq-evidence-closeout` |
| Prompt set | Direct `SRQ-06`, `SRQ-07`, `SRQ-10`, and `SRQ-11` prompts from `tests/fixtures/retrieval_chunks/semantic_chunks.yaml`, each with `请直接回答，不要写入文件。` |
| Encoding setup | Windows PowerShell UTF-8 stdout and console encoding were set before invoking `claude -p`. |
| Transcript status | Standalone answer excerpts committed at `docs/runtime-evidence/2026-08-19-claude-code-srq-06-runtime-spot-answer.md`, `docs/runtime-evidence/2026-08-19-claude-code-srq-07-runtime-spot-answer.md`, `docs/runtime-evidence/2026-08-19-claude-code-srq-10-runtime-spot-answer.md`, and `docs/runtime-evidence/2026-08-19-claude-code-srq-11-runtime-spot-answer.md`; compact review committed at `docs/runtime-evidence/2026-08-19-srq06-srq07-srq10-srq11-runtime-spot-review.md`. |
| Repository checks | PR #193 recorded a pre-calibration strict-literal fail for all four cases. Current calibrated replay of the same batch returns `pass=3`, `fail=1`; the focused `SRQ-06` / `SRQ-07` replay batch returns `pass=2`, `fail=0`; the focused `SRQ-10` replay batch returns `pass=1`, `fail=0`; the focused `SRQ-11` collision replay batch returns `pass=0`, `fail=1`. |
| Overall result | `target-partial`: the committed `SRQ-06` / `SRQ-07` / `SRQ-10` runtime answer excerpts pass the current exact alias-group contracts; `SRQ-11` still fails after the shallow heading collision is cleared. No platform-status change. |

### Contract Results

| Answer excerpt | Reviewed as | Result | Notes |
|---|---|---|---|
| `2026-08-19-claude-code-srq-06-runtime-spot-answer.md` | `SRQ-06` | `pass` | Current calibrated replay accepts exact alias `无法决定` for the indeterminate-resolution slot; the original #193 strict-literal note recorded missing `不能决定`. |
| `2026-08-19-claude-code-srq-07-runtime-spot-answer.md` | `SRQ-07` | `pass` | Current calibrated replay accepts exact alias `总与别` for the Collected Topics surface slot; the original #193 strict-literal note recorded missing `摄类学`. |
| `2026-08-19-claude-code-srq-10-runtime-spot-answer.md` | `SRQ-10` | `pass` | Current calibrated replay accepts exact aliases for attribution-error, motive-inference, affliction, and non-harm surfaces; the original #193 strict-literal note recorded missing explicit cognitive and corrective-factor terms. |
| `2026-08-19-claude-code-srq-11-runtime-spot-answer.md` | `SRQ-11` | `fail` | Current calibrated replay no longer treats the heading `性相成立的标准` as a forbidden wrong assertion, but the answer still misses `性相过宽`, `唯在所表上成立`, `违②`, and `definiendum_boundary`. |

### Known Limits

- This is a targeted SRQ runtime spot review, not a full platform rerun.
- It records pass evidence for the committed `SRQ-06` / `SRQ-07` answer excerpts under the current calibrated contract,
  plus pass evidence for the committed `SRQ-10` excerpt under the current calibrated contract, while preserving
  explicit `SRQ-11` fail evidence after the shallow forbidden collision is cleared.
- The contract misses are deterministic exact-string / slot-surface results, not full doctrinal quality judgments.
- `docs/platform-validation.md` and platform tested status remain unchanged.

## 2026-08-10 Claude Code ZC-05 Broad Runtime Rerun

| Field | Value |
|---|---|
| Runtime | Claude Code CLI |
| Provider / model | Claude Code `2.1.220`; local JSON model usage reported `deepseek-v4-pro[1m]` under the user's Claude Code configuration. This is Claude Code route evidence, not native OpenAI API or OpenAI-compatible provider validation. |
| Tool version | `claude -p` noninteractive mode with `agents/zilan-claude-code.md` loaded as the system prompt |
| Repository base | `398edd2` (`Add CBETA XML anchor probes and candidate map (#189)`) |
| Branch | `codex/broad-zc05-runtime-rerun` |
| Prompt set | One broad `ZC-05` cross-domain prompt: `请 spawn 一个 zilan agent，用应成论式分析诸法无我，并串联阿含、摄类学、因明和观禅。` |
| Encoding setup | Windows PowerShell UTF-8 stdout, console, and stdin were set before piping the Chinese prompt into `claude -p`. |
| Transcript status | Standalone answer excerpt committed at `docs/runtime-evidence/2026-08-10-claude-code-zc-05-broad-runtime-rerun-answer.md`; compact review committed at `docs/runtime-evidence/2026-08-10-zc-05-broad-runtime-rerun.md`; raw JSON and extracted local Markdown stayed outside the repository under `C:\tmp\zilan-zc05-runtime-rerun-20260810`. |
| Repository checks | `python scripts\reasoning_answer_review_batch.py --batch docs\runtime-evidence\2026-08-10-zc-05-broad-runtime-rerun-batch.yaml` passed; full maintenance baseline run before PR handoff. |
| Overall result | `target-pass`: the broad `ZC-05` answer passes `SRQ-01`, `SRQ-03`, `SRQ-04`, and `SRQ-08`; no platform-status change. |

### Contract Results

| Answer excerpt | Reviewed as | Result | Notes |
|---|---|---|---|
| `2026-08-10-claude-code-zc-05-broad-runtime-rerun-answer.md` | `SRQ-01` | `pass` | Integrated no-self surfaces are present: Agama evidence, representative retrieval framing, Hetuvidya check, `我所`, cognitive terms, and the non-attainment boundary. |
| `2026-08-10-claude-code-zc-05-broad-runtime-rerun-answer.md` | `SRQ-03` | `pass` | The answer explicitly preserves `不立自宗`, `二谛`, and `proposition_decomposition` surfaces. |
| `2026-08-10-claude-code-zc-05-broad-runtime-rerun-answer.md` | `SRQ-04` | `pass` | The answer includes local Agama citation anchors and marks the evidence as representative rather than exhaustive. |
| `2026-08-10-claude-code-zc-05-broad-runtime-rerun-answer.md` | `SRQ-08` | `pass` | The answer keeps a nihilism boundary and avoids treating emptiness/no-self analysis as annihilationism. |

### Known Limits

- This is a targeted broad `ZC-05` runtime spot rerun, not a full platform rerun.
- It validates the observed Claude Code route under the local user configuration; it does not validate native OpenAI API or OpenAI-compatible provider routes.
- The answer-contract helper is a deterministic local review aid. Passing it is evidence for required answer surfaces, not a substitute for full scholarly or practice review.
- `docs/platform-validation.md` and platform tested status remain unchanged.

## 2026-06-10 Codex Baseline

| Field | Value |
|---|---|
| Runtime | Codex |
| Scope | ZC-01 through ZC-06 from `CODEX_REGRESSION_TESTS.md` |
| Evidence source | Existing project validation notes in `agents/openai.yaml` and `docs/platform-validation.md` |
| Repository context | Local Markdown context and explicit sub-agent triggers for ZC-04 through ZC-06 |
| Transcript status | Full transcripts are not committed in this repository. Treat this entry as a summarized baseline, not a transcript archive. |
| Follow-up | Re-run and append a transcript-backed entry after meaningful prompt, routing, or context changes. |

### Case Results

| Case | Mode | Result | Notes |
|---|---|---|---|
| ZC-01 | Skill lightweight dialogue | `pass` | Lightweight daily-practice support; no sub-agent expected. |
| ZC-02 | Skill concept lookup | `pass` | Expected to use or follow `context/因明推理引擎.md`. |
| ZC-03 | Skill cross-domain explanation | `pass` | Expected to combine `context/摄类学工具箱.md` and `context/心类学认知分析.md`. |
| ZC-04 | Explicit sub-agent Agama search | `pass` | Explicit sub-agent trigger; Agama Markdown search expected, with `_source/` excluded. |
| ZC-05 | Explicit sub-agent cross-domain research | `pass` | Explicit sub-agent trigger; expected to connect Agama, Collected Topics, Buddhist logic, Madhyamaka, and vipassana. |
| ZC-06 | Long report output | `pass` | Explicit sub-agent trigger; file output expected only because the prompt requested it. |

### Known Limits

- This entry is a summarized baseline. It does not contain full model transcripts.
- CI validates case inventory, prompt contracts, search behavior, and repository invariants; it does not grade answer quality.
- Future prompt or routing changes should append a new entry rather than editing this historical baseline in place.

## 2026-06-12 Codex Rerun

| Field | Value |
|---|---|
| Runtime | Codex |
| Provider / model | Codex current session; exact model ID not recorded in repository evidence |
| Tool version | Codex session with `multi_agent_v1.spawn_agent` and `multi_agent_v1.wait_agent` available |
| Repository commit | `8079c1b7a455cb60e2c6560577c45d452f53b6f4` |
| Branch | `codex/runtime-validation-rerun-20260612` |
| Prompt set | ZC-01 through ZC-06 from `CODEX_REGRESSION_TESTS.md` and `tests/regression_cases.yaml` |
| Transcript status | Summarized here; full transcripts are not committed. Parent session recorded sub-agent IDs for ZC-04 through ZC-06. ZC-06 also wrote a report to `C:\tmp\zilan-validation-20260612-ZC06.md`, outside the repository. |
| Repository checks | `python -m ruff check scripts tests` pass; `python -m pytest` pass; `python scripts\validate_zilan_repo.py --check-generated --strict-yaml` pass |
| Overall result | `pass` with the limitations below |

### Case Results

| Case | Mode | Result | Notes |
|---|---|---|---|
| ZC-01 | Skill lightweight dialogue | `pass` | Main Codex session, no sub-agent. Covered daily-practice support with psychology / vipassana framing, avoided scripture overreach, and stated practice boundaries. |
| ZC-02 | Skill concept lookup | `pass` | Main Codex session, no sub-agent. Explained the three characteristics of a valid reason: `遍是宗法性`, `同品定有性`, and `异品遍无性`, with the expected Collected Topics relation. |
| ZC-03 | Skill cross-domain explanation | `pass` | Main Codex session, no sub-agent. Combined Collected Topics and Buddhist psychology, distinguishing fact, concept label, feeling / perception, and anger, with a practice boundary. |
| ZC-04 | Explicit sub-agent Agama search | `pass` | Spawned sub-agent `019eba77-1d09-79e1-b853-ada7ab3ff31c` (`Popper`). It searched local Agama Markdown, excluded `_source/` XML, reported 282 script matches, grouped the evidence into six doctrinal categories, supplied CBETA / fascicle / local-line citations, and stated search limits. |
| ZC-05 | Explicit sub-agent cross-domain research | `pass` | Spawned sub-agent `019eba77-5d1a-7032-9bec-2d71c2715f9b` (`Russell`). It connected Agama, Collected Topics, Buddhist logic, Madhyamaka, and vipassana, supplied local citations, and stated practice and textual inference boundaries. |
| ZC-06 | Long report output | `pass` | Spawned sub-agent `019eba77-7e15-7992-886b-4a9b9b866a25` (`Raman`). It wrote `C:\tmp\zilan-validation-20260612-ZC06.md`, searched local Agama Markdown with `_source/` excluded, reported passage counts by corpus, produced a long report with citations, and stated non-exhaustive / non-practice-certification boundaries. |

### Sub-Agent Evidence

| Case | Parent-observed agent ID | Evidence |
|---|---|---|
| ZC-04 | `019eba77-1d09-79e1-b853-ada7ab3ff31c` | Completion notification returned the Agama search summary, search commands, match counts, representative citations, and boundary statement. |
| ZC-05 | `019eba77-5d1a-7032-9bec-2d71c2715f9b` | Completion notification returned the cross-domain doctrinal answer, representative citations, and boundary statement. |
| ZC-06 | `019eba77-7e15-7992-886b-4a9b9b866a25` | Completion notification confirmed file output at `C:\tmp\zilan-validation-20260612-ZC06.md`; the file was read and summarized for this log. |

### Known Limits

- Full prompts and answer transcripts are summarized, not committed verbatim.
- Sub-agents cannot self-observe the parent session's spawn handle, so their self-reports mark sub-agent verification as partial. Parent-observed agent IDs are the runtime evidence for ZC-04 through ZC-06.
- ZC-04 surfaced residual false positives such as non-doctrinal `無我` contexts that require manual screening after keyword search.
- One shell attempt to read a local installed skill path failed under the Windows sandbox. The rerun used the repository-local `SKILL.md`, agent prompt, and context files successfully.

## 2026-06-12 Claude Code Rerun

| Field | Value |
|---|---|
| Runtime | Claude Code CLI |
| Provider / model | Claude Code 2.1.169; JSON model usage reported `deepseek-v4-pro[1m]` under the local Claude Code configuration |
| Tool version | `claude -p` noninteractive mode with `agents/zilan-claude-code.md` appended as the agent prompt |
| Repository commit | `1cae652fec50132e69c526113ba644dfeba21cbf` |
| Branch | `codex/claude-openai-validation` |
| Prompt set | ZC-01 through ZC-06 from `CODEX_REGRESSION_TESTS.md` and `tests/regression_cases.yaml` |
| Transcript status | Summarized here; full JSON outputs are not committed. ZC-06 also wrote a report to `C:\tmp\zilan-claude-validation-20260612-ZC06.md`, outside the repository. |
| Repository checks | `python -m ruff check scripts tests` pass; `python -m pytest` pass; `python scripts\validate_zilan_repo.py --check-generated --strict-yaml` pass |
| Overall result | `pass` with the limitations below |

### Case Results

| Case | Mode | Result | Notes |
|---|---|---|---|
| ZC-01 | Skill lightweight dialogue | `pass` | Claude Code session `edbefc6f-5344-48f8-b4c8-8e47c9f25ab4`; used `Read` for `摄类学工具箱.md`, `心类学认知分析.md`, and `南传观禅指南.md`; no `Bash` or `Write`; boundary statement present. |
| ZC-02 | Skill concept lookup | `pass` | Session `c5e3599d-d54d-4666-b27f-4f62fc8aa285`; used `Read` for `因明推理引擎.md` and `摄类学工具箱.md`; explained `遍是宗法性`, `同品定有性`, and `异品遍无性`; boundary statement present. |
| ZC-03 | Skill cross-domain explanation | `pass` | Session `a51d0a1c-fb53-4600-872e-201821b02461`; used `Read` for `摄类学工具箱.md` and `心类学认知分析.md`; distinguished fact, concept label, `受`, `想`, and `瞋`; boundary statement present. |
| ZC-04 | Explicit agent Agama search | `pass` | Initial session `2e25ea9e-761c-4371-b658-e10c29f47b6f` completed classification but looked for `~/.claude/skills/zilan-agent/scripts/search_agama.py`, which was not installed locally. Rerun session `6a7da561-6c7a-4ba0-8e8d-1e2f66c43629` used the explicit repository root and `scripts/search_agama.py --json`; local Markdown only; boundary statement present. |
| ZC-05 | Explicit agent cross-domain research | `pass` | Session `13d6aac6-0594-4277-8431-ccaf4bfa057d`; used `Read` and `Bash`; connected Agama, Collected Topics, Buddhist logic, Madhyamaka, and vipassana; supplied local citations and practice / textual boundaries. |
| ZC-06 | Long report output | `pass` | Session `7e4c7b98-e351-4abd-ae8e-03ac3b3455bb`; used `Read`, `Bash`, and `Write`; wrote `C:\tmp\zilan-claude-validation-20260612-ZC06.md`; independent file check found 352 lines; repository worktree remained clean. |

### Known Limits

- This validates Claude Code CLI noninteractive execution with the repository agent prompt loaded directly. It does not independently prove every user's installed `~/.claude/skills/zilan-agent` path is current.
- Background auto-spawn behavior was not separately audited; explicit ZC-04 through ZC-06 prompts were executed through the loaded agent prompt in `claude -p`.
- Full JSON transcripts are summarized, not committed verbatim.
- The first ZC-04 run exposed an installation-path gap: `~/.claude/agents/zilan.md` existed locally, but `~/.claude/skills/zilan-agent/scripts/search_agama.py` did not. The repository prompt now prefers current-repo `scripts/` when available.

## 2026-06-12 OpenAI API Harness Dry Run

| Field | Value |
|---|---|
| Runtime | OpenAI API harness |
| Provider / model | OpenAI Responses API request model `gpt-5.5` |
| Tool version | `scripts/openai_api_harness.py` dry-run mode |
| Repository branch | `codex/claude-openai-validation` |
| Prompt set | Harness dry-run for ZC-02 / ZC-03 request construction from `tests/regression_cases.yaml` |
| Transcript status | Dry-run request construction only; no live OpenAI response transcript is recorded. |
| Repository checks | `python -m ruff check scripts tests` pass; `python -m pytest` pass; `python scripts\validate_zilan_repo.py --check-generated --strict-yaml` pass |
| Overall result | `partial`: harness-ready, live provider execution not yet tested |

### Observations

- The harness loads `agents/openai.yaml`, regression case prompts, and bounded local context files.
- Dry-run mode does not require `OPENAI_API_KEY` and is covered by `tests/test_openai_api_harness.py`.
- Live mode is implemented behind `--live` and fails fast unless `OPENAI_API_KEY` is present.
- OpenAI API should remain `harness-ready`, not `tested`, until a dated live run is recorded.

## 2026-06-15 Clean Install Smoke

| Field | Value |
|---|---|
| Runtime | Clean repository install smoke |
| Source | Fresh clone from `https://github.com/RyanYao527/zilan-agent.git` |
| Local path | `C:\tmp\zilan-clean-install-20260615` |
| Repository commit | `7033ff1b7a46f626856a13799a0f2f65bd304838` |
| Scope | Installation and engineering checks from `docs/installation.md` |
| Transcript status | Command outputs summarized here and excerpted in `docs/runtime-evidence/2026-06-15-clean-install-smoke.md`; no model transcript involved. |
| Overall result | `pass` |

### Checks

| Check | Result | Notes |
|---|---|---|
| `python scripts\validate_zilan_repo.py --check-generated --strict-yaml` | `pass` | Generated Agama files remained clean after validation. |
| `python -m pytest` | `pass` | 15 tests passed after generated-file validation completed. |
| `python -m ruff check scripts tests` | `pass` | No lint findings. |
| `python scripts\openai_api_harness.py --case ZC-02` | `pass` | Dry-run only; model `gpt-5.5`; no live API call. |
| `python scripts\search_agama.py --terms "無我|非我|緣起" --limit 5` | `pass` | Returned five local Markdown matches with stable citations. |

### Observation

An initial operator attempt ran `validate_zilan_repo.py --check-generated` in parallel with pytest. Because the validation command may rebuild generated Agama Markdown, this can create a transient read/write race for tests that inspect generated files. The valid clean-install protocol is to run generated-file validation sequentially before pytest.

## 2026-06-15 Mock Claude Install Smoke

| Field | Value |
|---|---|
| Runtime | Mock Claude Code install smoke |
| Tool | `scripts/mock_install_smoke.py` |
| Repository commit | `a9121d21ae376533a837a450fb487012bcaa3401` |
| Scope | Simulated `.claude/skills/zilan-agent` and `.claude/agents/zilan.md` install paths in a temporary mock home |
| Transcript status | Command output summarized here and excerpted in `docs/runtime-evidence/2026-06-15-mock-claude-install-smoke.md`; no model transcript involved. |
| Overall result | `pass` |

### Checks

| Check | Result | Notes |
|---|---|---|
| Mock skill copy | `pass` | Copied the repository into a temporary `.claude/skills/zilan-agent` path. |
| Mock agent install | `pass` | Installed `agents/zilan-claude-code.md` as temporary `.claude/agents/zilan.md`. |
| Required skill paths | `pass` | Confirmed `SKILL.md`, `scripts/search_agama.py`, `scripts/build_agama_context.py`, key context files, and Agama index files. |
| Agent prompt fragments | `pass` | Confirmed `name: zilan`, `tools:`, `search_agama.py`, and `context/` fragments. |
| Installed Agama search | `pass` | The copied skill's `scripts/search_agama.py --terms "緣起" --limit 1` returned a local Markdown citation. |

### Boundary

This validates installation layout and helper availability only. It does not run Claude Code or validate answer quality.

## 2026-06-15 Codex v2.4.5 Runtime Rerun And Claude Code Blocker

| Field | Value |
|---|---|
| Runtime | Codex current session; Claude Code CLI control attempts |
| Provider / model | Codex current session for ZC validation; Claude Code 2.1.169 reported local `deepseek-v4-pro[1m]` usage |
| Tool version | Codex sub-agent tools available; Claude Code `claude -p` noninteractive mode |
| Repository branch | `codex/runtime-rerun-20260615` |
| Repository base commit | `6988f7b6a24fbe92e1175de2bca7043afa5bdd05` plus activation/task prompt-guard changes in this branch |
| Prompt set | ZC-01 through ZC-06 from `CODEX_REGRESSION_TESTS.md` and `tests/regression_cases.yaml` after v2.4.5 public-doc depersonalization |
| Transcript status | Summarized here; full transcripts are not committed. A compact evidence excerpt is committed at `docs/runtime-evidence/2026-06-15-codex-v245-runtime-rerun.md`. ZC-06 wrote `C:\tmp\zilan-validation-20260615-ZC06.md` outside the repository. |
| Repository checks | `python -m ruff check scripts tests` pass; `python -m pytest` pass; `python scripts\validate_zilan_repo.py --check-generated --strict-yaml` pass |
| Overall result | Codex `pass`; Claude Code `blocked` for exact wake-word prompts |

### Codex Case Results

| Case | Mode | Result | Notes |
|---|---|---|---|
| ZC-01 | Skill lightweight dialogue | `pass` | Parent-session review confirmed the v2.4.5 neutral `工作反馈` prompt is covered by `SKILL.md`, `context/心类学认知分析.md`, and `context/南传观禅指南.md`; expected boundary behavior remains present. |
| ZC-02 | Skill concept lookup | `pass` | Parent-session review confirmed `context/因明推理引擎.md` and `context/摄类学工具箱.md` cover `遍是宗法性`, `同品定有性`, and `异品遍无性`. |
| ZC-03 | Skill cross-domain explanation | `pass` | Parent-session review confirmed the neutral `收到批评后我很受挫` prompt is supported by the Collected Topics and cognitive-analysis context, including fact / concept-label / `受` / `想` / `瞋` distinctions. |
| ZC-04 | Explicit sub-agent Agama search | `pass` | Spawned sub-agent `019eca67-84a4-7913-a06c-b89b7b5f82bf` (`Ptolemy`). It used repository-local `agents/zilan-codex.md`, `context/agama/agama-index.md`, and `scripts/search_agama.py`; searched Markdown only; excluded `_source`; returned distribution counts and representative citations. |
| ZC-05 | Explicit sub-agent cross-domain research | `pass` | Spawned sub-agent `019eca67-b025-7e81-a216-c1c6d24f695e` (`Schrodinger`). It loaded Agama, Collected Topics, Buddhist logic, Madhyamaka, vipassana, and cognitive-analysis context; supplied stable local citations and practice / textual boundaries. |
| ZC-06 | Long report output | `pass` | Spawned sub-agent `019eca67-da7e-73b2-aa12-1804163e8878` (`Curie`). It wrote `C:\tmp\zilan-validation-20260615-ZC06.md`; the file exists and includes search strategy, hit distribution, classification table, representative citations, analysis, boundary statements, and collation TODOs. |

### Codex Sub-Agent Evidence

| Case | Parent-observed agent ID | Evidence |
|---|---|---|
| ZC-04 | `019eca67-84a4-7913-a06c-b89b7b5f82bf` | Completion notification reported Markdown-only Agama search, `_source` exclusion, hit distribution (`雜阿含` 273 lines, `增壹阿含` 64, `中阿含` 55, `長阿含` 25), preliminary categories, and citations such as `context/agama/T0099-za-agama.md:147`. |
| ZC-05 | `019eca67-b025-7e81-a216-c1c6d24f695e` | Completion notification reported local context loading, `search_agama.py` / `rg` use, reasoning chain through Agama + 摄类学 + 因明 + 中观 + 观禅, and representative citations including `context/agama/T0099-za-agama.md:147` and `context/agama/T0026-zhong-agama.md:2227`. |
| ZC-06 | `019eca67-da7e-73b2-aa12-1804163e8878` | Completion notification confirmed file output at `C:\tmp\zilan-validation-20260615-ZC06.md`; local file check confirmed the report begins with search scope and excludes `_source` XML. |

### Claude Code Control Attempts

| Attempt | Result | Notes |
|---|---|---|
| `claude -p` with `--append-system-prompt` or `--system-prompt` and positional exact ZC-02 prompt | `blocked` | Returned only identity / activation greetings such as "孜澜在此", without answering `什么是因三相`. |
| `claude -p` with `--safe-mode`, repository `agents/zilan-claude-code.md`, and exact wake-word prompts through stdin | `blocked` | Still returned identity greetings or interpreted the wake-word prompt as activation, not as a concrete task. |
| `claude -p` with repository prompt through stdin but without the `孜澜` wake-word prefix | `pass-control` | Answered ZC-02 substantively, covering `遍是宗法性`, `同品定有性`, `异品遍无性`, and the dependency on `context/摄类学工具箱.md`. |

### Claude Code Failure Mode

Claude Code CLI 2.1.169 with the current local provider route did not pass the exact ZC prompt family when the prompt contained the Zilan wake word. The failures were not generic CLI failures: a minimal `claude -p --safe-mode "请只回答：OK"` returned `OK`, and a stdin control without the wake word answered ZC-02. The observed blocker is specific to the wake-word / route interaction, where a concrete task is reduced to an identity greeting.

The branch adds prompt guards that state activation keywords plus concrete tasks must be answered directly, but the current Claude Code route still failed exact wake-word prompts during this session. Therefore `agents/openai.yaml` and `docs/platform-validation.md` conservatively downgrade Claude Code from `tested` to `blocked` until a future rerun demonstrates the exact ZC prompts complete successfully.

Superseding note: the 2026-06-16 rerun below reclassifies this failure as a Windows PowerShell stdin encoding issue for Chinese prompts.

## 2026-06-16 Claude Code UTF-8 Stdin Rerun

| Field | Value |
|---|---|
| Runtime | Claude Code CLI |
| Provider / model | Claude Code 2.1.169; JSON model usage reported `deepseek-v4-pro[1m]` under the local Claude Code configuration |
| Tool version | `claude -p` noninteractive mode with `agents/zilan-claude-code.md` loaded through `--system-prompt` |
| Repository branch | `codex/claude-utf8-rerun` |
| Repository base commit | `8cebd83ed` plus Claude Code output hard-constraint prompt changes in this branch |
| Prompt set | ZC-01 through ZC-06 from `CODEX_REGRESSION_TESTS.md` and `tests/regression_cases.yaml`, using exact wake-word style prompts where applicable |
| Encoding setup | Windows PowerShell set `$OutputEncoding = [System.Text.UTF8Encoding]::new($false)` and `[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)` before piping Chinese prompts into `claude -p` |
| Transcript status | Summarized here; full JSON outputs are not committed. A compact evidence excerpt is committed at `docs/runtime-evidence/2026-06-16-claude-code-utf8-rerun.md`. ZC-06 wrote `C:\tmp\zilan-claude-validation-20260616-ZC06.md` outside the repository. |
| Repository checks | `python -m ruff check scripts tests` pass; `python -m pytest` pass; `python scripts\validate_zilan_repo.py --check-generated --strict-yaml` pass; `python scripts\mock_install_smoke.py` pass; `python scripts\openai_api_harness.py --case ZC-02` pass |
| Overall result | Claude Code `pass` with UTF-8 stdin requirement and the limitations below |

### Encoding Diagnosis

| Control | Result | Notes |
|---|---|---|
| Default PowerShell pipe into `claude -p` echo control | `fail-control` | Chinese prompt text arrived as `?????????????????`, proving that the previous wake-word prompt was not reaching Claude Code intact. |
| UTF-8 PowerShell pipe into `claude -p` echo control | `pass-control` | The same prompt arrived as `孜澜，什么是因三相？请用三点回答。`. |

The 2026-06-15 blocker is therefore reclassified as a Windows PowerShell stdin encoding failure for Chinese prompt piping. The prompt guard changes remain useful, but the critical runtime protocol is to force UTF-8 before piping Chinese prompts to Claude Code.

### Case Results

| Case | Mode | Result | Notes |
|---|---|---|---|
| ZC-01 | Skill lightweight dialogue | `pass` | Directly answered the `工作反馈` scenario, separated event,受挫感, and `我被否定了`; used `context/心类学认知分析.md` and `context/南传观禅指南.md`; no Agama overreach; boundary statement present. |
| ZC-02 | Skill concept lookup | `pass` | Directly explained `遍是宗法性`, `同品定有性`, and `异品遍无性`, and connected them to Collected Topics; used `context/因明推理引擎.md` and `context/摄类学工具箱.md`; boundary statement present. |
| ZC-03 | Skill cross-domain explanation | `pass` | Distinguished fact, concept label, `受`, `想`, and `瞋`; used `context/摄类学工具箱.md`, `context/心类学认知分析.md`, `SKILL.md`, and `tests/regression_cases.yaml`; boundary statement present. |
| ZC-04 | Explicit agent Agama search | `pass` | Used repository-local context and `scripts/search_agama.py`; excluded `_source`; reported counts for `無我`, `非我`, and `無我所` across four Agama files; supplied representative local citations and classification boundaries. |
| ZC-05 | Explicit agent cross-domain research | `pass` | Connected Agama, Collected Topics, Buddhist logic, Madhyamaka, and vipassana; supplied local citations and a reasoning chain. The run reported a `search_agama.py` attempt followed by `Grep` fallback for some citations, so this remains a transcript-backed pass with a tooling-note limitation. |
| ZC-06 | Long report output | `pass` | Used `scripts/search_agama.py` and local context; wrote `C:\tmp\zilan-claude-validation-20260616-ZC06.md`; the file check confirmed search scope, keyword groups, match statistics, classification table, representative citations, analysis, collation TODOs, and boundary statements. |

### Known Limits

- This validates Claude Code CLI noninteractive execution with repository `agents/zilan-claude-code.md` loaded directly and UTF-8 stdin used for Chinese prompts.
- It does not independently prove every user's installed `~/.claude/skills/zilan-agent` path is current.
- Background auto-spawn behavior was not separately audited; explicit ZC-04 through ZC-06 prompts were executed through the loaded agent prompt.
- Full JSON transcripts are summarized, not committed verbatim.
- Windows PowerShell users must set UTF-8 output encodings before piping Chinese prompts to `claude -p`; otherwise prompt corruption can look like a route or wake-word failure.

## 2026-06-16 Volcengine OpenAI-Compatible ZC-02 Live Run

| Field | Value |
|---|---|
| Runtime | OpenAI-compatible provider harness |
| Provider / model | Volcengine OpenAI-compatible endpoint; model `ark-code-latest` |
| API surface | `chat-completions` |
| Endpoint | `https://ark.cn-beijing.volces.com/api/coding/v3/chat/completions` |
| Base URL | `https://ark.cn-beijing.volces.com/api/coding/v3` |
| Key env | `VOLCENGINE_OPENAI_API_KEY`; value not committed |
| Repository base | Post-PR #23 `main` at `a04bbe0`; evidence committed on `codex/volcengine-live-evidence` |
| Prompt set | ZC-02 from `tests/regression_cases.yaml` |
| Transcript status | Summarized here; compact redacted evidence is committed at `docs/runtime-evidence/2026-06-16-volcengine-openai-compatible-zc-02-live.md`. Full request/response payload and provider response ID are not committed. |
| Overall result | `pass` for Volcengine OpenAI-compatible ZC-02; native OpenAI API remains `harness-ready` |

### Case Result

| Case | Mode | Result | Notes |
|---|---|---|---|
| ZC-02 | OpenAI-compatible chat-completions live | `pass` | Output explained `因三相` as a `正因` validator, covered `遍是宗法性`, `同品定有性`, and `异品遍无性`, used the `声，应是无常，以所作性故` example, cited `context/因明推理引擎.md` and `context/摄类学工具箱.md`, and did not rely on native OpenAI API. |

### Known Limits

- This validates only the Volcengine OpenAI-compatible `chat-completions` route for ZC-02.
- It does not validate native OpenAI API or the Responses API endpoint.
- It does not validate ZC-01, ZC-03, ZC-04, ZC-05, ZC-06, deeper Agama-search, or file-output cases on Volcengine.
- Full provider payload and response ID are redacted.

## 2026-06-16 Volcengine OpenAI-Compatible ZC-01 And ZC-03 Live Runs

| Field | Value |
|---|---|
| Runtime | OpenAI-compatible provider harness |
| Provider / model | Volcengine OpenAI-compatible endpoint; model `ark-code-latest` |
| Provider route | `volcengine_openai_compatible` |
| API surface | `chat-completions` |
| Endpoint | `https://ark.cn-beijing.volces.com/api/coding/v3/chat/completions` |
| Base URL | `https://ark.cn-beijing.volces.com/api/coding/v3` |
| Key env | `VOLCENGINE_OPENAI_API_KEY`; value not committed |
| Repository base | Post-PR #26 `main` at `6913178`; evidence committed on `codex/volcengine-zc01-zc03-evidence` |
| Prompt set | ZC-01 and ZC-03 from `tests/regression_cases.yaml` |
| Transcript status | Summarized here; compact redacted evidence is committed at `docs/runtime-evidence/2026-06-16-volcengine-openai-compatible-zc-01-zc-03-live.md`. Full request/response payloads and provider response IDs are not committed. |
| Overall result | `pass` for Volcengine OpenAI-compatible ZC-01 and ZC-03; together with the prior ZC-02 entry, Volcengine live coverage now includes ZC-01 through ZC-03. Native OpenAI API remains `harness-ready`. |

### Case Results

| Case | Mode | Result | Notes |
|---|---|---|---|
| ZC-01 | OpenAI-compatible chat-completions live | `pass` | Output separated work feedback from self-worth, described the feedback →苦受→想心所→防御叙事 chain, cited `context/心类学认知分析.md` and `context/南传观禅指南.md`, and offered bounded lightweight observation steps. |
| ZC-03 | OpenAI-compatible chat-completions live | `pass` | Output split the scenario into fact, interpretation, self-evaluation, and feeling layers; rejected `被批评 → 我无价值` as `不周遍`; used `触 → 作意 → 受 → 想 → 思`; cited `context/摄类学工具箱.md` and `context/心类学认知分析.md`; and stated a therapy/clinical-evaluation boundary. |

### Known Limits

- This validates ZC-01 and ZC-03 only on the Volcengine OpenAI-compatible `chat-completions` route.
- Together with the prior ZC-02 live entry, this validates ZC-01 through ZC-03 only.
- It does not validate native OpenAI API or the Responses API endpoint.
- It does not validate ZC-04, ZC-05, ZC-06, deeper Agama-search, sub-agent routing, or file-output cases on Volcengine.
- Full provider payloads and response IDs are redacted.

## 2026-06-18 Claude Code Post-Contract Target Review

| Field | Value |
|---|---|
| Runtime | Claude Code CLI |
| Provider / model | Claude Code `2.1.169`; underlying provider is governed by the user's local Claude Code configuration |
| Tool version | `claude -p` noninteractive mode with `agents/zilan-claude-code.md` loaded as the system prompt |
| Repository base | `af90038` |
| Prompt set | Target prompts for `SRQ-02`, `SRQ-03`, `SRQ-04`, plus one broad `ZC-05` cross-domain prompt |
| Encoding setup | Windows PowerShell UTF-8 stdout/console before piping Chinese prompts into `claude -p` |
| Transcript status | Compact answer excerpts committed under `docs/runtime-evidence/2026-06-18-claude-code-post-contract-*-answer.md`; raw JSON kept local only |
| Repository checks | `python scripts\semantic_answer_contract_review.py --answer-file ...` rerun on committed excerpts; `python scripts\validate_zilan_repo.py --strict-yaml` pass; `python scripts\validate_zilan_repo.py --check-generated --strict-yaml` pass; `python -m ruff check scripts tests` pass; `python -m pytest` pass; `git diff --check` pass |
| Overall result | `mixed`: targeted `SRQ-02` and `SRQ-03` pass; targeted `SRQ-04` and broad `ZC-05` reveal answer-contract gaps; no platform status change |

### Contract Results

| Answer | Reviewed Against | Result | Notes |
|---|---|---|---|
| `2026-06-18-claude-code-post-contract-srq-02-answer.md` | `SRQ-02` | `pass` | Identifies `因不成`, failed `遍是宗法性`, and the `声` / `色形` mismatch. |
| `2026-06-18-claude-code-post-contract-srq-03-answer.md` | `SRQ-03` | `pass` | Preserves `对方承许`, `归谬`, `自性有`, `缘起`, `矛盾`, and `不立自宗`. |
| `2026-06-18-claude-code-post-contract-srq-04-answer.md` | `SRQ-04` | `fail` | Missing explicit `context/agama/` local anchor wording and `代表性` status language. |
| `2026-06-18-claude-code-post-contract-zc-05-answer.md` | `SRQ-03` | `fail` | Missing explicit `对方承许`, `自性有`, and `不立自宗`; keyword review also flags `断灭`, likely from a warning against `断灭见` rather than an endorsed forbidden claim. |
| `2026-06-18-claude-code-post-contract-zc-05-answer.md` | `SRQ-04` | `fail` | Missing explicit `CBETA`, `检索范围`, `代表性`, and `待校勘` boundary terms. |

### Known Limits

- This is target-contract evidence, not a full ZC-01 through ZC-06 platform rerun.
- This does not validate native OpenAI API or the Responses API endpoint.
- The keyword contract helper is a minimum explicitness check; it can produce substring false positives, as with the `断灭` warning case.
- Follow-up work should tighten prompt/output-contract guidance for broad ZC-05-style answers before claiming SRQ-03/SRQ-04 boundaries are robust in multi-domain responses.

## 2026-06-18 Claude Code Agama Contract Fix Review

| Field | Value |
|---|---|
| Runtime | Claude Code CLI |
| Provider / model | Claude Code `2.1.169`; underlying provider is governed by the user's local Claude Code configuration |
| Tool version | `claude -p` noninteractive mode with `agents/zilan-claude-code.md` loaded as the system prompt |
| Repository base | `5d1de60` plus branch changes for the Agama evidence output contract |
| Prompt set | Target `SRQ-04` plus one broad `ZC-05` cross-domain prompt |
| Encoding setup | Windows PowerShell UTF-8 stdout/console before piping Chinese prompts into `claude -p` |
| Transcript status | Compact answer excerpts committed under `docs/runtime-evidence/2026-06-18-claude-code-agama-contract-fix-*-answer.md`; raw JSON kept local only |
| Repository checks | `python scripts\semantic_answer_contract_review.py --answer-file ...` rerun on committed excerpts; `python scripts\validate_zilan_repo.py --strict-yaml` pass; `python -m pytest tests\test_semantic_answer_contract_review_srq04.py tests\test_validate_zilan_repo.py` pass; full repository checks run before PR handoff |
| Overall result | `target-pass`: `SRQ-04` direct answer and broad `ZC-05` answer pass the Agama citation-boundary contract; `ZC-05` still fails `SRQ-03` because `对方承许` remains absent |

### Contract Results

| Answer | Reviewed Against | Result | Notes |
|---|---|---|---|
| `2026-06-18-claude-code-agama-contract-fix-srq-04-answer.md` | `SRQ-04` | `pass` | Includes `CBETA`, `T02n0099`, local `context/agama/` anchors, `检索范围`, `代表性`, and `待校勘`; no forbidden collation-overclaim terms. |
| `2026-06-18-claude-code-agama-contract-fix-zc-05-answer.md` | `SRQ-04` | `pass` | Broad answer now keeps Agama evidence in the main response and satisfies the Agama citation-boundary terms. |
| `2026-06-18-claude-code-agama-contract-fix-zc-05-answer.md` | `SRQ-03` | `fail` | Residual expected gap: answer omits literal `对方承许`; Madhyamaka/prasaṅga boundary hardening remains next work. |

### Known Limits

- This is target-contract evidence, not a full ZC-01 through ZC-06 platform rerun.
- It validates the Agama citation-boundary fix only; it does not claim the broad `ZC-05` prompt now satisfies all reasoning contracts.
- It does not validate native OpenAI API or the Responses API endpoint.
- The answer-contract helper remains a minimum explicitness check rather than a doctrinal judge.

## 2026-06-18 Claude Code Madhyamaka Contract Fix Review

| Field | Value |
|---|---|
| Runtime | Claude Code CLI |
| Provider / model | Claude Code `2.1.169`; underlying provider is governed by the user's local Claude Code configuration |
| Tool version | `claude -p` noninteractive mode with `agents/zilan-claude-code.md` loaded as the system prompt |
| Repository base | `4970810` plus branch changes for the Madhyamaka prasaṅga output contract |
| Prompt set | One broad `ZC-05` cross-domain prompt |
| Encoding setup | Windows PowerShell UTF-8 stdout/console before piping Chinese prompts into `claude -p` |
| Transcript status | Compact answer excerpt committed under `docs/runtime-evidence/2026-06-18-claude-code-madhyamaka-contract-fix-zc-05-answer.md`; raw JSON kept local only |
| Repository checks | `python scripts\semantic_answer_contract_review.py --query-id SRQ-03 --answer-file ... --json` pass; `python scripts\semantic_answer_contract_review.py --query-id SRQ-04 --answer-file ... --json` pass; `python scripts\validate_zilan_repo.py --strict-yaml` pass; targeted pytest and ruff pass; full repository checks run before PR handoff |
| Overall result | `target-pass`: broad `ZC-05` answer now passes both the `SRQ-03` Madhyamaka prasaṅga-boundary contract and the `SRQ-04` Agama citation-boundary contract |

### Contract Results

| Answer | Reviewed Against | Result | Notes |
|---|---|---|---|
| `2026-06-18-claude-code-madhyamaka-contract-fix-zc-05-answer.md` | `SRQ-03` | `pass` | Includes `对方承许`, `归谬`, `自性有`, `缘起`, `矛盾`, and `不立自宗`; no forbidden prasaṅga-overclaim terms. |
| `2026-06-18-claude-code-madhyamaka-contract-fix-zc-05-answer.md` | `SRQ-04` | `pass` | Preserves `CBETA`, `T02n0099`, local `context/agama/` anchors, `检索范围`, `代表性`, and `待校勘`; no forbidden collation-overclaim terms. |

### Known Limits

- This is target-contract evidence, not a full ZC-01 through ZC-06 platform rerun.
- It validates the narrow Madhyamaka prasaṅga output-contract fix and checks that the prior Agama evidence contract still holds for `ZC-05`.
- It does not validate native OpenAI API or the Responses API endpoint.
- The answer-contract helper remains a minimum explicitness check rather than a doctrinal judge.

## 2026-06-18 Claude Code Post-Contract Full Rerun

| Field | Value |
|---|---|
| Runtime | Claude Code CLI |
| Provider / model | Claude Code `2.1.169`; underlying provider is governed by the user's local Claude Code configuration |
| Tool version | `claude -p` noninteractive mode with `agents/zilan-claude-code.md` loaded as the system prompt |
| Repository base | `3b14473` (`Tighten Madhyamaka prasanga output contract (#48)`) |
| Branch | `codex/claude-post-contract-full-rerun-20260618` |
| Prompt set | `ZC-01` through `ZC-06` from `tests/regression_cases.yaml` |
| Encoding setup | Windows PowerShell UTF-8 stdout/console before piping Chinese prompts into `claude -p` |
| Transcript status | Compact evidence committed at `docs/runtime-evidence/2026-06-18-claude-code-post-contract-full-rerun.md`; raw JSON and answer Markdown kept local only under `C:\tmp\zilan-claude-post-contract-full-rerun-20260618` |
| Repository checks | `python scripts\semantic_answer_contract_review.py --query-id SRQ-03 --answer-file C:\tmp\zilan-claude-post-contract-full-rerun-20260618\ZC-05.answer.md --json` pass; `python scripts\semantic_answer_contract_review.py --query-id SRQ-04 --answer-file C:\tmp\zilan-claude-post-contract-full-rerun-20260618\ZC-05.answer.md --json` pass; full repository checks run before PR handoff |
| Overall result | `pass` with limitations: the Claude Code route still requires UTF-8 stdin for Chinese prompts; ZC-04 had minor local-anchor formatting variance; ZC-06 wrote its report to the installed skill reports path rather than the repository |

### Case Results

| Case | Mode | Result | Notes |
|---|---|---|---|
| ZC-01 | Skill lightweight dialogue | `pass` | Directly answered the work-feedback scenario, separated event from self-worth, used the five-mental-factor chain, and stated bounded practice guidance. |
| ZC-02 | Skill concept lookup | `pass` | Explained `因三相` with `遍是宗法性`, `同品定有性`, and `异品遍无性`. |
| ZC-03 | Skill cross-domain explanation | `pass` | Combined Collected Topics and cognitive-analysis framing, including `不周遍`, `受`, `想`, `瞋`, and a practice / clinical boundary. |
| ZC-04 | Explicit agent Agama search | `pass` | Produced an Agama no-self search and preliminary classification with CBETA identifiers, local Markdown line anchors, representative evidence, and collation boundaries. Some local references used shorter file anchors instead of the full `context/agama/` prefix; this case was not reviewed against `SRQ-04`. |
| ZC-05 | Explicit agent cross-domain research | `pass` | Broad cross-domain answer preserved Agama evidence and Madhyamaka prasaṅga boundaries after the prompt-contract fixes; `SRQ-03` and `SRQ-04` contract review both passed. |
| ZC-06 | Long report output | `pass` | Generated the requested long report and wrote it to `~/.claude/skills/zilan-agent/reports/阿含无我观法门研究报告.md`; local file check confirmed the report exists. |

### Known Limits

- This refreshes Claude Code post-contract validation evidence; it does not validate native OpenAI API or any OpenAI-compatible provider route.
- Background auto-spawn behavior was not separately audited; ZC-04 through ZC-06 used explicit spawn-style prompts through the loaded Claude Code agent prompt.
- Full JSON and answer transcripts are not committed. The committed evidence is a compact review summary.
- The answer-contract helper is a minimum explicitness check, not doctrinal grading.

## 2026-06-20 Claude Code SRQ-05 Spot Review

| Field | Value |
|---|---|
| Runtime | Claude Code CLI |
| Provider / model | Claude Code `2.1.169`; underlying provider is governed by the user's local Claude Code configuration |
| Tool version | `claude -p` noninteractive mode with `agents/zilan-claude-code.md` loaded as the system prompt |
| Repository base | `8ea2144` (`Add Hetuvidya non-pervasive fixture (#51)`) |
| Prompt set | One target `SRQ-05`-style Hetuvidya prompt: `孜澜，检验论式：声，应是无常，以是所知故。` |
| Encoding setup | Windows PowerShell UTF-8 stdout/console before passing Chinese prompt text to `claude -p` |
| Transcript status | Compact answer excerpt committed at `docs/runtime-evidence/2026-06-20-claude-code-srq-05-spot-review-answer.md`; raw transcript not committed |
| Repository checks | `python scripts\semantic_answer_contract_review.py --query-id SRQ-05 --answer-file docs\runtime-evidence\2026-06-20-claude-code-srq-05-spot-review-answer.md --json` pass; full repository checks run before PR handoff |
| Overall result | `target-pass`: Claude Code's direct SRQ-05 answer satisfies the Hetuvidya `不周遍` answer contract; no platform status change |

### Contract Results

| Answer | Reviewed Against | Result | Notes |
|---|---|---|---|
| `2026-06-20-claude-code-srq-05-spot-review-answer.md` | `SRQ-05` | `pass` | Identifies the论式 decomposition, first-check success, failed `异品遍无性`, `常法` counterexamples, and `不周遍` classification. |

### Known Limits

- This is a target-contract spot review, not a full ZC-01 through ZC-06 platform rerun.
- It does not validate native OpenAI API or any OpenAI-compatible provider route.
- The answer-contract helper remains a minimum explicitness check rather than a doctrinal judge.

## 2026-06-28 Claude Code SRQ-08 / ZC-05 Spot Review

| Field | Value |
|---|---|
| Runtime | Claude Code CLI |
| Provider / model | Claude Code `2.1.195`; underlying provider is governed by the user's local Claude Code configuration |
| Tool version | `claude -p` noninteractive mode with `agents/zilan-claude-code.md` loaded as the system prompt |
| Repository base | `fd7f7cc` (`Add reasoning contract runner (#58)`) |
| Branch | `codex/runtime-spot-review-srq08-zc05-20260628` |
| Prompt set | One direct `SRQ-08` prompt plus one broad `ZC-05` cross-domain prompt |
| Encoding setup | Windows PowerShell UTF-8 stdout/console before piping Chinese prompts into `claude -p` |
| Transcript status | Compact evidence committed at `docs/runtime-evidence/2026-06-28-claude-code-srq-08-zc-05-spot-review.md`; raw JSON and extracted answer Markdown kept local only under `C:\tmp\zilan-srq08-zc05-spot-review-20260628` |
| Repository checks | `python scripts\reasoning_contract_runner.py --query-id SRQ-08 --answer-file ...` run on both extracted answers; full repository checks run before PR handoff |
| Overall result | `target-gap`: both answers mechanically fail the `SRQ-08` answer contract; no platform status change |

### Contract Results

| Answer | Reviewed Against | Result | Notes |
|---|---|---:|---|
| `SRQ-08.answer.md` | `SRQ-08` / `madhyamaka_nihilism_boundary` | `fail` | The answer explicitly rejects deriving `因果不存在` from `无自性` and states a two-truths-style distinction, but misses literal required terms `只破自性有`, `断灭`, and `不成立`, plus the `nihilism_error` slot. |
| `ZC-05.answer.md` | `SRQ-08` / `madhyamaka_nihilism_boundary` | `fail` | The broad ZC-05 answer preserves existing no-self, Agama, Collected Topics, Hetuvidya, Madhyamaka, and practice boundaries, but does not explicitly surface the causality-cancellation / nihilism boundary required by `SRQ-08`. |

### Known Limits

- This is a target-contract spot review, not a full ZC-01 through ZC-06 platform rerun.
- It does not validate native OpenAI API or any OpenAI-compatible provider route.
- The mechanical failure is an explicitness gap, not by itself proof of doctrinal failure.
- Follow-up work should decide whether to tighten the agent prompt for SRQ-08 wording, loosen the fixture to accept `断见`-style wording, or both.

## 2026-06-28 Claude Code SRQ-08 Boundary Fix Spot Review

| Field | Value |
|---|---|
| Runtime | Claude Code CLI |
| Provider / model | Claude Code `2.1.195`; underlying provider is governed by the user's local Claude Code configuration |
| Tool version | `claude -p` noninteractive mode with `agents/zilan-claude-code.md` loaded as the system prompt |
| Repository base | `787d4bd` plus this PR's prompt-contract changes |
| Branch | `codex/srq08-nihilism-boundary-prompt-20260628` |
| Prompt set | One direct `SRQ-08` prompt plus one broad `ZC-05` cross-domain prompt |
| Encoding setup | Windows PowerShell UTF-8 stdout/console before piping Chinese prompts into `claude -p` |
| Transcript status | Compact evidence committed at `docs/runtime-evidence/2026-06-28-claude-code-srq-08-boundary-fix.md`; raw JSON and extracted answer Markdown kept local only under `C:\tmp\zilan-srq08-boundary-fix-20260628` |
| Repository checks | `python scripts\reasoning_contract_runner.py --query-id SRQ-08 --answer-file ...` run on both extracted answers; full repository checks run before PR handoff |
| Overall result | `pass`: both answers pass the `SRQ-08` answer contract; no platform status change |

### Contract Results

| Answer | Reviewed Against | Result | Notes |
|---|---|---:|---|
| `SRQ-08.answer.md` | `SRQ-08` / `madhyamaka_nihilism_boundary` | `pass` | Required terms and slots all present, including `只破自性有`, `断灭`, and `二谛`; no forbidden terms present. |
| `ZC-05.answer.md` | `SRQ-08` / `madhyamaka_nihilism_boundary` | `pass` | Broad ZC-05 answer now explicitly preserves the same nihilism boundary in the Madhyamaka segment; no forbidden terms present. |

### Known Limits

- This is a target-contract spot review, not a full ZC-01 through ZC-06 platform rerun.
- It does not validate native OpenAI API or any OpenAI-compatible provider route.
- The answer-contract helper remains a minimum explicitness check rather than a doctrinal judge.

## 2026-07-02 Claude Code SRQ-07 Collected Topics Boundary Fix Spot Review

| Field | Value |
|---|---|
| Runtime | Claude Code CLI |
| Provider / model | Claude Code `2.1.195`; underlying provider is governed by the user's local Claude Code configuration |
| Tool version | `claude -p` noninteractive mode with `agents/zilan-claude-code.md` loaded as the system prompt |
| Repository base | `57ea21e` plus this PR's prompt-contract changes |
| Branch | `collected-topics-boundary-contract` |
| Prompt set | One direct `SRQ-07` prompt plus one broad `ZC-03` work-feedback prompt |
| Encoding setup | Windows PowerShell UTF-8 stdout/console before piping Chinese prompts into `claude -p` |
| Transcript status | Compact evidence committed at `docs/runtime-evidence/2026-07-02-claude-code-srq-07-collected-topics-boundary-fix.md`; raw JSON and extracted answer Markdown kept local only under `C:\tmp\zilan-srq07-collected-topics-boundary-20260702` |
| Repository checks | `python scripts\reasoning_contract_runner.py --query-id SRQ-07 --answer-file ...` run on the direct answer; ZC-03 checked by literal Collected Topics boundary term scan; full repository checks run before PR handoff |
| Overall result | `pass`: direct SRQ-07 passes the `collected_topics_total_part_error` contract, and broad ZC-03 explicitly surfaces the same boundary terms; no platform status change |

### Review Results

| Answer | Reviewed Against | Result | Notes |
|---|---|---:|---|
| `SRQ-07-rerun.answer.md` | `SRQ-07` / `collected_topics_total_part_error` | `pass` | Required terms and slots all present, including `总别混淆`, `局部别法`, `整体总法`, `不周遍`, and `不成立`; no forbidden terms present. |
| `ZC-03-rerun.answer.md` | Collected Topics boundary term scan | `pass` | Broad work-feedback answer explicitly includes `总与别`, `局部别法`, `整体总法`, `总别混淆`, `不周遍`, and `不成立`. |

### Known Limits

- This is a target-contract spot review, not a full ZC-01 through ZC-06 platform rerun.
- It does not validate native OpenAI API or any OpenAI-compatible provider route.
- The answer-contract helper remains a minimum explicitness check rather than a doctrinal judge.

## 2026-07-06 Claude Code SRQ-09 Cognitive Practice Boundary Spot Review

| Field | Value |
|---|---|
| Runtime | Claude Code CLI |
| Provider / model | Claude Code `2.1.195`; underlying provider is governed by the user's local Claude Code configuration |
| Tool version | `claude -p` noninteractive mode with `agents/zilan-claude-code.md` loaded as the system prompt |
| Repository base | `7bbaa62` (`Add SRQ-09 cognitive practice boundary fixture (#62)`) |
| Branch | `srq09-runtime-spot-review` |
| Prompt set | One direct `SRQ-09` prompt plus one broad `ZC-03` work-feedback prompt |
| Encoding setup | Windows PowerShell UTF-8 stdout/console before piping Chinese prompts into `claude -p` |
| Transcript status | Compact evidence committed at `docs/runtime-evidence/2026-07-06-claude-code-srq-09-spot-review.md`; raw JSON and extracted answer Markdown kept local only under `C:\tmp\zilan-srq09-spot-review-20260706` |
| Repository checks | `python scripts\reasoning_contract_runner.py --query-id SRQ-09 --answer-file ...` run on both extracted answers; full repository checks run before PR handoff |
| Overall result | `target-gap`: both answers mechanically fail the `SRQ-09` answer contract; no platform status change |

### Contract Results

| Answer | Reviewed Against | Result | Notes |
|---|---|---:|---|
| `SRQ-09.answer.md` | `SRQ-09` / `cognitive_practice_boundary` | `fail` | Covers the five-universal chain and a practice boundary with no forbidden terms, but misses the `cognitive_quality` slot and required explicit terms including `颠倒知`, `慧`, `无瞋`, `行舍`, `缘摄受`, `三相印证`, and `非心理治疗`. |
| `ZC-03.answer.md` | `SRQ-09` / `cognitive_practice_boundary` | `fail` | Covers the cognitive-quality path and several corrective factors with no forbidden terms, but misses the `vipassana_mapping` slot and required explicit terms including `名色分别`, `缘摄受`, `三相印证`, `非心理治疗`, and `善知识指导`. |

### Known Limits

- This is a target-contract spot review, not a full ZC-01 through ZC-06 platform rerun.
- It does not validate native OpenAI API or any OpenAI-compatible provider route.
- The answer-contract helper remains a minimum explicitness check rather than a doctrinal judge.
- The result is an explicitness gap, not by itself proof of doctrinal failure.

## 2026-07-06 Claude Code SRQ-09 Boundary Fix Spot Review

| Field | Value |
|---|---|
| Runtime | Claude Code CLI |
| Provider / model | Claude Code `2.1.195`; underlying provider is governed by the user's local Claude Code configuration |
| Tool version | `claude -p` noninteractive mode with `agents/zilan-claude-code.md` loaded as the system prompt |
| Repository base | `01c998e` plus this PR's prompt-contract changes |
| Branch | `srq09-cognitive-practice-boundary-prompt` |
| Prompt set | One direct `SRQ-09` prompt plus one broad `ZC-03` work-feedback prompt |
| Encoding setup | Windows PowerShell UTF-8 stdout/console before piping Chinese prompts into `claude -p` |
| Transcript status | Compact evidence committed at `docs/runtime-evidence/2026-07-06-claude-code-srq-09-boundary-fix.md`; raw JSON and extracted answer Markdown kept local only under `C:\tmp\zilan-srq09-boundary-fix-20260706` |
| Repository checks | `python scripts\reasoning_contract_runner.py --query-id SRQ-09 --answer-file ...` run on both final extracted answers; full repository checks run before PR handoff |
| Overall result | `pass`: both final answers pass the `SRQ-09` answer contract; no platform status change |

### Contract Results

| Answer | Reviewed Against | Result | Notes |
|---|---|---:|---|
| `SRQ-09.final.answer.md` | `SRQ-09` / `cognitive_practice_boundary` | `pass` | Required terms and slots all present, including the five-universal chain, `颠倒知`, `念`, `慧`, `无瞋`, `行舍`, `名色分别`, `缘摄受`, `三相印证`, `非心理治疗`, and `善知识指导`; no forbidden terms present. |
| `ZC-03.final.answer.md` | `SRQ-09` / `cognitive_practice_boundary` | `pass` | Broad work-feedback answer also preserves `颠倒知`, `犹豫识`, `比量`, corrective factors, vipassana mapping, and practice-boundary terms; no forbidden terms present. |

### Known Limits

- This is a target-contract spot review, not a full ZC-01 through ZC-06 platform rerun.
- It does not validate native OpenAI API or any OpenAI-compatible provider route.
- The answer-contract helper remains a minimum explicitness check rather than a doctrinal judge.
- `--dangerously-skip-permissions` was used only to keep local noninteractive Claude Code validation from stopping at file-read approval prompts.

## 2026-07-13 Claude Code SRQ-11 Collected Topics Definition-Scope Spot Review

| Field | Value |
|---|---|
| Runtime | Claude Code CLI |
| Provider / model | Claude Code `2.1.204`; underlying provider is governed by the user's local Claude Code configuration |
| Tool version | `claude -p` noninteractive mode with `agents/zilan-claude-code.md` loaded as the system prompt |
| Repository base | `4d276f1` (`Add Collected Topics definition-scope fixture (#100)`) |
| Branch | `srq11-runtime-spot-review` |
| Prompt set | One direct `SRQ-11` definition-scope prompt |
| Encoding setup | Windows PowerShell UTF-8 stdout/console/stdin before piping Chinese prompts into `claude -p` |
| Transcript status | Compact evidence committed at `docs/runtime-evidence/2026-07-13-claude-code-srq-11-spot-review.md`; raw JSON and extracted answer Markdown kept local only under `C:\tmp\zilan-srq11-spot-review-20260713` |
| Repository checks | `python scripts\reasoning_contract_runner.py --query-id SRQ-11 --answer-file C:\tmp\zilan-srq11-spot-review-20260713\SRQ-11.answer.md --json` pass; full repository checks run before PR handoff |
| Overall result | `pass`: the direct answer passes the `SRQ-11` Collected Topics definition-scope answer contract; no platform status change |

### Contract Results

| Answer | Reviewed Against | Result | Notes |
|---|---|---:|---|
| `SRQ-11.answer.md` | `SRQ-11` / `collected_topics_definition_scope_error` | `pass` | Required terms and slots all present, including `摄类学`, `性相`, `所表`, `能盛水者`, `瓶`, `湖`, `性相过宽`, `唯在所表上成立`, `违②`, `错误类型`, and `不成立`; no forbidden terms present. |

### Known Limits

- This is a target-contract spot review, not a full ZC-01 through ZC-06 platform rerun.
- It does not validate native OpenAI API or any OpenAI-compatible provider route.
- The answer-contract helper remains a minimum explicitness check rather than a doctrinal judge.
- This evidence does not change platform validation status.

## 2026-07-14 Claude Code SRQ-04 / ZC-04 Agama Citation Boundary Spot Review

| Field | Value |
|---|---|
| Runtime | Claude Code CLI |
| Provider / model | Claude Code `2.1.204`; underlying provider is governed by the user's local Claude Code configuration |
| Tool version | `claude -p` noninteractive mode with `agents/zilan-claude-code.md` loaded as the system prompt |
| Repository base | `512a333` (`Preserve Agama section titles in citations (#117)`) |
| Branch | `srq04-agama-runtime-spot-review` |
| Prompt set | One direct `SRQ-04` prompt, one exact `ZC-04` prompt attempt, and one compact `ZC-04`-style Agama-search prompt |
| Encoding setup | Windows PowerShell UTF-8 stdout/console/stdin before piping Chinese prompts into `claude -p` |
| Transcript status | Compact evidence committed at `docs/runtime-evidence/2026-07-14-claude-code-srq-04-zc-04-agama-boundary-spot-review.md`; raw JSON and extracted answer Markdown kept local only under `C:\tmp\zilan-srq04-zc04-spot-review-20260714` |
| Repository checks | `python scripts\semantic_answer_contract_review.py --query-id SRQ-04 --answer-file C:\tmp\zilan-srq04-zc04-spot-review-20260714\SRQ-04.answer.md --json` pass; same review for `ZC-04-compact.answer.md` fail only on forbidden term `校勘确认`; full repository checks run before PR handoff |
| Overall result | `target-partial`: direct `SRQ-04` passes; compact `ZC-04`-style answer covers citation-boundary slots but exposes a shallow forbidden-term/negation nuance; no platform status change |

### Contract Results

| Answer | Reviewed Against | Result | Notes |
|---|---|---:|---|
| `SRQ-04.answer.md` | `SRQ-04` / `agama_citation_boundary` | `pass` | Preserves search scope, representative status, `CBETA`, `T02n0099`, local `context/agama/` anchors, local line numbers, title-bearing paragraph labels where available, and `待校勘` / publication-level boundary language. |
| Exact `ZC-04` prompt | `ZC-04` runtime attempt | `blocked` | Timed out after 304 seconds and produced no saved answer file. |
| `ZC-04-compact.answer.md` | `SRQ-04` / `agama_citation_boundary` | `fail` | Required terms and slots are present, including local line anchors and section markers/titles. Mechanical review fails because the negated boundary phrase `不构成校勘确认` contains forbidden term `校勘确认`. |

### Known Limits

- This is a target-contract spot review, not a full ZC-01 through ZC-06 platform rerun.
- The exact broad `ZC-04` prompt needs a separate long-running or bounded-output rerun if exact-case performance is the target.
- The answer-contract helper is a minimum explicitness check and does not understand negation scope, so `不构成校勘确认` is mechanically flagged even though it is a boundary statement rather than a collation overclaim.
- This evidence does not validate native OpenAI API or any OpenAI-compatible provider route.

## 2026-07-14 Claude Code Compact ZC-04 Agama Boundary Rerun

| Field | Value |
|---|---|
| Runtime | Claude Code CLI |
| Provider / model | Claude Code `2.1.204`; underlying provider is governed by the user's local Claude Code configuration |
| Tool version | `claude -p` noninteractive mode with `agents/zilan-claude-code.md` loaded as the system prompt |
| Repository base | `25bdb5d` (`Tighten Agama collation boundary wording (#119)`) |
| Branch | `zc04-agama-boundary-rerun` |
| Prompt set | One compact `ZC-04`-style Agama-search prompt after prompt wording hardening |
| Encoding setup | Windows PowerShell UTF-8 stdout/console/stdin before piping Chinese prompts into `claude -p` |
| Transcript status | Compact evidence committed at `docs/runtime-evidence/2026-07-14-claude-code-zc-04-agama-boundary-rerun.md`; raw JSON and extracted answer Markdown kept local only under `C:\tmp\zilan-zc04-boundary-rerun-20260714` |
| Repository checks | `python scripts\semantic_answer_contract_review.py --query-id SRQ-04 --answer-file C:\tmp\zilan-zc04-boundary-rerun-20260714\ZC-04-compact-rerun.answer.md --json` pass; full repository checks run before PR handoff |
| Overall result | `target-pass`: compact `ZC-04` now passes the `SRQ-04` Agama citation-boundary contract after the prompt wording fix; no platform status change |

### Contract Results

| Answer | Reviewed Against | Result | Notes |
|---|---|---:|---|
| `ZC-04-compact-rerun.answer.md` | `SRQ-04` / `agama_citation_boundary` | `pass` | Preserves search scope, representative status, `CBETA`, `T02n0099`, local `context/agama/` anchors, local line numbers, title-bearing paragraph labels where available, and `待校勘` / publication-level boundary language. No forbidden collation-overclaim terms were present. |

### Known Limits

- This is a compact target-contract rerun, not a full ZC-01 through ZC-06 platform rerun.
- It validates the current Claude Code CLI route with repository prompt loaded through UTF-8 stdin; it does not validate native OpenAI API or any OpenAI-compatible provider route.
- The answer-contract helper is a minimum explicitness check and does not grade doctrinal correctness or retrieval completeness.
- This evidence does not change platform validation status.

## 2026-07-14 Claude Code Post-Prompt ZC-01 To ZC-06 Rerun

| Field | Value |
|---|---|
| Runtime | Claude Code CLI |
| Provider / model | Claude Code `2.1.204`; underlying provider is governed by the user's local Claude Code configuration |
| Tool version | `claude -p` noninteractive mode with `agents/zilan-claude-code.md` loaded as the system prompt |
| Repository base | `b78732a` (`docs: update closing dharma seal (#122)`) |
| Branch | `claude-post-prompt-rerun-evidence` |
| Prompt set | `ZC-01` through `ZC-06` from `tests/regression_cases.yaml`, rerun after root-document archival and closing Dharma-seal wording changes |
| Encoding setup | Windows PowerShell UTF-8 stdout/console/stdin before piping Chinese prompts into `claude -p` |
| Transcript status | Compact evidence committed at `docs/runtime-evidence/2026-07-14-claude-code-post-prompt-zc-01-zc-06-rerun.md`; raw JSON and extracted answer Markdown kept local only under `C:\tmp\zilan-claude-post-prompt-rerun-20260714`; `ZC-06` generated `C:\Users\rori9\Desktop\阿含无我观法门研究报告.md` outside the repository |
| Repository checks | Contract spot checks run for `ZC-03`/`SRQ-09`, `ZC-04`/`SRQ-04`, `ZC-05`/`SRQ-03`, `ZC-05`/`SRQ-08`, and generated `ZC-06` report/`SRQ-04`; full repository checks run before PR handoff |
| Overall result | `partial`: all six Claude Code invocations returned `success`, while strict answer-contract review still exposes `ZC-04`/`SRQ-04` and `ZC-05`/`SRQ-08` explicitness gaps; no platform status change |

### Case Results

| Case | Runtime result | Contract result | Notes |
|---|---|---|---|
| `ZC-01` | `success` | not run | Lightweight work-feedback support response; no file output. |
| `ZC-02` | `success` | not run | Explains `因三相` with expected Hetuvidya terminology. |
| `ZC-03` | `success` | `SRQ-09` pass | Cross-domain Collected Topics / cognitive-analysis answer preserves cognitive-chain and practice-boundary slots. |
| `ZC-04` | `success` | `SRQ-04` fail | Main answer is a compact summary; it misses explicit `T02n0099`, `context/agama/`, `检索范围`, and `代表性` terms, plus `search_scope` and `evidence_status` slots. |
| `ZC-05` | `success` | `SRQ-03` pass; `SRQ-08` fail | Prasaṅga boundary is present; nihilism-boundary explicitness is incomplete because `断灭`, `二谛`, `不成立`, and the `nihilism_error` slot are missing. |
| `ZC-06` | `success` | generated report `SRQ-04` pass | Main answer reports file creation; generated report at `C:\Users\rori9\Desktop\阿含无我观法门研究报告.md` satisfies `SRQ-04`. |

### Known Limits

- This rerun validates Claude Code execution and records answer-contract gaps; it does not upgrade or downgrade platform status.
- Raw Claude JSON and full extracted answers are summarized, not committed.
- The generated `ZC-06` report remains outside the repository and is summarized only.
- Follow-up work should make broad `ZC-04` and `ZC-05` answers preserve the same explicit boundary slots already proven by compact target reviews.

## 2026-07-14 Claude Code Broad Boundary Postfix Review

| Field | Value |
|---|---|
| Runtime | Claude Code CLI |
| Provider / model | Claude Code `2.1.204`; underlying provider is governed by the user's local Claude Code configuration |
| Tool version | `claude -p` noninteractive mode with `agents/zilan-claude-code.md` loaded as the system prompt |
| Repository base | `c6b686c` (`Harden broad boundary prompt slots (#124)`) |
| Branch | `post-broad-boundary-runtime-review` |
| Prompt set | Broad `ZC-04` and `ZC-05` runtime spot review after #124 prompt hardening |
| Encoding setup | Windows PowerShell UTF-8 stdout/console/stdin before piping Chinese prompts into `claude -p` |
| Transcript status | Compact evidence committed at `docs/runtime-evidence/2026-07-14-claude-code-broad-boundary-postfix-review.md`; raw JSON and extracted answer Markdown kept local only under `C:\tmp\zilan-claude-broad-boundary-postfix-20260714` |
| Repository checks | Contract spot checks run for `ZC-04`/`SRQ-04`, `ZC-05`/`SRQ-04`, `ZC-05`/`SRQ-03`, and `ZC-05`/`SRQ-08`; full repository checks run before PR handoff |
| Overall result | `partial`: broad `ZC-05` now passes `SRQ-03`, `SRQ-04`, and `SRQ-08`; broad `ZC-04` still fails `SRQ-04` on missing `检索范围`, `T02n0099`, and `search_scope`; no platform status change |

### Contract Results

| Answer | Reviewed Against | Result | Notes |
|---|---|---:|---|
| `ZC-04.answer.md` | `SRQ-04` / `agama_citation_boundary` | `fail` | Missing `检索范围`, `T02n0099`, and `search_scope`; no forbidden collation-overclaim terms. |
| `ZC-05.answer.md` | `SRQ-04` / `agama_citation_boundary` | `pass` | Required Agama citation-boundary terms and slots are present. |
| `ZC-05.answer.md` | `SRQ-03` / `madhyamaka_prasanga_boundary` | `pass` | `SRQ-03` forbidden terms were narrowed from bare `断灭` to `断灭的结论` so boundary-word use does not conflict with `SRQ-08`. |
| `ZC-05.answer.md` | `SRQ-08` / `madhyamaka_nihilism_boundary` | `pass` | Required nihilism-boundary terms and slots are present. |

### Known Limits

- This is a targeted runtime spot review, not a full platform rerun.
- Broad `ZC-04` still needs a follow-up if direct Agama summary answers must always preserve the exact `SRQ-04` slots.
- This evidence does not change platform validation status.

## 2026-07-14 Claude Code ZC-04 Post-#126 Agama Slot Rerun

| Field | Value |
|---|---|
| Runtime | Claude Code CLI |
| Provider / model | Claude Code `2.1.204`; CLI model usage reported `deepseek-v4-pro[1m]` under the user's local configuration |
| Repository base | `43b408a` (`Harden broad ZC-04 Agama slots (#126)`) |
| Branch | `broad-zc04-agama-slot-rerun` |
| Prompt set | Broad `ZC-04` `四阿含` `无我` survey prompt |
| Encoding setup | Windows PowerShell UTF-8 stdout/console/stdin with prompt read from a UTF-8 file |
| Transcript status | Compact evidence committed at `docs/runtime-evidence/2026-07-14-claude-code-zc-04-post-126-agama-slot-rerun.md`; raw JSON and extracted answer Markdown kept local only under `C:\tmp\zilan-claude-zc04-post126-20260714` |
| Repository checks | `SRQ-04` answer-contract review passed; full repository checks run before PR handoff |
| Overall result | `pass`: broad `ZC-04` now preserves `检索范围`, `T02n0099`, `CBETA`, `context/agama/`, `代表性`, and `待校勘` in the main response; no platform status change |

### Contract Results

| Answer | Reviewed Against | Result | Notes |
|---|---|---:|---|
| `ZC-04.answer.md` | `SRQ-04` / `agama_citation_boundary` | `pass` | Required terms and slots are present; no forbidden collation-overclaim terms are present. |

### Known Limits

- This is a targeted runtime spot review, not a full platform rerun.
- The answer-contract helper is a minimum explicitness check and does not grade retrieval completeness or publication-level collation.

## 2026-08-06 Claude Code ZC-05 / SRQ-01 Runtime Spot Review

| Field | Value |
|---|---|
| Runtime | Claude Code CLI |
| Provider / model | Claude Code `2.1.220`; underlying provider is governed by the user's local Claude Code configuration |
| Tool version | `claude -p` noninteractive mode with `agents/zilan-claude-code.md` loaded as the system prompt |
| Repository base | `9ef4a76` (`Harden broad ZC-05 SRQ-01 prompt slots`) plus branch-local prompt / fixture cleanup |
| Branch | `codex/zc05-srq01-runtime-spot` |
| Prompt set | One broad `ZC-05` cross-domain prompt: `请 spawn 一个 zilan agent，用应成论式分析诸法无我，并串联阿含、摄类学、因明和观禅。` |
| Encoding setup | Windows PowerShell UTF-8 stdout/console/stdin before piping Chinese prompts into `claude -p` |
| Transcript status | Standalone answer excerpt committed at `docs/runtime-evidence/2026-08-06-claude-code-zc-05-srq-01-runtime-spot-answer.md`; compact review committed at `docs/runtime-evidence/2026-08-06-zc-05-srq-01-runtime-spot-review.md`; raw JSON and extracted answer Markdown kept local only under `C:\tmp\zilan-zc05-srq01-runtime-spot-20260806` |
| Repository checks | Batch review run for `SRQ-01`, `SRQ-03`, `SRQ-04`, and `SRQ-08`; full repository checks run before PR handoff |
| Overall result | `partial`: final committed broad `ZC-05` answer passes `SRQ-04` but still fails `SRQ-01`, `SRQ-03`, and `SRQ-08`; no platform status change |

### Contract Results

| Answer | Reviewed Against | Result | Notes |
|---|---|---:|---|
| `2026-08-06-claude-code-zc-05-srq-01-runtime-spot-answer.md` | `SRQ-01` / `cross_domain_no_self_analysis` | `fail` | Missing literal `阿含证据`, `代表性检索`, and `因明校验` terms. The answer also uses shortened citation bullet anchors such as `T0099-za-agama.md:147` even though the prompt asks for complete `context/agama/...` anchors. |
| `2026-08-06-claude-code-zc-05-srq-01-runtime-spot-answer.md` | `SRQ-03` / `madhyamaka_prasanga_boundary` | `fail` | Missing literal `不立自宗`. |
| `2026-08-06-claude-code-zc-05-srq-01-runtime-spot-answer.md` | `SRQ-04` / `agama_citation_boundary` | `pass` | Required Agama citation-boundary terms and slots are present after the minimum-template prompt hardening. |
| `2026-08-06-claude-code-zc-05-srq-01-runtime-spot-answer.md` | `SRQ-08` / `madhyamaka_nihilism_boundary` | `fail` | Missing literal `二谛` and the proposition-decomposition slot. |

### Known Limits

- This is a targeted runtime spot review, not a full `ZC-01` through `ZC-06` platform rerun.
- The runtime still does not prove broad `ZC-05` integrated `SRQ-01` pass; current status is runtime pending / strict replay fail.
- The answer-contract helper checks minimum explicitness and does not grade doctrinal correctness, retrieval completeness, or publication-level collation.
- This evidence does not validate native OpenAI API or any OpenAI-compatible provider route, and it does not change platform validation status.

## 2026-08-19 Claude Code SRQ-11 Definition Runtime Rerun Attempt

| Field | Value |
|---|---|
| Runtime | Claude Code CLI |
| Provider / model | Claude Code `2.1.234`; local configuration attempted custom DeepSeek Anthropic-compatible model `deepseek-v4-pro[1m]` |
| Tool version | `claude -p` noninteractive mode with `agents/zilan-claude-code.md` loaded as the system prompt |
| Repository commit | post-`SRQ-11` definition-boundary prompt hardening on `main` |
| Prompt set | Direct `SRQ-11` prompt: `用摄类学检查定义：瓶的性相是能盛水者。这个定义成立吗？请直接回答，不要写入文件。` |
| Encoding setup | Windows PowerShell UTF-8 stdout/console/stdin before invoking `claude -p` |
| Transcript status | No answer excerpt; summary-only blocked evidence committed at `docs/runtime-evidence/2026-08-19-srq11-definition-runtime-rerun.md` |
| Repository checks | Local prompt invariant checks passed before the runtime attempt; no answer-contract batch was created because no answer file exists |
| Overall result | `blocked` / `runtime_pending`: Claude Code returned `[claude-code:unrecognized_model] {"model":"deepseek-v4-pro[1m]","query_source":"sdk"}` before answer generation; no platform-status change |

### Known Limits

- This attempt does not validate `SRQ-11` runtime behavior after prompt hardening.
- The already committed 2026-08-19 `SRQ-11` answer excerpt remains fail evidence under the current answer contract.
- `docs/platform-validation.md` remains unchanged.

## Next Validation Entries

Use this template for future manual sessions:

```markdown
## YYYY-MM-DD Runtime Name

| Field | Value |
|---|---|
| Runtime |  |
| Provider / model |  |
| Tool version |  |
| Repository commit |  |
| Prompt set |  |
| Transcript status | committed / summarized / unavailable |
| Repository checks |  |

| Case | Mode | Result | Notes |
|---|---|---|---|
| ZC-01 | Skill lightweight dialogue | `not-run` |  |
| ZC-02 | Skill concept lookup | `not-run` |  |
| ZC-03 | Skill cross-domain explanation | `not-run` |  |
| ZC-04 | Explicit sub-agent Agama search | `not-run` |  |
| ZC-05 | Explicit sub-agent cross-domain research | `not-run` |  |
| ZC-06 | Long report output | `not-run` |  |
```
