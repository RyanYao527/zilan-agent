# 2026-09-01 SRQ-04 Reviewer Decision Ingestion Path

## Summary

This note records a local, deterministic ingestion path for future human `SRQ-04` XML-P5 semantic-boundary decisions.
No new reviewer conclusion was supplied in this change.

Current state remains conservative:

- all three `SRQ-04` reviewer-decision intake rows are still `pending_reviewer_decision`;
- existing XML anchors remain located;
- existing manual collation evidence remains limited theme-parallel only;
- textual equivalence, source dependence, and publication-ready collation remain unestablished;
- this is not runtime answer evidence and does not change platform validation status.

## Decision Fixture

Future decisions should be recorded in:

```text
tests/fixtures/collation/srq04_manual_semantic_boundary_decisions.yaml
```

Each candidate-set row keeps the existing required fields:

- `theme_parallel`
- `textual_equivalence`
- `source_dependence`
- `publication_ready`
- `decision_notes`

## Ingestion Rules

Pending rows must keep all reviewer boundary fields at `pending`. A pending row cannot carry a textual-equivalence,
source-dependence, or publication-ready claim.

`limited_theme_parallel_confirmed` rows must record:

- `theme_parallel: limited`
- `textual_equivalence: not_established`
- `source_dependence: not_established`
- `publication_ready: not_established`
- `evidence_file: docs/runtime-evidence/YYYY-MM-DD-*.md`

`stronger_claim_requires_separate_evidence` rows must mark at least one of these fields as
`supported_with_evidence`:

- `textual_equivalence`
- `source_dependence`
- `publication_ready`

They must also cite `evidence_file: docs/runtime-evidence/YYYY-MM-DD-*.md`.

If a stronger claim is accepted later, update only the matching candidate set in
`tests/fixtures/collation/high_value_no_self_parallel_candidates.yaml`. Do not expand the update into
publication-level collation.

## Validation

The ingestion path is checked locally by:

```powershell
python scripts\srq04_manual_review_packet.py
python scripts\srq04_manual_review_packet.py --json
python scripts\cbeta_collation_preflight.py --check-anchors --json
python scripts\validate_zilan_repo.py --strict-yaml
python scripts\validate_zilan_repo.py --check-generated --strict-yaml
```

## Known Limits

- No provider was called.
- No runtime answer excerpt was created.
- No candidate-map conclusion was changed.
- `SRQ-04` remains `manual_review_required` in the evidence manifest and coverage report.
- `docs/platform-validation.md` remains unchanged.
