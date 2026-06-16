# Installation And Runtime Guide

> Last updated: 2026-06-16

This guide separates the supported operating routes for Zilan: Codex, Claude Code, the OpenAI API harness, and OpenAI-compatible provider harnesses. Platform validation status is tracked separately in `docs/platform-validation.md`.

## Prerequisites

- Git
- Python 3.10 or newer for repository checks and helper scripts
- Optional development install:

```powershell
python -m pip install -e ".[dev]"
```

## Clone

```powershell
git clone https://github.com/RyanYao527/zilan-agent.git
cd zilan-agent
```

Run the repository checks before relying on a local checkout:

```powershell
python scripts/validate_zilan_repo.py --check-generated --strict-yaml
python -m pytest
```

## Claude Code

Claude Code has two separate install surfaces:

- Skill: lightweight dialogue and context activation
- Agent definition: explicit deep-research route with tool use

From the parent directory that contains the cloned `zilan-agent` folder:

```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.claude\skills" | Out-Null
Copy-Item -Recurse -Force ".\zilan-agent" "$env:USERPROFILE\.claude\skills\"

New-Item -ItemType Directory -Force "$env:USERPROFILE\.claude\agents" | Out-Null
Copy-Item -Force ".\zilan-agent\agents\zilan-claude-code.md" "$env:USERPROFILE\.claude\agents\zilan.md"
```

Equivalent POSIX shell commands:

```bash
mkdir -p ~/.claude/skills ~/.claude/agents
cp -R zilan-agent ~/.claude/skills/
cp zilan-agent/agents/zilan-claude-code.md ~/.claude/agents/zilan.md
```

Smoke-check the installed files:

```powershell
Test-Path "$env:USERPROFILE\.claude\skills\zilan-agent\SKILL.md"
Test-Path "$env:USERPROFILE\.claude\agents\zilan.md"
```

To test the Claude Code install layout without touching your real user profile, run the mock install smoke:

```powershell
python scripts/mock_install_smoke.py
```

The smoke script creates a temporary mock home directory, copies the repository to `.claude/skills/zilan-agent`, installs `agents/zilan-claude-code.md` as `.claude/agents/zilan.md`, and runs an Agama search from the copied skill.

Use lightweight prompts for Skill mode:

```text
孜澜，我今天职场又被否定了，心里很难受。
孜澜，什么是因三相？
```

Use explicit prompts for Agent mode:

```text
请 spawn 一个 zilan agent，查四阿含中关于无我的经文，并做初步归类分析。
请 spawn 一个 zilan agent，用应成论式分析诸法无我，并串联阿含、摄类学、因明和观禅。
```

When working from a repository checkout, prefer repository-local paths such as `scripts/search_agama.py` and `context/`. When working only from an installed skill, use the installed `~/.claude/skills/zilan-agent/` paths.

## Codex

Codex can work directly from this repository checkout. Keep the repository root as the working directory so the agent prompt, context files, regression matrix, and search tools resolve consistently.

Useful entry points:

- `SKILL.md` for the main skill definition
- `agents/zilan-codex.md` for explicit sub-agent behavior
- `CODEX_REGRESSION_TESTS.md` and `tests/regression_cases.yaml` for expected runtime scenarios
- `scripts/search_agama.py` for local Agama search with stable citations

Recommended local checks:

```powershell
python -m ruff check scripts tests
python -m pytest
python scripts/validate_zilan_repo.py --check-generated --strict-yaml
python scripts/mock_install_smoke.py
python scripts/search_agama.py --terms "無我|非我|緣起" --limit 5
```

## OpenAI API Harness

The native OpenAI route is implemented as a minimal Responses API harness. It is dry-run by default and does not require credentials:

```powershell
python scripts/openai_api_harness.py --case ZC-02 --json
```

Live mode requires an environment variable and explicit opt-in:

```powershell
$env:OPENAI_API_KEY = "..."
python scripts/openai_api_harness.py --case ZC-02 --live --json
```

Do not commit API keys, live response payloads containing secrets, or private account metadata. Record live validation summaries according to `docs/validation-evidence.md`.

## OpenAI-Compatible Provider Harness

The same harness can build OpenAI-compatible Chat Completions requests for providers such as Volcengine. This is a separate route from native OpenAI API validation:

```powershell
python scripts\openai_api_harness.py --case ZC-02 --provider-route volcengine_openai_compatible --json
```

The provider route preset reads the tested Volcengine defaults from `agents/openai.yaml`. To override them manually:

```powershell
$env:OPENAI_BASE_URL = "https://<provider-openai-compatible-base-url>/v1"
$env:OPENAI_MODEL = "<provider-model-id>"
$env:OPENAI_API_SURFACE = "chat-completions"
$env:OPENAI_API_KEY_ENV = "VOLCENGINE_OPENAI_API_KEY"
python scripts/openai_api_harness.py --case ZC-02 --json
```

Live mode uses the provider-specific key environment variable:

```powershell
$env:VOLCENGINE_OPENAI_API_KEY = "..."
python scripts/openai_api_harness.py --case ZC-02 --provider-route volcengine_openai_compatible --live --json
```

Record a successful compatible-provider run under that provider route. Do not use it to mark native OpenAI API as `tested`.

## Provider Routes

Volcengine OpenAI-compatible is `tested` for one ZC-02 live run through `chat-completions`; native OpenAI API remains `harness-ready`. DeepSeek, GLM, and Qwen currently remain provider metadata routes unless a native harness, credentials, and dated runtime evidence are added. See `docs/provider-routes.md` for the current route triage.

## Troubleshooting

- If Claude Code finds `~/.claude/agents/zilan.md` but cannot run `search_agama.py`, refresh the installed skill folder from the repository.
- If an answer cites Agama passages without file references, rerun the task with explicit instruction to use `scripts/search_agama.py --json`.
- If OpenAI live mode fails immediately, confirm `OPENAI_API_KEY` is set in the same shell session.
- If provider route validation is blocked by missing credentials, keep the platform status conservative and record the blocker instead of upgrading status.
