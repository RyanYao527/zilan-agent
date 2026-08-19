# 2026-08-12 Long Agama No-Self Verse Manual Collation Note

## Scope

This note records a second narrow manual XML-P5 review for an existing `SRQ-04` evidence need:

- source: `cbeta-anchor:T01n0001:line-881` / `agama:T01n0001:juan-1:line-881`
- candidate: `cbeta-anchor:T01n0001:line-1829` / `agama:T01n0001:juan-3:line-1829`

Both passages are checked-in `SRQ-04` expected chunks in `tests/fixtures/retrieval_chunks/semantic_chunks.yaml`. This
review records a limited Long Agama no-self theme-parallel relation for representative retrieval evidence. It does not
call providers, does not run live runtime, does not alter prompts, routes, or install paths, and does not change
`docs/platform-validation.md`.

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
| Source | `context/agama/T0001-chang-agama.md:881` | `context/agama/_source/T01n0001.xml` | `T01.0001.0009b`, `0009b12` | `sha256:89372a4f6f93f7aa3cdb58d51ccc103a064636f7c5f3a6a00d4a85fecc13abcd` |
| Candidate | `context/agama/T0001-chang-agama.md:1829` | `context/agama/_source/T01n0001.xml` | `T01.0001.0021a`, `0021a18` | `sha256:2215c02d0e8da74dfcdb2b2cd5931b22992cc739f552aa8e8a2a9398f12a2277` |

## Manual XML Comparison

The source XML span in `T01n0001` says, in verse form, that one who learns the determinate Dharma knows all dharmas as
non-self. The candidate XML span in the same work says that seeing aggregates, elements, and sense bases as non-self is
the foremost offering.

Limited conclusion: the pair is a manually reviewed doctrinal theme parallel for `SRQ-04` because both spans support the
same representative no-self citation surface in the Long Agama. The relation is useful for retrieval triage and citation
review, but it remains a bounded theme relation between different verse contexts.

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
