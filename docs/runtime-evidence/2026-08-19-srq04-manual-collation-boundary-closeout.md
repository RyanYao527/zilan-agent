# 2026-08-19 SRQ-04 Manual Collation Boundary Closeout

## Scope

This note consolidates the current `SRQ-04` manual XML-P5 collation boundary. It does not add a new runtime answer,
does not claim publication-level collation, and does not change platform validation status.

`SRQ-04` asks for representative Four-Agama no-self citation behavior. The current checked-in collation evidence is
useful for citation triage, but it remains limited manual theme-parallel evidence.

## Local Checks

```powershell
python scripts\cbeta_collation_preflight.py --check-anchors --json
```

Result on 2026-08-19: `pass`.

- Four committed Agama works are route-ready for local XML-P5 lookup.
- Four anchor probes are located in committed CBETA XML-P5 body spans.
- The preflight still states that publication-level collation, parallel-text comparison, variant witnesses, and human
  scholarly judgment remain pending.

## Boundary Map

| Candidate set | Source anchor | Candidate anchor | Current boundary |
|---|---|---|---|
| `no-self-five-aggregates-and-feeling` | `cbeta-anchor:T02n0099:line-147` | `cbeta-anchor:T01n0001:line-3997` | limited theme parallel; no textual-equivalence claim |
| `long-agama-no-self-verse-and-aggregates` | `cbeta-anchor:T01n0001:line-881` | `cbeta-anchor:T01n0001:line-1829` | limited theme parallel; no textual-equivalence claim |
| `za-agama-and-long-agama-no-self-verse` | `cbeta-anchor:T02n0099:line-147` | `cbeta-anchor:T01n0001:line-881` | limited cross-Agama theme parallel; no textual-equivalence or source-dependence claim |

## Conservative Conclusion

- Anchor-located spans are not textual-equivalence claims.
- Limited theme-parallel reviews are not publication-ready collation.
- Source-dependence claims remain unreviewed.
- The current `SRQ-04` runtime answer excerpts can still pass answer contracts, but the manual collation layer remains
  `manual_review_required` in the evidence manifest.

## Boundaries

- This note is not an answer excerpt and must not be used as `answer_file`.
- This note does not perform live runtime, provider validation, embeddings, vector search, or publication-level collation.
- This note does not change `docs/platform-validation.md`, provider route status, or platform tested status.
