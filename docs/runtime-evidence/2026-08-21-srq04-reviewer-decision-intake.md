# 2026-08-21 SRQ-04 Reviewer Decision Intake

## Scope

This note adds a structured intake path for future human `SRQ-04` semantic-boundary decisions. It does not add a new
runtime answer, does not perform provider calls, does not update prompts or provider routes, and does not change platform
validation status.

`tests/fixtures/collation/srq04_manual_semantic_boundary_decisions.yaml` now records one pending reviewer-decision row
for each existing `SRQ-04` no-self candidate set:

- `no-self-five-aggregates-and-feeling`
- `long-agama-no-self-verse-and-aggregates`
- `za-agama-and-long-agama-no-self-verse`

Each row carries the required reviewer fields:

- `theme_parallel`
- `textual_equivalence`
- `source_dependence`
- `publication_ready`
- `decision_notes`

## Current Conservative Decision State

All three rows are `pending_reviewer_decision`. Until a human reviewer records a new dated decision, the current
candidate-map conclusions remain unchanged:

- anchor located: yes, through existing XML-P5 anchor probes;
- limited theme-parallel review: recorded for the three candidate sets;
- textual equivalence: not established;
- source dependence: not established;
- publication-ready collation: not established.

## Validation

The repository validator now checks the intake fixture when it is present. The check confirms that each pending decision
references a known candidate set and keeps all required reviewer fields explicit.

Expected local checks:

```powershell
python scripts\cbeta_collation_preflight.py --check-anchors --json
python scripts\srq_coverage_report.py
python scripts\srq_coverage_report.py --json
python scripts\validate_zilan_repo.py --strict-yaml
```

## Boundaries

- This intake note is summary-only evidence and must not be used as `answer_file`.
- Pending reviewer decisions do not upgrade candidate status.
- Pending reviewer decisions do not prove textual equivalence, source dependence, or publication-ready collation.
- Runtime answer evidence and manual collation evidence remain separate.
- `docs/platform-validation.md`, provider route status, and platform tested status remain unchanged.
