# Codex Desktop Migration

> Last updated: 2026-08-03

This note defines the narrow Codex Desktop development path for zilan-agent maintenance work. It is a process note, not runtime validation evidence, and it does not change platform status in `agents/openai.yaml` or `docs/platform-validation.md`.

## Development Workflow

Use Codex Desktop as the primary maintenance surface when working in this repository.

1. Start from a clean worktree when practical:

```powershell
git status --short --branch
git log -5 --oneline --decorate
```

2. Keep each Desktop task narrowly scoped. Prefer one maintenance theme per branch or PR, and avoid mixing documentation, prompt, script, fixture, and platform-status changes unless the same evidence requires them.
3. Read the nearby repository docs before editing. Follow the existing boundary between platform status, runtime evidence, architecture notes, and maintenance roadmap entries.
4. Record the exact commit used for evidence before changing files when the evidence describes a pre-change baseline.
5. Treat generated-file checks as a separate step from pytest. `--check-generated` may rebuild committed Agama Markdown, so do not run it in parallel with tests that inspect generated files.
6. Do not mark a route as `tested` in `docs/platform-validation.md` unless the PR also includes dated runtime or live-provider evidence that satisfies `docs/validation-evidence.md`.

## Maintenance Checks

Run the standard local baseline before handing off a maintenance PR:

```powershell
python scripts\validate_zilan_repo.py --check-generated --strict-yaml
python -m pytest
python -m ruff check scripts tests
python -m mypy
```

Notes:

- `python -m pytest` can take more than two minutes on Windows. If a Desktop tool timeout stops the command without pytest failure output, rerun the same command with a longer execution window and record the timeout separately.
- Run lint and type checks after any Python or test change. For docs-only changes, keep the full baseline result in the PR when practical, because repository invariant tests cover documentation references.
- If `python scripts\validate_zilan_repo.py --check-generated --strict-yaml` changes generated Agama files, inspect the diff before committing and confirm the changes are intended.

## PR Flow

Use a small branch and PR for each Desktop migration step.

1. Create or switch to a branch named with the `codex/` prefix unless the maintainer requests another name.
2. Commit only the files in scope. For Desktop migration maintenance, expected files are usually under `docs/`, `docs/runtime-evidence/`, or tightly related validation scripts.
3. In the PR body, include:
   - scope summary
   - evidence date and repository commit
   - commands run and pass/fail/blocked status
   - any known timeouts, environment limits, or skipped checks
   - explicit note when `docs/platform-validation.md` status values are unchanged
4. Open a draft PR when evidence is still being reviewed. Mark it ready only after the requested baseline commands have completed or the blocked state is documented.
5. Do not combine status promotion with unrelated cleanup. Platform status changes should be easy to audit from the evidence alone.

## Evidence Recording

Use `docs/runtime-evidence/` for small, redacted command-output or Desktop-session evidence files. Use `docs/runtime-validation-log.md` for manual runtime sessions that evaluate platform behavior or ZC prompt results.

Evidence files should record:

- date
- scenario
- route or tool surface
- repository commit
- command or prompt set
- redaction note
- standalone answer excerpt status
- compact output excerpts
- result table
- limitations

For maintenance smoke tests that do not generate model answers, mark standalone answer excerpt status as `not applicable` and do not use the file as an `answer_file` input for contract or batch review.

Use summary-only evidence when raw transcripts or command output are too large, private, or not needed for mechanical review. Never commit API keys, tokens, cookies, private account metadata, full provider payloads, or private user content unrelated to the validation case.

## CLI Fallback Strategy

Use the CLI path when Codex Desktop cannot complete a task because of app instability, approval prompts, very long command runtimes, or branch/push constraints.

Fallback rules:

- Run the same repository commands from the same checkout whenever possible.
- Keep PowerShell as the default Windows shell for this repository.
- Preserve UTF-8 setup when piping Chinese prompts through external CLIs:

```powershell
$OutputEncoding = [System.Text.UTF8Encoding]::new()
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new()
```

- Save only compact, redacted evidence in the repository. Keep bulky raw transcripts outside the repo and mention their local-only status in the evidence note.
- If branch, push, or PR operations are blocked in Desktop, finish the file changes and validation locally, then use the CLI or Codex app controls to create the branch, commit, push, and PR.
- A CLI fallback run does not by itself upgrade platform status. Status promotion still requires the evidence policy in `docs/validation-evidence.md`.
