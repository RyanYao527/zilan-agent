# Semantic Retrieval Interface Sketch

> Status: design sketch only. No vector database, embedding provider, or runtime behavior is introduced here.

This document defines the smallest useful interface for future semantic retrieval in Zilan. It follows the guardrail in `docs/architecture/reasoning-contract.md`: retrieval should serve reasoning quality and citation integrity, not add framework weight before the interface is proven.

## Current Baseline

`scripts/search_agama.py` is the stable baseline. It already provides:

- keyword and regex search over local Agama Markdown
- `_source/` XML exclusion by default
- known false-positive filtering
- passage grouping
- JSON output
- stable `citation` and `passage_citation` fields

Semantic retrieval must not replace this baseline until it has regression evidence.

## Target Flow

```text
question
  -> query understanding
  -> keyword baseline retrieval
  -> citation-preserving semantic chunk candidates
  -> optional rerank
  -> context bundle
  -> answer
```

The first implementation should be a dry-run local interface, not a hosted service.

## Chunk Types

Use Buddhist textual and reasoning structure before token count.

| Type | Source | Purpose |
|---|---|---|
| `agama_passage` | `context/agama/*.md` | Scripture evidence with CBETA and local line anchors. |
| `context_topic` | `context/*.md` | Topic-level doctrine or method sections, such as 因三相 or 五遍行. |
| `reasoning_case` | `tests/reasoning_cases.yaml` | Structured target examples for reasoning output. |
| `argument_unit` | future extracted units | Small claims or inference rules, such as `被批评 -> 我无价值` is `不周遍`. |

## Minimal Chunk Schema

Future chunk fixtures should preserve these fields:

```yaml
chunk_id: "agama:T02n0099:juan-1:line-33"
chunk_type: "agama_passage"
source_file: "context/agama/T0099-za-agama.md"
start_line: 33
end_line: 37
citation: "《雜阿含經》(T02n0099) 卷 1, context/agama/T0099-za-agama.md:33"
passage_citation: "《雜阿含經》(T02n0099) 卷 1, context/agama/T0099-za-agama.md:33-37"
text: "..."
metadata:
  collection: "雜阿含經"
  cbeta_id: "T02n0099"
  juan: "1"
  section_marker: null
  topics:
    - 無我
    - 五蘊
  reasoning_roles:
    - agama_evidence
  source_hash: "sha256:..."
```

Required invariants:

- `source_file` must exist.
- `start_line` and `end_line` must point into the source file.
- `citation` or `passage_citation` must remain stable enough for prompt use.
- `chunk_type` must be explicit.
- `reasoning_roles` should use contract language where possible, such as `agama_evidence`, `hetuvidya`, `collected_topics`, `cognitive_analysis`, or `madhyamaka_prasanga`.
- `source_hash` is a future strengthening field; fixture v0 validates line anchors and text presence first.

## Query Understanding Fields

A dry-run query analyzer can initially emit:

```yaml
query: "用应成论式分析诸法无我"
needs:
  - agama_evidence
  - collected_topics
  - hetuvidya
  - madhyamaka_prasanga
  - practice_boundary
keywords:
  classical:
    - 無我
    - 非我
    - 五陰
  modern:
    - 无我
    - 应成论式
expected_sources:
  - context/agama/
  - context/摄类学工具箱.md
  - context/因明推理引擎.md
  - context/中观应成精要.md
```

This is enough to route retrieval without committing to a model provider.

## Fixture v0

The first fixture lives at `tests/fixtures/retrieval_chunks/semantic_chunks.yaml`.

Repository validation checks:

- chunk IDs are unique
- chunk types are one of `agama_passage`, `context_topic`, `reasoning_case`, or `argument_unit`
- `source_file` exists
- line ranges are valid for the source file
- `text` appears in the referenced source range
- `citation` and `passage_citation` include local line anchors
- `reasoning_roles` use the Reasoning Contract v0 role vocabulary
- dry-run query fixtures only reference known chunk IDs

This gives the project a citation-preserving retrieval surface without introducing embeddings, vector storage, or a reranker.

## Dry-Run Helper v0

`scripts/semantic_retrieval_dry_run.py` demonstrates the first executable retrieval interface while staying fully
fixture-based.

Example:

```powershell
python scripts/semantic_retrieval_dry_run.py --query-id SRQ-01 --json
```

The helper:

- loads `tests/fixtures/retrieval_chunks/semantic_chunks.yaml`
- selects a query fixture by `--query-id` or exact `--query`
- returns the query's `expected_chunk_ids` as full chunk objects
- preserves `source_file`, `citation`, and `passage_citation`
- states that the result is fixture-defined and performs no embeddings, vector search, reranking, or provider calls

This is intentionally not a ranking algorithm. It is a contract proof that query fixtures can route to
citation-preserving chunks before a real semantic retrieval implementation exists.

## Candidate Generator v0

`scripts/semantic_fixture_candidates.py` converts the `search_agama.py` keyword baseline into reviewable
`agama_passage` chunk candidates.

Example:

```powershell
python scripts/semantic_fixture_candidates.py --terms "無我|非我" --limit 3 --json
```

The generator:

- reuses `search_agama.py` as the source of truth for Agama matches
- deduplicates hits into passage-level `agama_passage` candidates
- preserves `citation` and `passage_citation`
- carries CBETA ID, local source file, line range, matched lines, topic metadata, and a source text hash
- emits JSON or YAML for review before any fixture is updated

This is still not semantic ranking. It is a fixture-refresh aid that keeps candidate generation tied to the
auditable keyword baseline.

## Next Implementation PR

The next retrieval PR should still stay local and fixture-based:

1. Add a reviewed fixture-refresh workflow that compares generated candidates with existing
   `tests/fixtures/retrieval_chunks/semantic_chunks.yaml`.
2. Keep fixture updates explicit; do not auto-overwrite checked-in chunks.
3. Keep `search_agama.py` as the keyword baseline.
4. Do not add embeddings, vector storage, or a reranker until fixture-based dry runs prove useful.

## Rollback Path

This interface is local and fixture-only. If it proves too early, revert this document, the fixture, and
`scripts/semantic_retrieval_dry_run.py` / `scripts/semantic_fixture_candidates.py` without affecting
`search_agama.py`, platform validation, runtime evidence, or installed Skill behavior.
