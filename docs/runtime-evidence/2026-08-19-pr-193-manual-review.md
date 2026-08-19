# 2026-08-19 PR #193 Manual Review

## Scope

This note records a manual merge-readiness review for PR #193:

- PR: `#193 Record SRQ runtime fail evidence and coverage classes`
- URL: `https://github.com/RyanYao527/zilan-agent/pull/193`
- Head branch: `codex/srq-evidence-closeout`
- Base branch: `main`
- Review date: `2026-08-19`
- Reviewed head before this note: `37b528c`

This is a PR review note. It is not runtime answer evidence, not provider validation evidence, and not a platform-status
promotion record.

## Review Focus

Primary question: are there any blockers that should prevent converting PR #193 from Draft to Ready and squash merging?

The blocker scan focused on:

- unexpected platform-status changes;
- accidental changes to provider route metadata or agent prompts;
- evidence wording that could misrepresent fail/manual evidence as runtime pass evidence;
- answer excerpts being confused with summary-only or manual-collation evidence;
- CI or merge-state blockers;
- unresolved GitHub reviews or comments.

## Current PR State

| Field | Observed state |
|---|---|
| PR state | `OPEN` |
| Draft state | `true` |
| Merge state | `CLEAN` |
| CI | Two `validate` checks completed successfully |
| Reviews | none |
| Comments | none |
| Labels | none |

## Changed-File Scope

PR #193 changes are limited to local evidence, evidence navigation, coverage-report readability, collation fixture
metadata, and tests:

- `CHANGELOG.md`
- `docs/maintenance-roadmap.md`
- `docs/runtime-validation-log.md`
- `docs/runtime-evidence/evidence_manifest.yaml`
- `docs/runtime-evidence/index.md`
- new 2026-08-19 runtime answer excerpts and review notes under `docs/runtime-evidence/`
- `scripts/zilanlib/reasoning/srq_coverage_report.py`
- `tests/fixtures/collation/high_value_no_self_parallel_candidates.yaml`
- `tests/test_collation_validation.py`
- `tests/test_srq_coverage_report.py`

No changes were observed to:

- `docs/platform-validation.md`
- `agents/openai.yaml`
- `agents/zilan-claude-code.md`
- `agents/zilan-codex.md`

## Blocking Findings

No blocker observed.

The PR records strict answer-contract failures for `SRQ-06`, `SRQ-07`, `SRQ-10`, and `SRQ-11` as fail evidence. It does
not claim runtime pass for those cases. It also records a limited `SRQ-04` manual XML-P5 theme-parallel review without
claiming textual equivalence, source dependence, publication-ready collation, runtime pass, or platform-status changes.

The coverage-report change is readability-oriented: it groups runtime evidence status by evidence class so
`standalone_answer_excerpt`, `summary_only`, `batch_manifest`, and `manual_collation` are not conflated.

## Non-Blocking Follow-Up

After merge, the next narrow work should be prompt or contract calibration for the observed fail evidence:

- `SRQ-06` / `SRQ-07`: likely lowest-risk calibration surface because failures are narrow literal-slot misses.
- `SRQ-10` / `SRQ-11`: likely need a separate PR because the misses involve broader cognitive-boundary and
  definition-scope wording.
- `SRQ-04`: continue only citation-demand-driven manual XML-P5 reviews; do not expand into publication-level collation.

These follow-ups should not block #193 because #193 is intentionally recording the fail/manual evidence instead of
pretending it passed.

## Merge Recommendation

Conclusion: PR #193 can be converted from Draft to Ready and squash merged, assuming the checks remain green at merge
time and no new human review blocker is added.

Recommended operator sequence:

```powershell
gh pr ready 193
gh pr checks 193
gh pr merge 193 --squash --delete-branch --subject "Record SRQ runtime fail evidence and coverage classes"
git switch main
git pull --ff-only
git status --short --branch
```

Do not update `docs/platform-validation.md` as part of this merge.
