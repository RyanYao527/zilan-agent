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

## First Implementation PR

The next PR after Reasoning Contract v0 should stay local and fixture-based:

1. Add a tiny fixture file under `tests/fixtures/retrieval_chunks/`.
2. Add a dry-run script or validation helper that reads fixture chunks and checks citation fields.
3. Reuse `search_agama.py` output where possible instead of duplicating citation parsing.
4. Add tests for source-file existence, line-range sanity, and stable citation fields.
5. Do not add embeddings, vector storage, or a reranker until fixtures and contracts prove useful.

## Rollback Path

This interface is documentation only. If it proves too early, revert this document without affecting `search_agama.py`, platform validation, runtime evidence, or installed Skill behavior.
