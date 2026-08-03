# 2026-08-03 Codex Desktop Maintenance Smoke

| Field | Value |
|---|---|
| Date | 2026-08-03 |
| Scenario | Codex Desktop migration step 1 maintenance baseline |
| Route / provider | Codex Desktop local shell and documentation workflow |
| Repository commit | `f63de71fb0e1db0e3adebc89dda26c7ad85fb726` |
| Source location | Local checkout `C:\Users\rori9\zilan-agent-review` |
| Redaction note | No API keys, provider payloads, account identifiers, private transcripts, or model answers were used. |
| Standalone answer excerpt | not applicable |
| Runtime log entry | not applicable; this is local maintenance smoke evidence, not platform runtime validation |

## Commands Or Prompts

The maintenance baseline was run before documentation edits and rerun after the new documentation and evidence index entry were added.

```powershell
git status --short --branch
git log -5 --oneline --decorate
python scripts\validate_zilan_repo.py --check-generated --strict-yaml
python -m pytest
python -m ruff check scripts tests
python -m mypy
```

## Output Excerpts

```text
git status --short --branch
## main...origin/main

git log -5 --oneline --decorate
f63de71 (HEAD -> main, origin/main, origin/HEAD) Extract Agama corpus validation helpers (#157)
51d2b85 Extract retrieval chunk validation helpers (#156)
f74e4b4 Extract regression case validation helpers
0112621 Extract reasoning case validation helpers
e2e2de0 (tag: v2.5.6) Release v2.5.6 metadata (#153)

python scripts\validate_zilan_repo.py --check-generated --strict-yaml
zilan-agent validation passed.

python -m pytest
197 passed in 136.88s (0:02:16)

python -m ruff check scripts tests
All checks passed!

python -m mypy
Success: no issues found in 56 source files

Post-documentation verification:
python scripts\validate_zilan_repo.py --check-generated --strict-yaml
zilan-agent validation passed.

python -m pytest
197 passed in 148.30s (0:02:28)

python -m ruff check scripts tests
All checks passed!

python -m mypy
Success: no issues found in 56 source files
```

## Result

| Check / case | Result | Notes |
|---|---|---|
| Git status | `pass` | Worktree was clean on `main` before edits. |
| Recent commit capture | `pass` | Baseline commit was `f63de71fb0e1db0e3adebc89dda26c7ad85fb726`. |
| Repository validation | `pass` | Generated-file and strict YAML checks passed. |
| Pytest | `pass` | First Desktop run timed out after about 124 seconds with no pytest failure output; the same command passed when rerun with a longer execution window. |
| Ruff | `pass` | `scripts` and `tests` passed lint. |
| Mypy | `pass` | 56 source files type-checked successfully. |
| Post-documentation verification | `pass` | The same four maintenance commands passed after adding the migration note, smoke evidence file, and evidence index entry. |
| Platform validation status | `unchanged` | `docs/platform-validation.md` was not edited and no `tested` status was changed. |

## Limitations

- This smoke records local repository maintenance checks only.
- It does not run ZC-01 through ZC-06 prompts, invoke a provider, generate model answers, or validate answer quality.
- It is not an `answer_file` input for semantic answer-contract review or batch review.
- The Codex Desktop app version was not recorded in repository evidence.
