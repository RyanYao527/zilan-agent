# 2026-08-19 Za Agama / Long Agama No-Self Verse Manual Collation

## Scope

This note records one narrow manual XML-P5 review for an existing `SRQ-04` evidence need:

- source: `cbeta-anchor:T02n0099:line-147` / `agama:T02n0099:juan-1:line-147`
- candidate: `cbeta-anchor:T01n0001:line-881` / `agama:T01n0001:juan-1:line-881`

Both passages are checked-in `SRQ-04` expected chunks in `tests/fixtures/retrieval_chunks/semantic_chunks.yaml`. This is
a limited manual semantic-boundary review for representative retrieval evidence. It is not publication-level collation,
not runtime answer evidence, and not platform validation evidence.

## Local XML-P5 Anchor Check

`python scripts\cbeta_collation_preflight.py --check-anchors --json` passed on 2026-08-19.

| Anchor probe | Markdown line | XML source | Located XML anchor / hash |
|---|---|---|---|
| `cbeta-anchor:T02n0099:line-147` | `context/agama/T0099-za-agama.md:147-149` | `context/agama/_source/T02n0099.xml` | `T02.0099.0002a`, `0002a03` through `0002a10`; text hash `sha256:fc7fcddb9c1c41ee8825df15c994be2ab6978575210fa8de8264774657e04e4c`. |
| `cbeta-anchor:T01n0001:line-881` | `context/agama/T0001-chang-agama.md:881` | `context/agama/_source/T01n0001.xml` | `T01.0001.0009b`, `0009b12`; text hash `sha256:89372a4f6f93f7aa3cdb58d51ccc103a064636f7c5f3a6a00d4a85fecc13abcd`. |

## Manual XML-P5 Reading

`T02n0099` line 147 through 149 says the five aggregates should be observed as impermanent, suffering, non-self, and not
mine, followed by disenchantment and liberation language. The committed XML span is located at `0002a03` through
`0002a10`.

`T01n0001` line 881 is a verse line: `若學決定法，知諸法無我；`. The committed XML span is located at `0009b12`.

Limited conclusion: the pair is a manually reviewed cross-Agama doctrinal theme parallel for `SRQ-04` because both
spans support representative no-self retrieval. The review does not claim textual equivalence: one source is a prose
five-aggregate teaching with `非我` / `非我所` and liberation framing, while the other is a compact verse line about
knowing all dharmas as non-self. It also does not claim source dependence, completeness, or publication readiness.

## Candidate Map Update

`tests/fixtures/collation/high_value_no_self_parallel_candidates.yaml` now records:

- `set_id`: `za-agama-and-long-agama-no-self-verse`
- `status`: `manual_collation_reviewed`
- `confidence`: `manual_limited_theme_parallel`
- `collation_status`: `manual_xml_p5_theme_parallel_reviewed`
- `equivalence_claim`: `false`
- `source_dependence_claim`: `false`
- `publication_ready`: `false`

## Boundaries

- This is local manual XML-P5 review, not publication-level collation.
- Anchor location is not enough to prove textual equivalence.
- Theme parallel evidence is not source-dependence evidence.
- This note is not a runtime answer excerpt and must not be used as an `answer_file`.
- This note does not change `docs/platform-validation.md`, provider route status, or platform tested status.
