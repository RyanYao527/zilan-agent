# 2026-08-12 No-Self Parallel Manual Collation Note

## Scope

This note records a narrow manual XML-P5 review for one existing high-value no-self candidate pair:

- source: `cbeta-anchor:T02n0099:line-147` / `agama:T02n0099:juan-1:line-147`
- candidate: `cbeta-anchor:T01n0001:line-3997` / `agama:T01n0001:juan-10:line-3997`

It updates `tests/fixtures/collation/high_value_no_self_parallel_candidates.yaml` from a review queue item to a limited
manual theme-parallel review. It does not call providers, does not run live runtime, does not alter prompts, routes, or
install paths, and does not change `docs/platform-validation.md`.

## Commands

```powershell
python scripts\cbeta_collation_preflight.py --check-anchors --json
python -m pytest tests\test_cbeta_collation_preflight.py tests\test_collation_validation.py -q
python scripts\validate_zilan_repo.py --strict-yaml
python -m ruff check scripts tests
python -m mypy
```

## Anchor Review

| Item | Markdown range | XML source | Located XML span | Text hash |
|---|---|---|---|---|
| Source | `context/agama/T0099-za-agama.md:147-149` | `context/agama/_source/T02n0099.xml` | `T02.0099.0002a`, `0002a03` through `0002a10` | `sha256:fc7fcddb9c1c41ee8825df15c994be2ab6978575210fa8de8264774657e04e4c` |
| Candidate | `context/agama/T0001-chang-agama.md:3997` | `context/agama/_source/T01n0001.xml` | `T01.0001.0061c`, `0061c06` through `0061c22` | `sha256:20ddc44c76009bfd6341d627e0772b4a17f67aa3f7aed2ff736b71c0bdf760d8` |

## Manual XML Comparison

The source XML span in `T02n0099` states the five aggregates are impermanent, suffering, non-self, and not self-owned,
then frames this as right observation. The candidate XML span in `T01n0001` analyzes the three feelings as conditioned,
impermanent, ceasing phenomena, then rejects treating feeling as self.

Limited conclusion: the pair is a manually reviewed doctrinal theme parallel for no-self reasoning because both spans
support the same bounded teaching surface used by `SRQ-04`: conditioned phenomena or feelings should not be appropriated
as self or self-owned.

## Boundaries

- This is not textual equivalence.
- This is not source-dependence evidence.
- This is not publication-ready collation.
- This does not compare Pali parallels, Sanskrit fragments, or variant Chinese witnesses.
- This is not runtime answer evidence and must not be used as `answer_file`.
- This does not change platform validation status.

## Runtime Rerun Decision

No prompt, provider route, or install-path file changed in this work. Therefore the ZC runtime rerun trigger is not
activated in this note. If a future change touches prompts, routes, or installation paths, capture a standalone answer
excerpt and review it with the relevant batch answer-contract manifest before changing any runtime claim.
