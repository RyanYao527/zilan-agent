# Zilan Skill To Agent Migration Record

> Current document version: v2.0
> Last updated: 2026-07-09
> Current project baseline: zilan-agent v2.5.0

This document records how Zilan evolved from a passive skill-style knowledge bundle into a dual-track Skill / Agent framework. It is historical and architectural context, not the source of truth for platform validation.

Authoritative current references:

- Installation and runtime paths: `docs/installation.md`
- Platform validation status: `docs/platform-validation.md`
- Runtime evidence log: `docs/runtime-validation-log.md`
- Evidence and transcript policy: `docs/validation-evidence.md`
- Provider route triage: `docs/provider-routes.md`
- Release notes: `CHANGELOG.md`

## Current Architecture

Zilan now uses a dual-track design:

| Track | Entry | Best for | Current status |
|---|---|---|---|
| Skill mode | `SKILL.md` / `SKILL-en.md` | Lightweight dialogue, daily practice reflection, simple concept explanation | Maintained in repository and covered by invariant checks |
| Codex sub-agent | `agents/zilan-codex.md` | Explicit spawned research, Agama retrieval, cross-domain reports | `tested` as of 2026-06-15 |
| Claude Code agent | `agents/zilan-claude-code.md` | Claude Code explicit agent route and local tool use | `tested` as of 2026-06-16 with UTF-8 stdin on Windows PowerShell |
| OpenAI API harness | `scripts/openai_api_harness.py` | Portable Responses API request construction and live validation path | `harness-ready`; live run still requires `OPENAI_API_KEY` evidence |
| Volcengine OpenAI-compatible harness | `scripts/openai_api_harness.py` | Configurable OpenAI-compatible base URL and `chat-completions` route | `tested` for ZC-01 through ZC-03 as of 2026-06-16; additional cases remain optional |
| Provider metadata | `agents/openai.yaml` | DeepSeek, GLM, Qwen route metadata | `config-only` until native harnesses or dated runtime evidence exist |

Do not infer platform support from this file alone. Use `agents/openai.yaml` and `docs/platform-validation.md`.

## Knowledge Base

Zilan's behavior depends on the committed local corpus:

| Area | File |
|---|---|
| Skill definition | `SKILL.md`, `SKILL-en.md` |
| Collected Topics | `context/摄类学工具箱.md` |
| Buddhist logic | `context/因明推理引擎.md` |
| Cognitive analysis | `context/心类学认知分析.md` |
| Madhyamaka-Prasangika | `context/中观应成精要.md` |
| Vipassana guide | `context/南传观禅指南.md` |
| Buddhist memetics | `context/模因机器视角下的佛教结集与传播.md` |
| Agama working corpus | `context/agama/*.md` |
| CBETA XML source | `context/agama/_source/*.xml` |

The Agama Markdown files are a searchable working corpus. Publication-level citation should verify against CBETA XML and relevant parallel texts.

## Historical Migration Decisions

The initial upgrade introduced:

- a Claude Code agent definition
- a Codex sub-agent prompt
- cross-platform metadata in `agents/openai.yaml`
- explicit Skill versus Agent routing rules
- local Agama search tooling
- platform validation documents and runtime logs
- a machine-readable regression matrix

The design decision that still stands:

- lightweight user-facing Buddhist support stays in Skill mode
- deep research, large Agama retrieval, cross-domain analysis, and long reports use explicit Agent or sub-agent routes
- every platform claim must be backed by dated evidence

## Installation Path Lessons

The 2026-06-12 Claude Code rerun exposed a practical installation-path gap: a local `~/.claude/agents/zilan.md` file can exist while the installed skill folder lacks `scripts/search_agama.py`.

Current guidance:

- If running from a repository checkout, prefer repository-local paths such as `scripts/search_agama.py` and `context/`.
- If running only from an installed Claude Code skill, refresh `~/.claude/skills/zilan-agent/` from the repository.
- The installation procedure is documented in `docs/installation.md`.

## DeepSeek Compatibility Caveat

An earlier Claude Code setup using a DeepSeek Anthropic-compatible endpoint produced an agent-spawn failure related to incompatible thinking / reasoning parameters. That historical observation remains useful when debugging that specific compatibility layer.

Current conservative interpretation:

- Claude Code had separate runtime evidence from 2026-06-12. The 2026-06-15 wake-word blocker was reclassified on 2026-06-16 as a Windows PowerShell stdin encoding failure: without UTF-8, Chinese prompts were received as question marks.
- Native DeepSeek API support is not validated by that Claude Code compatibility-layer observation.
- DeepSeek remains `config-only` in this repository until a native harness or dated provider run exists.

See `docs/provider-routes.md` for current route triage.

## Validation Workflow

Before changing prompts, context files, provider metadata, or harness code, run:

```powershell
python scripts/validate_zilan_repo.py --check-generated --strict-yaml
python -m ruff check scripts tests
python -m pytest
python scripts/openai_api_harness.py --case ZC-02
```

For clean install smoke testing, use a fresh clone and run the same checks sequentially. Do not run `validate_zilan_repo.py --check-generated` in parallel with pytest because the generated Agama Markdown files may be rebuilt during validation.

## Current Next Steps

1. Keep the Claude Code UTF-8 stdin protocol documented and rerun exact ZC prompts after prompt, tool, or install-path changes.
2. Run OpenAI API live validation only after `OPENAI_API_KEY` is available.
3. Add transcript-backed excerpts for representative Codex cases and future Claude Code passing cases where safe.
4. Expand Volcengine OpenAI-compatible live validation beyond ZC-02 only if that route becomes a primary operating path.
5. Add native dry-run/live harnesses for DeepSeek, GLM, and Qwen before upgrading those routes.
6. Improve Agama citation deduplication and publication-level collation.
7. Keep `CHANGELOG.md` updated for user-visible project changes.

## Historical Status

This file supersedes the original v1.0 migration note from 2026-06-10. The older note described the first Skill-to-Agent upgrade and an early Claude Code / DeepSeek compatibility issue. It should no longer be read as current installation or validation guidance.
