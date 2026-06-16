# Changelog

All notable changes to zilan-agent are tracked here. Platform validation status remains governed by `agents/openai.yaml` and `docs/platform-validation.md`.

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
