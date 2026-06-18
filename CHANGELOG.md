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
- Added repository validation for `tests/reasoning_cases.yaml` schema, local references, allowed contract families, and boundary-statement fields without changing runtime platform status.

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
