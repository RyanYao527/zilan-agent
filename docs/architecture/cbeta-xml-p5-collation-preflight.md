# CBETA XML-P5 Collation Preflight

> Date: 2026-08-10; manual-collation follow-up: 2026-08-12
> Status: local design, preflight, anchor probes, candidate-map fixtures, and two limited manual XML-P5 theme-parallel reviews
> Platform validation: unchanged; this document does not change `docs/platform-validation.md`

## Purpose

Local Agama Markdown is a searchable working corpus. It is good enough for representative retrieval, local citation anchors, and contract fixtures, but it is not a publication-grade critical edition. Publication-level citation work needs a route back to committed CBETA XML-P5 sources, then human collation against the XML text and relevant parallels.

This preflight establishes the first local route check:

```text
Markdown hit -> CBETA work id -> committed XML-P5 source -> TEI header/sourceDesc present -> publication collation remains pending
```

The 2026-08-10 follow-up adds a narrow checked fixture route:

```text
Markdown line range -> normalized text hash -> committed XML-P5 body span -> TEI pb/lb anchors -> manual collation remains pending
```

It deliberately avoids vector databases, embeddings, providers, live network calls, and platform-status claims.

## Local Helper

Run:

```powershell
python scripts/cbeta_collation_preflight.py --json
```

To include checked Markdown-line to XML `pb` / `lb` anchor probes, run:

```powershell
python scripts/cbeta_collation_preflight.py --check-anchors --json
```

The helper reads only committed files under:

- `context/agama/T0001-chang-agama.md`
- `context/agama/T0026-zhong-agama.md`
- `context/agama/T0099-za-agama.md`
- `context/agama/T0125-ekottarika-agama.md`
- `context/agama/_source/T01n0001.xml`
- `context/agama/_source/T01n0026.xml`
- `context/agama/_source/T02n0099.xml`
- `context/agama/_source/T02n0125.xml`

Expected successful summary:

```json
{
  "mode": "cbeta-xml-p5-collation-preflight",
  "status": "pass",
  "summary": {
    "works": 4,
    "ready": 4,
    "review_needed": 0,
    "blocked": 0,
    "issues": 0
  }
}
```

Expected successful anchor summary:

```json
{
  "mode": "cbeta-xml-anchor-locator",
  "status": "pass",
  "summary": {
    "probes": 4,
    "located": 4,
    "blocked": 0,
    "issues": 0
  }
}
```

The checked anchor fixtures live in `tests/fixtures/collation/cbeta_anchor_probes.yaml`. The current high-value
parallel map lives in `tests/fixtures/collation/high_value_no_self_parallel_candidates.yaml`, where entries may remain
candidate-only queue items or carry dated, limited manual XML-P5 review metadata.

## What It Checks

For each four-Agama work, the preflight checks:

- the generated Markdown view exists;
- the committed CBETA XML-P5 source exists;
- the XML root `xml:id` matches the expected CBETA work id;
- the XML has a TEI header, publication statement, and source description;
- the Markdown view still references the CBETA work id and `_source/<work>.xml`;
- the route is reported as `ready`, `review_needed`, or `blocked` with machine-readable issues.

For the checked anchor fixture set, the anchor locator checks:

- the configured Markdown file and line range exist;
- the selected non-empty Markdown lines have a stable `sha256:` text hash;
- the normalized Markdown line text occurs in the committed XML-P5 body text;
- the located XML body span maps to the expected start and end `pb` / `lb` anchors.

For the checked parallel candidate fixture, repository validation checks that candidate sets:

- reference known anchor probes;
- reference checked-in retrieval chunks;
- either stay marked `candidate_map_only` with `review_candidate` confidence and `pending_manual_collation` status, or
  use `manual_collation_reviewed` with dated manual evidence, `manual_limited_theme_parallel` confidence, and
  `manual_xml_p5_theme_parallel_reviewed` status;
- reject anchor-located-only statuses as completed manual collation;
- preserve the boundaries that manual review does not prove textual equivalence, publication-level equivalence, or runtime
  / platform validation status.

## What It Does Not Prove

This is not publication-level collation. It does not:

- align every Markdown line number back to XML `pb` / `lb` anchors;
- prove full Markdown/XML equality outside the checked fixture spans;
- deduplicate or classify search results;
- prove textual equivalence or publication-ready collation for the high-value candidate map;
- compare parallel Chinese translations, Pali parallels, or Sanskrit fragments for publication use;
- make doctrinal judgments;
- call providers or grade runtime answers;
- change any platform route to `tested`.

## Publication-Level Route

When an answer or report needs publication-grade citation, use this sequence:

1. Search the local Markdown working corpus with `scripts/search_agama.py` and preserve the local citation anchor.
2. Identify the CBETA work id and local Markdown file from the search result.
3. Run `python scripts/cbeta_collation_preflight.py --check-anchors --json` when the cited line is covered by a checked
   anchor probe; otherwise add a new narrow probe before relying on the line anchor.
4. Manually inspect the corresponding XML-P5 source and TEI header/sourceDesc for the cited work.
5. If a candidate set exists in `tests/fixtures/collation/high_value_no_self_parallel_candidates.yaml`, inspect its
   status. `candidate_map_only` is only a review queue item. `manual_collation_reviewed` records a dated, limited XML-P5
   theme-parallel review, not textual equivalence or publication-ready collation.
6. For publication claims, collate the passage against relevant parallel Chinese translations, Pali parallels, or other
   witnesses as appropriate.
7. Record the evidence separately as collation notes; do not upgrade runtime/platform validation status from this preflight.

## Next Narrow PRs

Useful follow-ups, still without vector infrastructure:

- expand anchor probes only when a specific cited passage needs review;
- repeat the dated manual XML-P5 review pattern for another high-value candidate when there is a concrete citation need;
- add collation evidence manifests under `docs/runtime-evidence/` only when multiple dated manual collation notes need
  machine-readable indexing;
- keep answer contracts saying publication collation remains pending until broader parallel-text review supports a stronger
  claim.
