# SRQ-04 Representative Anchor Design

## Goal

Ensure the SRQ-04 answer contract rejects an answer that names CBETA `T02n0099` but cites a different Agama passage as its representative evidence.

## Scope

- Add one required answer-contract slot for the checked representative local anchor: `context/agama/T0099-za-agama.md:147`; the existing `T02n0099` requirement continues to bind it to the checked work.
- Add one focused negative regression test whose answer contains every existing SRQ-04 generic requirement but substitutes a Long Agama citation.
- Preserve `scripts/search_agama.py`, retrieval ranking, provider metadata, platform-validation status, and the existing pass/fail samples.

## Behavior

The existing passing SRQ-04 fixture and the canonical `passage_citation` remain valid because both contain the required stable local anchor prefix. An answer that contains `CBETA`, `T02n0099`, `context/agama/`, the search/collation boundaries, but lacks that representative T0099 line anchor must fail with the missing `representative_agama_anchor` slot.

## Validation and Rollback

Run the focused SRQ-04 review test, retrieval dry run, repository validator, lint, type check, and full pytest suite. The change is additive and reversible by removing the one fixture slot and its test; it does not alter stored corpus data or external route behavior.
