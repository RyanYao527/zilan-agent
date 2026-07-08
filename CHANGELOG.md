# Changelog

All notable changes to zilan-agent are tracked here. Platform validation status remains governed by `agents/openai.yaml` and `docs/platform-validation.md`.

## [Unreleased]

### Added

- Added Reasoning Contract v0 documentation and seed `ZR-*` reasoning fixtures for Hetuvidya, Collected Topics, Madhyamaka prasaṅga, cognitive-analysis, and Agama-evidence structures.
- Added a retrospective ZC-to-ZR reasoning-contract review that maps existing ZC-02, ZC-03, and ZC-05 evidence without claiming a new runtime validation pass.
- Added a semantic retrieval interface sketch for future citation-preserving chunks while preserving `scripts/search_agama.py` as the stable baseline.
- Added fixture-only semantic retrieval chunks and repository validation for source-file existence, line-range sanity, local citation anchors, reasoning roles, and dry-run query chunk references.
- Added a fixture-only semantic retrieval dry-run helper that returns expected chunks for query fixtures without embeddings, vector storage, reranking, or provider calls.
- Added an Agama semantic fixture candidate generator that converts `search_agama.py` keyword-baseline hits into citation-preserving `agama_passage` chunk candidates.
- Added a semantic fixture review helper that compares generated Agama candidates with the checked-in fixture without auto-overwriting YAML.
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
