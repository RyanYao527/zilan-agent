# Changelog

All notable changes to zilan-agent are tracked here. Platform validation status remains governed by `agents/openai.yaml` and `docs/platform-validation.md`.

## [Unreleased]

### Added

- Added a 2026-09-01 `SRQ-04` reviewer-decision ingestion-path note so future human semantic-boundary results can be recorded with dated evidence without changing current candidate conclusions, runtime status, provider routes, or platform validation status.
- Added `scripts/srq04_manual_review_packet.py` as a local Markdown/JSON packet for handing the three current `SRQ-04` XML-P5 no-self candidate sets to human reviewers without provider calls, runtime evidence, publication-ready claims, or platform-status changes.
- Added `scripts/reasoning_alignment_report.py` and a local `SRQ-01` / `ZR-06` alignment report so Agama evidence, Hetuvidya, Collected Topics, Madhyamaka, cognitive mapping, and practice-boundary coverage can be triaged independently without provider calls, semantic grading, or platform-status changes.
- Added a 2026-08-21 structured `SRQ-04` reviewer-decision intake fixture and summary-only evidence note so future human semantic-boundary decisions can be recorded without upgrading current limited theme-parallel evidence, runtime status, or platform validation status.
- Added a 2026-08-20 `SRQ-04` manual semantic-boundary review queue for the three existing XML-P5 no-self candidate sets, keeping them `manual_review_required` rather than textual-equivalence, source-dependence, publication-ready collation, runtime pass, or platform validation evidence.
- Added a 2026-08-20 local `SRQ-11` definition-violation marker replay over the committed Volcengine OpenAI-compatible answer excerpt, recording a calibrated pass without a new provider call, native OpenAI validation, prompt change, public API change, or platform-status change.
- Added a 2026-08-20 Volcengine OpenAI-compatible direct `SRQ-11` live spot answer excerpt and batch evidence, preserving the #202 pre-calibration exact-literal fail on missing `违②` without validating native OpenAI API or changing platform status.
- Added 2026-08-19 Claude Code direct `SRQ-06`, `SRQ-07`, `SRQ-10`, and `SRQ-11` runtime spot excerpts plus fail evidence, keeping all platform status unchanged.
- Added a local Claude Code route preflight helper and 2026-08-19 provider/smoke evidence note documenting the current custom-model blocker without provider calls, answer pass evidence, or platform-status changes.
- Added a 2026-08-19 `SRQ-04` manual collation boundary closeout note clarifying that located XML anchors and limited theme-parallel reviews remain `manual_review_required`, not textual equivalence, source-dependence, publication collation, runtime pass, or platform validation evidence.
- Added local `SRQ-11` definition-boundary prompt hardening for `性相过宽`, `唯在所表上成立`, `违②`, and `definiendum_boundary`, with runtime rerun pending and platform status unchanged.
- Added a 2026-08-19 summary-only `SRQ-11` post-hardening runtime rerun attempt note documenting a local Claude Code custom-model blocker, without creating answer pass evidence or changing platform status.
- Added a 2026-08-19 local `SRQ-06` / `SRQ-07` contract-calibration replay over committed runtime answer excerpts, keeping then-unresolved `SRQ-10` / `SRQ-11` fail evidence and all platform status unchanged.
- Added a 2026-08-19 local `SRQ-10` contract-calibration replay over the committed runtime answer excerpt, keeping `SRQ-11` fail evidence and all platform status unchanged.
- Added a 2026-08-19 local `SRQ-11` forbidden-collision replay over the committed runtime answer excerpt, clearing the shallow `性相成立` heading collision while preserving explicit fail evidence and all platform status unchanged.
- Added a 2026-08-19 limited cross-Agama XML-P5 no-self manual collation note and candidate-map entry for `SRQ-04`, without claiming textual equivalence, source dependence, publication-ready collation, runtime pass, or platform-status changes.
- Added a 2026-08-19 SRQ manual-review handoff and reviewer note for conservative `SRQ-04`, `SRQ-06`, `SRQ-07`, `SRQ-10`, and `SRQ-11` evidence disposition without provider calls or platform-status changes.
- Added `docs/architecture/zilan-reliability-pattern.md` to document `zilan_contract`, the runtime evidence manifest, and the SRQ/ZR coverage report as a reusable local reliability pattern without changing provider routes or platform status.
- Added a machine-readable runtime evidence manifest plus `scripts/srq_coverage_report.py` / `scripts/zilanlib/reasoning/srq_coverage_report.py` for local SRQ/ZR evidence coverage triage without provider calls or platform-status changes.
- Added `docs/zilan-contract-release-checklist.md` and a domain-neutral 60-second quickstart path clarifying that `zilan_contract` is a deterministic output-contract checker, not an LLM judge or semantic grader.
- Added two 2026-08-12 limited manual XML-P5 no-self parallel collation notes, guarded candidate-status validation, and negative fixture coverage preventing anchor-located spans from being treated as completed collation, without provider calls or platform-status changes.
- Added a 2026-08-10 Claude Code broad `ZC-05` runtime rerun answer excerpt and replay evidence showing `SRQ-01`, `SRQ-03`, `SRQ-04`, and `SRQ-08` all pass without platform-status changes.
- Added Markdown-line to CBETA XML-P5 anchor probes, a high-value no-self parallel candidate map, collation fixture validation, and a 2026-08-10 local replay evidence note without provider calls or platform-status changes.
- Added a local CBETA XML-P5 collation preflight helper and architecture note for checking the publication-level route from Agama Markdown back to committed XML sources without vector infrastructure, provider calls, or platform-status changes.
- Added Codex Desktop maintenance workflow documentation and a 2026-08-03 local maintenance smoke evidence note without changing platform validation status.
- Added `section_label` metadata validation for checked-in Agama retrieval chunks, fixture-review drift reporting, and citation checks so section anchors cannot silently drift from the source corpus.
- Added a 2026-08-07 local replay evidence note proving committed broad `ZC-05` excerpts and `SRQ-03` / `SRQ-08` samples expose the remaining `不立自宗`, `二谛`, and `proposition_decomposition` gaps, with `runtime pending` and no provider calls or platform-status changes.
- Added second-round broad `ZC-05` prompt hardening for `SRQ-03` / `SRQ-08` literal slots (`不立自宗`, `二谛`, and `proposition_decomposition`) with local prompt-invariant evidence and no provider calls or platform-status changes.
- Added a 2026-08-07 local `SRQ-01` contract-calibration replay showing the 2026-08-06 broad `ZC-05` answer passes direct `SRQ-01` review after heading-label calibration, without provider calls or platform-status changes.
- Added canonical Agama `section_label` metadata to search results and semantic fixture candidates so title-bearing local citations can preserve section anchors without provider calls or platform-status changes.
- Added a 2026-08-06 Claude Code broad `ZC-05` runtime spot evidence note and standalone answer excerpt replaying `SRQ-01`, `SRQ-03`, `SRQ-04`, and `SRQ-08`, recording `SRQ-04` pass plus remaining broad-answer explicitness gaps without platform-status changes and without validating native OpenAI API or OpenAI-compatible provider routes.
- Added prompt hardening for broad `ZC-05` answers to preserve integrated `SRQ-01` slots across Codex, Claude Code, Skill, and OpenAI metadata surfaces, with local prompt-invariant evidence and no provider calls or platform-status changes.
- Added a 2026-08-06 local replay of the existing broad `ZC-05` answer excerpt against the new integrated `SRQ-01` answer contract, recording the expected explicitness gap without provider calls or platform-status changes.
- Added `SRQ-01` cross-domain no-self answer-contract samples covering Agama evidence, Hetuvidya, Collected Topics, Madhyamaka prasaṅga, cognitive-analysis, and practice-boundary slots without provider calls or platform-status changes.
- Added `ZR-06` cross-domain no-self reasoning-case coverage to the `SRQ-01` semantic retrieval and context-bundle fixtures without provider calls or platform-status changes.
- Added provider preflight evidence guidance, a 2026-08-05 local OpenAI harness preflight smoke note, and a Codex Desktop handoff record without provider calls or platform-status changes.
- Added `scripts/openai_api_harness.py --preflight` so native OpenAI and OpenAI-compatible provider route configuration, credential presence, validation status, and status boundaries can be checked without provider calls or platform-status changes.
- Added installed-package CLI smoke coverage for invalid YAML and missing top-level `contracts` mappings, confirming packaged `zilan-contract` keeps schema-loading failures at exit code `2`.
- Added installed-package console script smoke coverage for the packaged `zilan-contract` entrypoint, confirming the `[project.scripts]` wrapper runs from outside the source checkout.
- Added wheel-install smoke coverage confirming public `zilan_contract` APIs, module CLI, console script, bundled answer fixtures, and medical-disclaimer examples work from outside the source checkout.
- Added `docs/architecture/zilan-contract-productization-closeout.md` to close the P2 productization sweep with package-surface completion criteria, verification guardrails, and non-goals.

### Changed

- Updated the reasoning alignment report with a local `--all` mode that summarizes every `SRQ-*` case, highlights `SRQ-01` / `ZR-06` as the current full-chain exemplar, and keeps `SRQ-04` manual-review-required boundaries visible without provider calls or platform-status changes.
- Updated the reasoning alignment report to count explicit answer-contract `practice_boundary` slots as practice-boundary evidence for `SRQ-09` / `SRQ-10`, while still preventing cognitive-mapping coverage from substituting for a missing practice boundary.
- Updated the `SRQ-04` manual review packet with machine-readable ingestion rules and per-candidate next actions, and require dated evidence notes for non-pending limited reviewer decisions.
- Tightened `SRQ-04` reviewer-decision intake validation so pending rows cannot carry stronger boundary claims and stronger textual-equivalence/source-dependence/publication-ready claims must cite a dated runtime-evidence note.
- Updated the Agama evidence checker and SRQ/ZR coverage report to expose `SRQ-04` reviewer-decision intake status counts and pending candidate-set IDs without changing candidate conclusions, runtime evidence, provider routes, or platform status.
- Updated the Agama evidence checker and reasoning contract runner output to expose manual collation boundary fields (`anchor_located`, `limited_theme_parallel`, textual-equivalence/source-dependence/publication-ready claims) without promoting `SRQ-04` answer-contract pass evidence into publication collation or platform status.
- Updated the SRQ/ZR coverage report to expose checked XML anchor status and manual collation boundary states, making `anchor_located`, `theme_parallel_only`, and `textual_equivalence_unreviewed` visible without treating `SRQ-04` as publication-ready or changing platform status.
- Updated SRQ/ZR coverage citation metadata to distinguish source-unavailable Agama section labels from missing fixture metadata, preserving `SRQ-04` manual-review status and platform boundaries.
- Updated the SRQ/ZR coverage report to expose Agama citation metadata triage, including CBETA IDs, line anchors,
  section-label gaps, line hashes, and related manual collation candidate sets without changing runtime evidence,
  provider routes, or platform status.
- Updated the fixture-only `SRQ-11` definition-boundary answer contract to accept exact marker alternatives `违②` or `违三要素校验之②`, while keeping agent prompt invariants on the literal `违②` unchanged.
- Updated `scripts/srq_coverage_report.py` Markdown and JSON output to group runtime evidence status by evidence class, making standalone answer excerpts, batch manifests, summary notes, and manual collation easier to distinguish.
- Updated `scripts/srq_coverage_report.py` to report clear machine-readable `fail` coverage when local runtime evidence has only fail statuses instead of folding those cases into `partial`.
- Updated the fixture-only `SRQ-10` cognitive-analysis answer contract to accept exact alias groups for attribution-error, motive-inference, affliction, and non-harm surfaces without changing prompts, provider routes, or `zilan_contract` public APIs.
- Narrowed the fixture-only `SRQ-11` forbidden phrase from the broad heading-colliding `性相成立` fragment to the explicit wrong assertion `这个性相成立`, while keeping required defining-mark boundary terms strict.
- Updated fixture-only semantic answer contracts to support exact required-term groups for narrow alias surfaces such as `不能决定` / `无法决定` and `摄类学` / `总与别`, without fuzzy matching, semantic grading, provider calls, or public `zilan_contract` API changes.
- Updated runtime evidence and maintenance documentation to treat `docs/runtime-evidence/index.md` as human navigation and `docs/runtime-evidence/evidence_manifest.yaml` as the machine-readable local evidence index.
- Refreshed public engineering metrics to the current 2026-09-01 local baseline of 342 tests, 84% zilanlib coverage, and 74 mypy-checked source files.

- Calibrated the integrated `SRQ-01` answer contract so heading-like labels (`阿含证据`, `代表性检索`, `因明校验`) are no longer mandatory global literals when concrete Agama and Hetuvidya surfaces are present.
- Tightened broad `ZC-05` minimum-template prompt wording and narrowed the `SRQ-01` nihilism forbidden phrase to avoid a shallow collision with negated causality-boundary wording.
- Expanded `docs/zilan-contract-schema.md` with CLI/Python schema shapes, exact matching semantics, schema-error examples, issue kinds, unsupported v2.5.7 features, and CI exit-code guidance without changing runtime behavior or platform validation status.
- Updated `docs/zilan-contract-quickstart.md` and `docs/maintenance-roadmap.md` to document installed-package, console-script, and wheel-install verification boundaries for the closed productization surface.
- Clarified `docs/maintenance-roadmap.md` to mark `zilan_contract` productization complete, list remaining package/platform/collation boundaries, and set reasoning/retrieval quality as the next mainline.

## [2.5.7] - 2026-08-04

### Added

- Added productized `zilan_contract` public result helpers, a domain-neutral answer-contract runner, CLI/report output with machine-readable issue details, a contract schema reference, reusable medical/legal/financial examples, and installed-package smoke coverage without provider calls or platform-status changes.

### Changed

- Extracted reasoning-case schema validation into `scripts/zilanlib/validation/reasoning_cases.py` while preserving `scripts/validate_zilan_repo.py` compatibility aliases and CLI behavior.
- Extracted regression-case schema validation into `scripts/zilanlib/validation/regression_cases.py` while preserving `scripts/validate_zilan_repo.py` compatibility aliases and CLI behavior.
- Extracted retrieval-chunk fixture validation into `scripts/zilanlib/validation/retrieval_chunks.py` while preserving `scripts/validate_zilan_repo.py` compatibility aliases and CLI behavior.
- Extracted Agama corpus search and generated Markdown validation into `scripts/zilanlib/validation/agama_corpus.py` while preserving `scripts/validate_zilan_repo.py` compatibility aliases and CLI behavior.
- Extracted public documentation validation into `scripts/zilanlib/validation/public_docs.py` while preserving `scripts/validate_zilan_repo.py` compatibility aliases and CLI behavior.
- Extracted repository metadata validation into `scripts/zilanlib/validation/repository_metadata.py` while preserving `scripts/validate_zilan_repo.py` compatibility aliases and CLI behavior.
- Extracted platform YAML metadata guard validation into `scripts/zilanlib/validation/platform.py` while preserving `scripts/validate_zilan_repo.py` compatibility aliases and CLI behavior.
- Extracted validation suite orchestration into `scripts/zilanlib/validation/suite.py` while preserving `scripts/validate_zilan_repo.py` CLI behavior and `run_checks` compatibility.
- Added an entrypoint compatibility alias manifest and CLI-only structure guard for `scripts/validate_zilan_repo.py`.
- Documented the P1 validation cleanup closeout in `docs/architecture/zilanlib-extraction-cleanup-review.md`, including the finalized module split and next quality-maintenance direction.
- Added focused reasoning-case validation coverage for minimal valid Hetuvidya fixtures, duplicate ZR ids, and top-level metadata errors.
- Added focused retrieval-chunk validation coverage for minimal valid fixtures, duplicate ids, and answer sample path boundaries.
- Expanded reasoning-case validation coverage for invalid contracts, malformed case metadata, and non-Hetuvidya expected-output shapes.
- Added validation-suite orchestration coverage for stable validator order, shared failure/warning state, strict YAML flag forwarding, and generated-Agama gating.
- Refreshed public engineering metrics to the current local baseline of 237 tests, 85% zilanlib coverage, and 62 mypy-checked source files.

### Fixed

- Rejected malformed `zilan_contract` public contract schemas instead of allowing scalar or empty checks to pass silently, and expanded Markdown reports with issue details.
- Ignored local `build/` artifacts during mock Claude Code install smoke copies so stale packaging output cannot break repository-level pytest runs.

## [2.5.6] - 2026-07-30

### Added

- Added 2026-07-30 post-alignment answer-review replay evidence covering the existing 2026-07-17 and 2026-07-20 batch manifests, confirming no missing structured validator cases after the #150/#151 alignment reporting changes without provider calls or platform-status changes.
- Added `zilan_contract` standalone package: a clean public API (`ContractRunner`, `HetuvidyaValidator`, `ContractResult`) with bundled fixtures, `py.typed` marker, and a `docs/zilan-contract-quickstart.md` guide covering 60-second try and custom contract authoring.
- Added `docs/article-output-contracts.md`: a ~1,970-word technical article pitching the output-contract + deterministic-validator pattern to an LLM engineering audience, with concrete code examples, pass/fail samples, and a domain-generalization table.
- Added `docs/awesome-list-pr-entries.md`: pre-written PR entries for four curated awesome lists (`awesome-claude-skills`, `Awesome-Prompt-Engineering`, `awesome-agents`, `Awesome-LLM`) with descriptions and submission checklists.
- Added `docs/codex-manual-tasks.md`: a four-task manual-operation checklist (record demo GIF, upload HF dataset, submit awesome-list PRs, publish article) designed for Codex to execute autonomously.
- Added `scripts/hf_upload_dataset.py`: a HuggingFace Dataset upload script that packages the Agama corpus (1,844 passages) and six knowledge-base files with a dataset card, dry-run mode, and interactive repo-id prompting.
- Added `scripts/demo.sh` and `scripts/demo.tape`: a 60-second CLI demo script (asciinema-compatible) and a vhs tape definition for recording terminal GIFs.
- Added a four-tier contributor ladder (`🪜 贡献者阶梯` / `Contributor Ladder`) to `CONTRIBUTING.md` and `CONTRIBUTING-en.md`, with concrete first tasks for Evidence Runner (L1), Documentation Reviewer (L2), Contract Reviewer (L3), and Code Contributor (L4).
- Added a "For Engineers" section to `README.md`, pitching the output-contract pattern and engineering metrics (185 tests, 86% coverage, mypy/ruff clean) to LLM reliability engineers before the Buddhist-domain content.

### Changed

- Propagated answer-validator alignment status into single and batch reasoning answer reviews so reports distinguish answer-surface failures from missing structured validator cases.
- Added a reasoning contract runner answer-validator alignment guard so a passing answer contract now fails the run if the corresponding structured validator role has no selected reasoning case.
- Consolidated reasoning contract runner validator dispatch into a single internal spec table, preserving the stable CLI/API output while reducing future validator wiring drift.
- Updated public Skill script inventories for `scripts/hf_upload_dataset.py` after the Hugging Face dataset helper landed on `main`.
- Extracted agent prompt contract checks into `scripts/zilanlib/validation/agent_prompts.py` while preserving `scripts/validate_zilan_repo.py` compatibility aliases and CLI behavior.
- Extracted platform metadata and platform-validation document checks into `scripts/zilanlib/validation/platform.py` while preserving `scripts/validate_zilan_repo.py` compatibility aliases and CLI behavior.
- Standardized `from __future__ import annotations` across scripts and tests, with a repository convention test guarding future Python files.
- Extracted runtime-evidence repository validation into `scripts/zilanlib/validation/runtime_evidence.py` while preserving `scripts/validate_zilan_repo.py` compatibility aliases and CLI behavior.
- Reused `zilanlib.yaml_io.load_yaml_mapping()` in the OpenAI API harness while preserving dry-run request behavior and adding private-loader YAML error coverage.
- Replaced duplicated reasoning contract runner not-applicable test constants with a behavior-preserving factory helper.
- Scoped pytest coverage reporting to `scripts/zilanlib`, with a 2026-07-23 local baseline of 87%, while keeping root CLI wrapper tests in the suite.
- Marked `zilanlib` as a typed package and added package discovery, package-data, project URLs, and classifier metadata.
- Updated `pyproject.toml` with keywords, classifiers, `zilan_contract` package discovery, fixture package-data, and mypy/ruff/coverage inclusion for the new top-level package.
- Synced `SKILL-en.md` with `SKILL.md`: added missing Collected Topics total/part boundary output contract, cognitive-analysis & vipassanā practice boundary output contract, and Agent Mode sections.
- Added `.coverage` to `.gitignore`.

### Fixed

- Bundled answer sample Markdown fixtures in the `zilan_contract` wheel, made installed-package Agama local source-anchor checks report `not_applicable` without a source checkout, and added installed-package smoke coverage so `ContractRunner` quickstart `sample_id` and `answer_text` paths work outside a source checkout.
- Fixed `zilan_contract` fixture path (`_SEMANTIC_FIXTURE` missing `retrieval_chunks/` component) so `ContractRunner` works in pip-installed mode.
- Fixed `scripts/demo.sh` stderr pollution (`2>&1` before JSON pipe) that could corrupt `json.load`.
- Fixed incorrect validator line-count claim (~170 → ~200–256, Agama evidence checker 430) in `docs/article-output-contracts.md`.
- Fixed `docs/zilan-contract-quickstart.md` custom-contract tutorial: corrected YAML field formats (`query_id` → `id`, `required_slots` as dict list) and resolved fixture filename inconsistency.
- Added `zilan_contract` to mypy `files`, ruff `include`, and coverage measurement.

## [2.5.5] - 2026-07-21

### Added

- Added repository validation for `docs/runtime-evidence/index.md` references and runtime answer-review batch `answer_file` safety so stale evidence links and summary-only answer inputs are caught before merge.
- Added `scripts/reasoning_answer_review.py` and `scripts/zilanlib/reasoning/answer_review.py` as a compact, fixture-only answer review layer over the reasoning contract runner, preserving stable local CLI behavior without provider calls or platform-status changes.
- Added `scripts/reasoning_answer_review_batch.py` and `scripts/zilanlib/reasoning/answer_review_batch.py` to run compact answer reviews from a YAML batch manifest for transcript/excerpt review workflows without provider calls.
- Added a 2026-07-17 reasoning answer review batch manifest and evidence excerpt for committed `SRQ-04`, `SRQ-08`, `SRQ-09`, and `SRQ-11` pass samples; no provider calls or platform-status changes.
- Added a 2026-07-17 runtime answer excerpt batch manifest and evidence excerpt for committed Claude Code `SRQ-02`, `SRQ-03`, `SRQ-04`, `SRQ-05`, and broad `ZC-05` answer excerpts; no provider calls or platform-status changes.
- Added a runtime evidence capture policy for standalone contract-reviewable `*-answer.md` excerpts, with repository validation guarding against using summary-only evidence as `answer_file` input.
- Added 2026-07-14 standalone Claude Code `ZC-03`, post-#126 `ZC-04`, post-#124 `ZC-05`, and redacted `ZC-06` main-answer excerpts, plus a 2026-07-20 batch review showing the contract-reviewable excerpts pass `SRQ-09`, `SRQ-04`, `SRQ-03`, and `SRQ-08`; no provider calls or platform-status changes.
- Added 2026-07-14 standalone compact `SRQ-04` / `ZC-04` Agama answer excerpts plus a 2026-07-20 progression batch showing the direct `SRQ-04` pass, the pre-#119 compact `ZC-04` shallow-contract fail, and the post-#119 compact `ZC-04` pass; no provider calls or platform-status changes.
- Added `docs/runtime-evidence/index.md` to classify summary evidence, standalone answer excerpts, batch manifests, batch reports, provider smoke evidence, and `answer_file`-safe review inputs without changing platform status.

## [2.5.4] - 2026-07-15

### Added

- Added Claude Code post-#126 broad `ZC-04` runtime rerun evidence showing the `SRQ-04` Agama citation-boundary contract now passes after prompt hardening.
- Added Claude Code post-#124 broad boundary runtime spot-review evidence: broad `ZC-05` now passes `SRQ-03`, `SRQ-04`, and `SRQ-08`, while broad `ZC-04` still misses exact `SRQ-04` search-scope / `T02n0099` slots; no platform status change.
- Added Claude Code post-prompt `ZC-01` through `ZC-06` rerun evidence after root-document archival and closing Dharma-seal wording changes; all invocations succeeded, while broad `ZC-04`/`SRQ-04` and `ZC-05`/`SRQ-08` contract gaps remain follow-up work without platform status change.
- Replaced the old closing verse across public docs, Skill files, agent prompts, and archives with `诸行无常，诸法无我，涅槃寂静。`.
- Archived the legacy manual upload guide and early communication-history document under `docs/archive/`, and removed them from root-level public documentation surfaces.
- Added Claude Code compact `ZC-04` Agama boundary rerun evidence showing the post-wording-fix answer passes `SRQ-04` without forbidden collation-overclaim terms; no platform status change.
- Added Claude Code `SRQ-04` / compact `ZC-04` Agama citation-boundary spot-review evidence after Agama section-title citation metadata work; direct `SRQ-04` passes and compact `ZC-04` exposes a shallow forbidden-term nuance for negated `校勘确认` wording without changing platform status.
- Added `section_title` metadata to Agama search results and semantic fixture candidates so title-bearing section markers such as `（一）第一分初大本經第一` are preserved in citations when available.
- Updated the maintenance roadmap coverage baseline from 75% to 76% after adding citation-title coverage for Agama search and candidate generation.
- Updated the maintenance roadmap coverage baseline from 72% to 75% after adding `scripts/build_agama_context.py` smoke coverage.
- Added fixture-safe unit coverage for `scripts/build_agama_context.py` metadata extraction, text normalization, index writing, and temp-source main flow.

### Fixed

- Hardened broad ZC-04 Agama prompt wording so main responses must include a compact evidence summary even when a full report is saved elsewhere or produced by a spawned Agent.
- Narrowed the `SRQ-03` Madhyamaka forbidden term from bare `断灭` to the nihilistic phrase `断灭的结论`, avoiding conflict with `SRQ-08` boundary wording that must mention `断灭` explicitly.
- Tightened broad `ZC-04` / `ZC-05` agent prompt contracts so main responses preserve `SRQ-04` Agama citation-boundary slots and `SRQ-08` Madhyamaka nihilism-boundary slots even for summaries or file-output tasks.
- Tightened Agama evidence prompt wording so agents avoid reusing shallow collation-overclaim trigger phrases even in negated boundary statements; preferred wording now uses `未作校勘定案，不能作为定本使用`.
- Fixed `scripts/build_agama_context.py` TEI `choice` handling so `corr` elements without child nodes are preserved and `choice` tail text is not duplicated.

## [2.5.3] - 2026-07-13

### Added

- Updated the maintenance roadmap coverage baseline from 61% to 72% after the root CLI wrapper smoke-test sweep.
- Added in-process Agama semantic fixture CLI wrapper smoke tests for candidate generation and fixture review helpers.
- Added in-process reasoning CLI wrapper smoke tests for fixture validators, the reasoning contract runner, and the validator-output compatibility shim.
- Added in-process root CLI wrapper smoke tests for semantic helper scripts and the Agama compatibility wrapper so pytest-cov tracks wrapper coverage.
- Extracted a shared document-fragment validation helper into `scripts/zilanlib/text_checks.py` while preserving existing repository invariant error messages.

## [2.5.2] - 2026-07-13

### Added

- Extracted repository path/version/regression-matrix helpers into `scripts/zilanlib/repository.py` while keeping `validate_zilan_repo.py` wrapper names stable.
- Extracted repository YAML loading/list-shape helpers into `scripts/zilanlib/yaml_io.py` while keeping `validate_zilan_repo.py` behavior and private helper aliases stable.
- Added `pytest-cov` as a development dependency and enabled an all-scripts coverage report without a fail-under gate; the initial local baseline is 61% and is tracked in the maintenance roadmap.
- Added co-maintainer invitation sections to the root, Chinese, and English READMEs, plus co-maintainer role expectations in both contributing guides.
- Added `CODE_OF_CONDUCT.md` based on Contributor Covenant 2.1 and linked it from README and contributing guides.
- Added GitHub issue templates for bug reports and feature requests so contributors can report platform, validation, documentation, and reasoning-contract work through structured forms.
- Added ARCHITECTURE.md as a concise contributor-facing architecture entrypoint covering the Skill/Agent dual track, fixture-only validators, zilanlib, platform validation boundaries, and local validation workflow.
- Added Claude Code SRQ-11 runtime spot-review evidence showing the current answer passes the Collected Topics definition-scope answer contract for the too-broad defining mark `瓶的性相是能盛水者`; no platform status change.
- Added SRQ-11 / ZR-12 as a fixture-only Collected Topics definition-scope case for the too-broad defining mark 瓶的性相是能盛水者, covering 性相, 所表, 性相过宽, 唯在所表上成立, and checked-in pass/fail answer-contract samples.

## [2.5.1] - 2026-07-13

### Added

- Added a `zilanlib` extraction cleanup review that classifies root scripts, closes the current helper-extraction sweep, and identifies release hygiene as the next highest-ROI maintenance step.
- Extracted semantic context-bundle construction into `scripts/zilanlib/semantic/context_bundle.py` while keeping `scripts/semantic_context_bundle.py` as the stable CLI wrapper.
- Extracted semantic role-coverage review into `scripts/zilanlib/semantic/role_coverage.py` while keeping `scripts/semantic_role_coverage.py` as the stable CLI wrapper.
- Extracted semantic answer-boundary review into `scripts/zilanlib/semantic/answer_boundary_review.py` while keeping `scripts/semantic_answer_boundary_review.py` as the stable CLI wrapper.
- Extracted semantic answer-contract review into `scripts/zilanlib/semantic/answer_contract_review.py` while keeping `scripts/semantic_answer_contract_review.py` as the stable CLI wrapper.
- Extracted semantic retrieval dry-run construction into `scripts/zilanlib/semantic/retrieval_dry_run.py` while keeping `scripts/semantic_retrieval_dry_run.py` as the stable CLI wrapper.
- Extracted reasoning contract runner construction into `scripts/zilanlib/reasoning/contract_runner.py` while keeping `scripts/reasoning_contract_runner.py` as the stable CLI wrapper.
- Extracted Hetuvidya validator construction into `scripts/zilanlib/reasoning/hetuvidya_validator.py` while keeping `scripts/hetuvidya_validator.py` as the stable CLI wrapper.
- Extracted Collected Topics analyzer construction into `scripts/zilanlib/reasoning/collected_topics_analyzer.py` while keeping `scripts/collected_topics_analyzer.py` as the stable CLI wrapper.
- Extracted Madhyamaka critique engine construction into `scripts/zilanlib/reasoning/madhyamaka_critique_engine.py` while keeping `scripts/madhyamaka_critique_engine.py` as the stable CLI wrapper.
- Extracted cognitive-analysis mapper construction into `scripts/zilanlib/reasoning/cognitive_analysis_mapper.py` while keeping `scripts/cognitive_analysis_mapper.py` as the stable CLI wrapper.
- Extracted Agama evidence checker construction into `scripts/zilanlib/reasoning/agama_evidence_checker.py` while keeping `scripts/agama_evidence_checker.py` as the stable CLI wrapper.
- Extracted the shared reasoning-validator output envelope into `scripts/zilanlib/reasoning/validator_output.py` while keeping `scripts/reasoning_validator_output.py` as the compatibility shim.

- Extracted semantic fixture review comparison into `scripts/zilanlib/agama/fixture_review.py` while keeping `scripts/semantic_fixture_review.py` as the stable CLI wrapper.
- Extracted Agama semantic fixture candidate construction into `scripts/zilanlib/agama/candidates.py` while keeping `scripts/semantic_fixture_candidates.py` as the stable CLI wrapper.
- Extracted reusable Agama search APIs into `scripts/zilanlib/agama/search.py` while keeping `scripts/search_agama.py` as the stable CLI wrapper and compatibility surface.
- Added `scripts/zilanlib/` shared helpers and moved repeated YAML mapping loading for fixture-based validators into `zilanlib.yaml_io`.
- Added a minimal mypy type-check baseline for `scripts/`, including dev dependency, CI step, local command docs, and maintenance-roadmap guardrails.

## [2.5.0] - 2026-07-09

### Added

- Added PyYAML as a runtime dependency and expanded the public Skill script inventory with repository validation so listed scripts stay aligned with scripts/*.py.
- Added third-party notices and top-level license-scope wording for CBETA-derived Agama corpus files and excerpts.
- Added Reasoning Contract v0 documentation and seed `ZR-*` reasoning fixtures for Hetuvidya, Collected Topics, Madhyamaka prasaṅga, cognitive-analysis, and Agama-evidence structures.
- Added a retrospective ZC-to-ZR reasoning-contract review that maps existing ZC-02, ZC-03, and ZC-05 evidence without claiming a new runtime validation pass.
- Added a semantic retrieval interface sketch for future citation-preserving chunks while preserving `scripts/search_agama.py` as the stable baseline.
- Added fixture-only semantic retrieval chunks and repository validation for source-file existence, line-range sanity, local citation anchors, reasoning roles, and dry-run query chunk references.
- Added a fixture-only semantic retrieval dry-run helper that returns expected chunks for query fixtures without embeddings, vector storage, reranking, or provider calls.
- Added an Agama semantic fixture candidate generator that converts `search_agama.py` keyword-baseline hits into citation-preserving `agama_passage` chunk candidates.
- Expanded `scripts/semantic_fixture_candidates.py` candidate metadata with explicit `line_text_hash` and provenance fields while preserving `source_hash` as a legacy line-text hash alias.
- Added repository validation for checked-in Agama semantic chunk provenance hashes, matched lines, and source-script metadata.
- Added a semantic fixture review helper that compares generated Agama candidates with the checked-in fixture without auto-overwriting YAML.
- Expanded the semantic fixture review helper to report provenance/hash drift between generated Agama candidates and checked-in chunks without writing fixtures.
- Expanded `SRQ-04` Agama evidence fixture coverage with a reviewed `長阿含經` 卷 10 three-feelings non-self passage selected from the fixture review workflow.
- Expanded `SRQ-01` semantic retrieval fixture coverage with reviewed `長阿含經` Agama chunks selected from the fixture review workflow.
- Added a fixture-only semantic context-bundle dry run that assembles selected chunks into prompt-ready order.
- Added a fixture-only semantic role-coverage review that compares query `needs` with selected chunk `reasoning_roles`.
- Expanded `SRQ-01` semantic role fixture coverage with Collected Topics and Madhyamaka prasaṅga context chunks, while keeping `practice_boundary` as a non-chunk answer boundary need.
- Added a fixture-only semantic answer-boundary review for `practice_boundary` so downstream answer text can be checked without treating boundary guidance as retrieval evidence.
- Added a checked-in `SRQ-01` answer-boundary sample fixture and `--sample-id` review path so boundary checks can run without inline CLI answer text.
- Added a checked-in negative `SRQ-01` answer-boundary sample so committed sample review covers expected `pass` and `fail` outcomes.
- Added `SRQ-02` as a fixture-only Hetuvidya error-detection query for the `ZR-03` `reason_unestablished` case.
- Added fixture-only `SRQ-02` answer-contract review with checked-in pass/fail samples for Hetuvidya error detection.
- Added `SRQ-03` as a fixture-only Madhyamaka prasaṅga boundary query with checked-in pass/fail answer-contract samples.
- Added `SRQ-04` as a fixture-only Agama citation-boundary query with checked-in pass/fail answer-contract samples.
- Added a post-contract runtime evidence review that checks existing ZC-02/ZC-03/ZC-05 summaries against SRQ-02 through SRQ-04 without changing platform status.
- Added Claude Code UTF-8 target-review evidence for `SRQ-02`, `SRQ-03`, `SRQ-04`, and `ZC-05`, including committed answer excerpts and contract-review results.
- Added repository validation for `tests/reasoning_cases.yaml` schema, local references, allowed contract families, and boundary-statement fields without changing runtime platform status.
- Added an explicit Agama evidence output contract to agent prompts and OpenAI metadata, requiring search scope, CBETA/local `context/agama/` anchors, representative-status wording, and collation boundaries.
- Added an explicit Madhyamaka prasaṅga output contract to agent prompts and OpenAI metadata so broad answers preserve `对方承许`, `归谬`, `自性有`, `缘起`, `矛盾`, and `不立自宗` boundaries.
- Added Claude Code post-contract full `ZC-01` through `ZC-06` rerun evidence after the Agama and Madhyamaka output-contract fixes.
- Added answer-contract v0.1 required slots so fixture reviews can check shallow answer structure in addition to required and forbidden terms.
- Added `SRQ-05` / `ZR-07` as a fixture-only Hetuvidya `不周遍` error-detection case for “声，应是无常，以是所知故”.
- Added `SRQ-06` / `ZR-08` as a fixture-only Hetuvidya `不定因` error-detection case for “声，应是常，以是所知故”.
- Added a minimal `scripts/hetuvidya_validator.py` prototype that reads structured `tests/reasoning_cases.yaml` Hetuvidya fixtures and emits deterministic validation results without model calls or natural-language parsing.
- Added `SRQ-07` as a fixture-only Collected Topics total/part error case for local-feedback-to-whole-self overgeneralization.
- Added `SRQ-08` / `ZR-09` as a fixture-only Madhyamaka nihilism-boundary case that rejects reading emptiness as cancellation of dependent arising or causality.
- Expanded `scripts/hetuvidya_validator.py` with `hetuvidya-validator-output-v0.1`, including structured trairupya checks, judgment status, and diagnostics while preserving existing fields.
- Added `scripts/reasoning_contract_runner.py` as a fixture-only runner that combines semantic retrieval dry runs, role coverage, answer-contract review, and the Hetuvidya validator without provider calls or platform-status changes.
- Added Claude Code `SRQ-08` / `ZC-05` runtime spot-review evidence showing the current answers still need more explicit nihilism-boundary wording for the `SRQ-08` contract; no platform status change.
- Tightened the Madhyamaka nihilism-boundary prompt contract across Skill, Codex, Claude Code, and OpenAI metadata so emptiness/no-self/dependent-arising answers explicitly preserve `只破自性有`, `断灭`, and `二谛` boundaries.
- Tightened the Collected Topics total/part prompt contract and `SRQ-07` answer fixture so work-feedback overgeneralization answers explicitly preserve `总与别`, `局部别法`, `整体总法`, `总别混淆`, `不周遍`, and `不成立` boundaries.
- Added `SRQ-09` / `ZR-10` as a fixture-only cognitive-analysis and practice-boundary case for work-feedback distress, covering the five-universal chain, cognitive-quality downgrade, corrective mental factors, vipassana mapping, and non-clinical practice boundaries.
- Added Claude Code `SRQ-09` / `ZC-03` runtime spot-review evidence showing current answers still need more explicit cognitive-quality, vipassana-mapping, and non-clinical practice-boundary wording for the `SRQ-09` contract; no platform status change.
- Tightened the heart/mind cognitive-analysis and vipassana practice-boundary prompt contract across Skill, Codex, Claude Code, and OpenAI metadata so work-feedback answers explicitly preserve `颠倒知`, `犹豫识`, `比量`, `念`, `慧`, `无瞋`, `行舍`, `名色分别`, `缘摄受`, `三相印证`, `非心理治疗`, and `善知识指导` boundaries.
- Added Claude Code SRQ-09 boundary-fix spot evidence showing both direct SRQ-09 and broad ZC-03 answers pass the cognitive practice-boundary contract after prompt tightening; no platform status change.
- Added SRQ-10 / ZR-11 as a fixture-only cognitive-analysis and practice-boundary case for caregiving-pressure attribution, covering the five-universal chain, attribution error, affliction chain, corrective mental factors, vipassana mapping, and non-clinical practice boundaries.
- Added a minimal `scripts/cognitive_analysis_mapper.py` prototype that reads structured cognitive-analysis fixtures and emits deterministic five-universal, affliction, corrective-factor, and practice-boundary mappings without model calls or natural-language parsing.
- Integrated the cognitive-analysis mapper into `scripts/reasoning_contract_runner.py` so `SRQ-09` and `SRQ-10` now expose structured cognitive mappings under `validators.cognitive_analysis`.
- Added a minimal `scripts/collected_topics_analyzer.py` prototype that reads structured Collected Topics fixtures and emits deterministic `concepts`, `relation_checks`, and `error_type` analyses without model calls or natural-language parsing.
- Integrated the Collected Topics analyzer into `scripts/reasoning_contract_runner.py` so `SRQ-07` / `ZR-02` now exposes structured total/part and non-pervasion analysis under `validators.collected_topics`.
- Added a minimal `scripts/madhyamaka_critique_engine.py` prototype that reads structured Madhyamaka prasaṅga fixtures and emits deterministic opponent-premise, accepted-commitment, contradiction, no-independent-thesis, critique-step, and diagnostic critiques without model calls or natural-language parsing.
- Integrated the Madhyamaka critique engine into `scripts/reasoning_contract_runner.py` so Madhyamaka query fixtures such as `SRQ-08` / `ZR-09` expose structured prasaṅga critiques under `validators.madhyamaka_prasanga`.
- Added a shared reasoning-validator output envelope so Hetuvidya, Collected Topics, Madhyamaka, cognitive-analysis, and runner validator outputs expose consistent `status`, `validator`, `contract_family`, `source`, `case_ids`, `count`, and `limitations` fields without changing provider or platform status.
- Added a minimal `scripts/agama_evidence_checker.py` prototype that reads structured Agama evidence fixtures and emits deterministic citation, search-scope, local-reference, and collation-boundary checks without running search or changing platform status.
- Integrated the Agama evidence checker into `scripts/reasoning_contract_runner.py` so `SRQ-04` / `ZR-05` exposes structured citation-boundary analysis under `validators.agama_evidence`.
- Expanded `scripts/agama_evidence_checker.py` to `agama-evidence-checker-output-v0.1` with local evidence checks for checked-in semantic Agama chunks, local Markdown files, CBETA IDs, line ranges, and fixture text anchors without running search or changing platform status.
- Added a negative Agama local-anchor fixture covering bad line ranges, mismatched CBETA IDs, and missing text anchors so the checker fails deterministically on broken evidence metadata.

## [2.4.8] - 2026-06-17

### Added

- Added `--provider-route` support to the OpenAI-compatible harness, with tested Volcengine defaults loaded from `agents/openai.yaml`.
- Added redacted Volcengine OpenAI-compatible ZC-01 and ZC-03 live evidence, extending the route's live coverage to ZC-01 through ZC-03.

### Changed

- Updated README compatibility summaries to match `docs/platform-validation.md`: Codex and Claude Code are tested, Volcengine OpenAI-Compatible is tested only for ZC-01 through ZC-03, and native OpenAI API remains `harness-ready`.

## [2.4.7] - 2026-06-16

### Added

- Added compact runtime evidence excerpts for the 2026-06-15 Codex rerun and 2026-06-16 Claude Code UTF-8 rerun.
- Added OpenAI-compatible harness configuration for custom base URLs, API surfaces, and provider-specific key environment variables.
- Added a Volcengine OpenAI-compatible route without upgrading native OpenAI API status.
- Added a redacted Volcengine OpenAI-compatible ZC-02 live evidence excerpt.

### Changed

- Improved Agama search citations by carrying paragraph section markers such as `（一）` into line and passage citations when available.
- Promoted the Volcengine OpenAI-compatible route to `tested` for the 2026-06-16 ZC-02 live run, while keeping native OpenAI API `harness-ready`.

## [2.4.6] - 2026-06-16

### Changed

- Restored Claude Code to `tested` after a 2026-06-16 UTF-8 stdin rerun showed the blocker was caused by Windows PowerShell pipe encoding, not the ZC prompt contract itself.
- Added a Claude Code output hard-constraint guard so concrete tasks cannot start with identity greetings, verse openers, or capability-menu prompts.
- Updated platform validation, provider route triage, runtime validation, and maintenance docs for the Claude Code UTF-8 stdin protocol.

### Added

- Added repository validation for the Claude Code output hard-constraint prompt section.

## [2.4.5] - 2026-06-15

### Changed

- Depersonalized public Skill, README, and Agent prompt descriptions by replacing private/autobiographical scenes with reusable application examples.
- Added explicit material-layer boundaries so doctrine, method metaphors, application examples, and historical notes are not conflated.
- Updated core context examples and regression prompts to use neutral daily-practice scenarios.
- Clarified that activation keywords combined with concrete questions must be answered directly instead of stopping at identity greetings.
- Recorded the 2026-06-15 Codex rerun and downgraded Claude Code to `blocked` pending a wake-word / noninteractive route fix.

### Added

- Added repository validation for high-risk private/autobiographical fragments in public docs and prompt files.
- Added agent prompt validation for the activation/task merge contract.

## [2.4.4] - 2026-06-15

### Added

- Added `scripts/mock_install_smoke.py` to validate the Claude Code skill/agent install layout in a temporary mock home.
- Added pytest coverage and CI smoke testing for the mock Claude install path.
- Added runtime evidence for the mock install smoke.

### Changed

- Updated installation and engineering-check docs to include mock install validation.

## [2.4.3] - 2026-06-15

### Added

- Added `docs/runtime-evidence/` for small redacted validation excerpts.
- Added command-output evidence for the 2026-06-15 clean install smoke test.
- Added an evidence template for future runtime or provider validation excerpts.

### Changed

- Linked runtime validation log entries to committed evidence excerpts where available.
- Added invariant checks for the runtime evidence directory.

## [2.4.2] - 2026-06-15

### Changed

- Rewrote `AGENT_UPGRADE_PORTABLE.md` as a current Skill-to-Agent migration record instead of an obsolete v2.3 implementation note.
- Clarified that the historical DeepSeek Anthropic-compatible caveat is not native DeepSeek route validation.
- Recorded a clean clone installation smoke test in `docs/runtime-validation-log.md`.
- Added invariant checks for current migration-record fragments.

## [2.4.1] - 2026-06-15

### Added

- Added `docs/installation.md` with separate Codex, Claude Code, and OpenAI API operating paths.
- Added `docs/validation-evidence.md` to define runtime evidence levels, transcript redaction, and status-promotion rules.
- Added `docs/provider-routes.md` to triage OpenAI API, DeepSeek, GLM, and Qwen route status without overclaiming live validation.
- Added this changelog as the release summary surface for future project updates.

### Changed

- Updated README and maintenance docs to point to installation, evidence, provider-route, and changelog documents.
- Kept OpenAI API live validation intentionally last; the route remains `harness-ready` until a live `OPENAI_API_KEY` run is recorded.
- Kept DeepSeek, GLM, and Qwen conservative at `config-only` pending native harnesses or dated runtime evidence.

## [2.4.0] - 2026-06-12

### Added

- Added a minimal OpenAI Responses API harness with dry-run and live modes.
- Added pytest coverage and CI smoke testing for the OpenAI API harness.
- Added `docs/openai-api-harness.md`.

### Changed

- Marked Claude Code as `tested` after a ZC-01 through ZC-06 runtime rerun.
- Updated repository metadata, README status text, and platform validation records.
- Updated the Claude Code agent prompt to prefer repository-local `scripts/` and `context/` paths when available.

## [2.3.1] - 2026-06-12

### Changed

- Filtered additional Agama search false positives.
- Preserved stable citation output for downstream prompt contracts.

## [2.3.0] - 2026-06-10

### Added

- Added Codex and Claude Code agent prompts.
- Added platform validation documents, runtime validation log, maintenance roadmap, and regression matrix.
- Added Agama search and repository validation tooling.
