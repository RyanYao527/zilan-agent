# 2026-09-02 SRQ-04 Citation Anchor / Section Refinement

## Scope

This note records a local, deterministic citation-boundary refinement for `SRQ-04`.

It does not call a provider, does not generate or review a runtime answer, does not update the SRQ-04 candidate-map
conclusion, and does not change platform validation status.

## Checked Evidence

The focused citation gap was `agama:T01n0001:juan-3:line-1829`.

Local checks:

- Markdown source: `context/agama/T0001-chang-agama.md:1829`
- CBETA XML-P5 source: `context/agama/_source/T01n0001.xml`
- XML anchor: `T01.0001.0021a` / `0021a18`
- Anchor probe: `cbeta-anchor:T01n0001:line-1829`
- Current fixture section state: `section_label_status: source_unavailable`

The XML-P5 anchor is located, but the local Markdown/XML span around `0021a18` does not provide a stable title-bearing
`section_label` that can be safely derived for this fixture row. The fixture therefore remains explicitly
`source_unavailable` rather than silently missing.

## Report Change

`scripts/srq_coverage_report.py` now exposes per-chunk citation anchor details under each case's
`citation_metadata.citation_anchor_details` field. For SRQ-04, each Agama chunk shows:

- `chunk_id`
- `cbeta_id`
- `section_label`
- `section_label_status`
- `xml_anchor_status`
- `anchor_probe_id`
- `manual_boundary_status`
- `candidate_set_ids`

This keeps `anchor_located`, `source_unavailable`, and `theme_parallel_only` visible as separate evidence surfaces.

## Result

Status: `manual_review_required`.

The report can now identify that `agama:T01n0001:juan-3:line-1829` is XML-anchor-located but still lacks a stable
source-derived section label. This is citation/coverage evidence only; it is not textual equivalence, source dependence,
publication-ready collation, runtime answer evidence, or platform validation evidence.

## Validation

Run locally after the change:

```powershell
python -m pytest tests\test_srq_coverage_report.py -q
```

The targeted coverage-report tests passed.
