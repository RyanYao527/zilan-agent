# CBETA XML-P5 Collation Preflight

> Date: 2026-08-07  
> Status: local design and preflight only  
> Platform validation: unchanged; this document does not change `docs/platform-validation.md`

## Purpose

Local Agama Markdown is a searchable working corpus. It is good enough for representative retrieval, local citation anchors, and contract fixtures, but it is not a publication-grade critical edition. Publication-level citation work needs a route back to committed CBETA XML-P5 sources, then human collation against the XML text and relevant parallels.

This preflight establishes the first local route check:

```text
Markdown hit -> CBETA work id -> committed XML-P5 source -> TEI header/sourceDesc present -> publication collation remains pending
```

It deliberately avoids vector databases, embeddings, providers, live network calls, and platform-status claims.

## Local Helper

Run:

```powershell
python scripts/cbeta_collation_preflight.py --json
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

## What It Checks

For each four-Agama work, the preflight checks:

- the generated Markdown view exists;
- the committed CBETA XML-P5 source exists;
- the XML root `xml:id` matches the expected CBETA work id;
- the XML has a TEI header, publication statement, and source description;
- the Markdown view still references the CBETA work id and `_source/<work>.xml`;
- the route is reported as `ready`, `review_needed`, or `blocked` with machine-readable issues.

## What It Does Not Prove

This is not publication-level collation. It does not:

- align Markdown line numbers back to XML `pb` / `lb` anchors;
- compare the generated Markdown passage text against the XML body;
- deduplicate or classify search results;
- compare parallel Chinese translations, Pali parallels, or Sanskrit fragments;
- make doctrinal judgments;
- call providers or grade runtime answers;
- change any platform route to `tested`.

## Publication-Level Route

When an answer or report needs publication-grade citation, use this sequence:

1. Search the local Markdown working corpus with `scripts/search_agama.py` and preserve the local citation anchor.
2. Identify the CBETA work id and local Markdown file from the search result.
3. Run `python scripts/cbeta_collation_preflight.py --json` to confirm the committed XML-P5 source route is available.
4. Manually inspect the corresponding XML-P5 source and TEI header/sourceDesc for the cited work.
5. For publication claims, collate the passage against relevant parallel Chinese translations, Pali parallels, or other witnesses as appropriate.
6. Record the evidence separately as collation notes; do not upgrade runtime/platform validation status from this preflight.

## Next Narrow PRs

Useful follow-ups, still without vector infrastructure:

- add a Markdown-line to XML-page/line locator for a small checked fixture set;
- add a tiny parallel-text candidate map for high-value no-self passages;
- add collation evidence manifests under `docs/runtime-evidence/` only when a dated manual collation note exists;
- keep answer contracts saying `待校勘` / publication collation pending until those manual checks are recorded.
