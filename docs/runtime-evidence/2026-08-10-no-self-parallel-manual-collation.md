# 2026-08-10 No-Self Parallel Manual Collation Note

## Scope

This note records the first manual evidence item derived from the high-value parallel candidate map introduced by
the CBETA XML-P5 collation preflight work.

Candidate set: `no-self-five-aggregates-and-feeling`

Source anchor: `cbeta-anchor:T02n0099:line-147` / `agama:T02n0099:juan-1:line-147`

Candidate anchor: `cbeta-anchor:T01n0001:line-3997` / `agama:T01n0001:juan-10:line-3997`

This is a theme-level manual review note. It does not prove publication-level equivalence, does not claim a direct
textual parallel, does not compare Pali or Sanskrit witnesses, does not call providers, and does not change platform
validation status.

`docs/platform-validation.md` was not edited.

## Local Anchor Evidence

Command:

```powershell
python scripts\cbeta_collation_preflight.py --check-anchors --json
```

Result: `pass`, with `works=4`, `ready=4`, `issues=0`, `probes=2`, `located=2`, `blocked=0`.

| Probe | Markdown span | XML span | Text hash |
|---|---|---|---|
| `cbeta-anchor:T02n0099:line-147` | `context/agama/T0099-za-agama.md:147-149` | `context/agama/_source/T02n0099.xml`, `T02.0099.0002a`, `0002a03` through `0002a10` | `sha256:fc7fcddb9c1c41ee8825df15c994be2ab6978575210fa8de8264774657e04e4c` |
| `cbeta-anchor:T01n0001:line-3997` | `context/agama/T0001-chang-agama.md:3997` | `context/agama/_source/T01n0001.xml`, `T01.0001.0061c`, `0061c06` through `0061c22` | `sha256:20ddc44c76009bfd6341d627e0772b4a17f67aa3f7aed2ff736b71c0bdf760d8` |

## Manual Comparison

| Aspect | `T02n0099` source | `T01n0001` candidate | Review result |
|---|---|---|---|
| Main object | Five aggregates, beginning with form and extending through feeling, perception, formations, and consciousness. | Three feelings and views that identify self with feeling or with what depends on feeling. | Same no-self problem space, different doctrinal route. |
| Reasoning surface | Impermanence -> suffering -> not-self -> not-mine, followed by disenchantment and release language. | Feeling arises from contact and ceases with contact; conditioned feeling is impermanent and not self / not mine. | Strong doctrinal-theme parallel around conditioned phenomena and non-self. |
| Textual relation | Compact aggregate formula in the `雜阿含經`. | Extended analytical exchange in the `長阿含經`. | Not marked as a direct textual parallel. |

Recorded relation: `doctrinal_theme_parallel`

Recorded confidence: `review_candidate`

Recorded collation status: `manual_theme_collation_recorded`

## Boundary

This note upgrades the checked candidate from a queue item to dated manual evidence for a narrow theme-level relation.
It still does not prove publication-level equivalence. Use it as local evidence that these two anchored passages should
be discussed together for no-self retrieval and citation review; do not use it as a critical-edition collation result.

Answer contracts and runtime responses should continue to preserve `待校勘` / publication-boundary language unless a
separate publication-grade collation review is recorded.
