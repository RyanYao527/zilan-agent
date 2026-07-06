# Runtime Validation Log

> Last updated: 2026-07-06

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
