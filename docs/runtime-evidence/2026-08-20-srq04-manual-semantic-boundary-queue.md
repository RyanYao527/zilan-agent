# 2026-08-20 SRQ-04 Manual Semantic-Boundary Queue

## Scope

This note queues the current `SRQ-04` manual semantic-boundary review work for human reviewers. It does not add a new
runtime answer, does not perform provider calls, does not update prompts or provider routes, and does not change platform
validation status.

`SRQ-04` asks for representative Four-Agama no-self citation behavior with a clear search and collation boundary. The
existing XML-P5 evidence supports local citation triage and limited theme-parallel review only. It does not prove textual
equivalence, source dependence, or publication-ready collation.

## Local Baseline

Run these commands before making a reviewer decision:

```powershell
python scripts\cbeta_collation_preflight.py --check-anchors --json
python scripts\srq_coverage_report.py
python scripts\srq_coverage_report.py --json
```

Expected conservative status:

- CBETA XML-P5 preflight and anchor locator: `pass`
- SRQ coverage summary: `ready=10`, `manual_review_required=1`
- Only case requiring manual review: `SRQ-04`

## Queue Items

| Candidate set | Source anchor | Candidate anchor | Current status | Reviewer decision required |
|---|---|---|---|---|
| `no-self-five-aggregates-and-feeling` | `cbeta-anchor:T02n0099:line-147` / `agama:T02n0099:juan-1:line-147` | `cbeta-anchor:T01n0001:line-3997` / `agama:T01n0001:juan-10:line-3997` | anchor located; limited theme-parallel review recorded | Confirm whether the pair remains only a doctrinal theme parallel, or whether there is separate evidence for textual equivalence, source dependence, or publication-ready collation. |
| `long-agama-no-self-verse-and-aggregates` | `cbeta-anchor:T01n0001:line-881` / `agama:T01n0001:juan-1:line-881` | `cbeta-anchor:T01n0001:line-1829` / `agama:T01n0001:juan-3:line-1829` | anchor located; limited theme-parallel review recorded | Confirm whether the two Long Agama verse contexts remain only representative no-self theme parallels, or whether stronger collation claims can be supported. |
| `za-agama-and-long-agama-no-self-verse` | `cbeta-anchor:T02n0099:line-147` / `agama:T02n0099:juan-1:line-147` | `cbeta-anchor:T01n0001:line-881` / `agama:T01n0001:juan-1:line-881` | anchor located; limited cross-Agama theme-parallel review recorded | Confirm whether the cross-Agama relation remains limited to representative no-self evidence, with no textual-equivalence or source-dependence claim. |

## Reviewer Questions

For each candidate set, answer all four questions:

1. Is the current evidence still only a limited doctrinal theme parallel?
2. Can the reviewer support a textual-equivalence claim from the checked XML-P5 spans?
3. Can the reviewer support a source-dependence claim from the checked XML-P5 spans and known parallels?
4. Can the reviewer support publication-ready collation, including broader parallel-text and witness comparison?

Default conservative answer before new human review:

- Theme-parallel: yes, limited.
- Textual equivalence: not established.
- Source dependence: not established.
- Publication-ready collation: not established.

## Evidence To Inspect

- `docs/runtime-evidence/2026-08-12-no-self-parallel-manual-collation.md`
- `docs/runtime-evidence/2026-08-12-long-agama-no-self-verse-manual-collation.md`
- `docs/runtime-evidence/2026-08-19-za-long-agama-no-self-verse-manual-collation.md`
- `docs/runtime-evidence/2026-08-19-srq04-manual-collation-boundary-closeout.md`
- `tests/fixtures/collation/cbeta_anchor_probes.yaml`
- `tests/fixtures/collation/high_value_no_self_parallel_candidates.yaml`

## Boundaries

- Anchor located means the committed Markdown line text was found in committed CBETA XML-P5 body text; it is not a
  collation conclusion.
- Limited theme-parallel review means the passages support representative retrieval/citation triage; it is not textual
  equivalence.
- This queue note is not an answer excerpt and must not be used as `answer_file`.
- This queue note does not turn `SRQ-04` manual collation into runtime pass evidence.
- `docs/platform-validation.md`, provider route status, and platform tested status remain unchanged.

## Next Action

Keep `SRQ-04` as `manual_review_required` until a future dated human review records one of these explicit outcomes:

- keep the current limited theme-parallel boundary;
- add a narrower manually reviewed candidate decision with the same conservative boundaries;
- record a stronger textual-equivalence, source-dependence, or publication collation claim with separate evidence.
