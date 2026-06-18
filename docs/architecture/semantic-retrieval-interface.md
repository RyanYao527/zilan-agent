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
python scripts/semantic_retrieval_dry_run.py --query-id SRQ-02 --json
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

## Fixture Review v0

`scripts/semantic_fixture_review.py` compares generated Agama candidates with the checked-in fixture without
writing files.

Example:

```powershell
python scripts/semantic_fixture_review.py --terms "無我|非我" --limit 5 --json
```

The review helper reports:

- `already_present`: generated candidates whose `chunk_id` already exists in the fixture
- `range_matches`: generated candidates whose source file and line range already exist under a different ID
- `new_candidates`: generated candidates that are not represented in the fixture
- `fixture_only_agama_chunks`: checked-in Agama chunks not produced by the current candidate command

This keeps fixture refreshes explicit: a maintainer can inspect the report, then decide whether to copy any
candidate chunks into `tests/fixtures/retrieval_chunks/semantic_chunks.yaml`.

## Context Bundle Dry Run v0

`scripts/semantic_context_bundle.py` assembles fixture-selected chunks into prompt-ready Markdown without changing the
retrieval route.

Example:

```powershell
python scripts/semantic_context_bundle.py --query-id SRQ-01
python scripts/semantic_context_bundle.py --query-id SRQ-01 --json
```

The bundle helper:

- reuses `semantic_retrieval_dry_run.py` for fixture selection and chunk order
- renders chunks in `expected_chunk_ids` order
- preserves chunk IDs, source files, citations, reasoning roles, and text
- emits either prompt-ready Markdown or JSON with the same `bundle_text`

This proves the context-assembly surface before adding embeddings, vector storage, reranking, or provider calls.

## Role Coverage Review v0

`scripts/semantic_role_coverage.py` reviews whether a fixture-selected context bundle covers the query's declared
`needs` through selected chunk `reasoning_roles`.

Example:

```powershell
python scripts/semantic_role_coverage.py --query-id SRQ-01
python scripts/semantic_role_coverage.py --query-id SRQ-01 --json
```

The role coverage helper:

- reuses `semantic_context_bundle.py` so review is applied after fixture selection and bundle limiting
- reports `role_needs`, `non_chunk_needs`, `covered_needs`, `missing_needs`, `extra_roles`, and a per-chunk role map
- treats missing needs as review findings, not runtime validation failures
- does not edit fixtures, add chunks, call providers, or infer doctrinal completeness

For the current `SRQ-01` fixture, Agama evidence, Collected Topics, Hetuvidya, and Madhyamaka prasaṅga are represented
as chunk-covered role needs. `practice_boundary` remains a non-chunk need because it constrains answer behavior rather
than selecting a specific evidentiary passage.

`SRQ-02` is a narrower Hetuvidya error-detection fixture. It routes the question "检验论式：声，应是可见，以是色形故。"
to the trairupya context chunk plus the `ZR-03` `reason_unestablished` reasoning case. It deliberately does not select
Agama evidence or practice-boundary samples because the gap is formal inference validation.

## Answer Boundary Review v0

`scripts/semantic_answer_boundary_review.py` checks downstream answer text against fixture-defined non-chunk boundary
contracts.

Example:

```powershell
python scripts/semantic_answer_boundary_review.py --query-id SRQ-01 --answer-text "边界：以下只是基于本地 context 的义理分析，不等于修证，也不构成临床、医疗或心理治疗建议。" --json
python scripts/semantic_answer_boundary_review.py --query-id SRQ-01 --sample-id srq01-practice-boundary-pass --json
python scripts/semantic_answer_boundary_review.py --query-id SRQ-01 --sample-id srq01-practice-boundary-fail --json
```

The answer-boundary helper:

- reuses the same query fixture used by retrieval dry runs
- checks only `non_chunk_needs` such as `practice_boundary`
- can read checked-in sample answers from `tests/fixtures/answers/` through `--sample-id`
- reports missing required terms and present forbidden terms
- does not generate answers, call providers, grade doctrine, or upgrade platform validation

For `SRQ-01`, `practice_boundary` currently requires a visible boundary marker and an explicit "不等于修证" statement,
and rejects overclaims such as "保证证悟" or "已证空性".

## Next Implementation PR

The next retrieval PR should still stay local and fixture-based:

1. Add an answer-level sample review for `SRQ-02` only after a concrete reasoning-error output contract is defined.
2. Keep fixture updates explicit; do not auto-overwrite checked-in chunks.
3. Keep `search_agama.py` as the keyword baseline.
4. Do not add embeddings, vector storage, or a reranker until fixture-based dry runs prove useful.

## Rollback Path

This interface is local and fixture-only. If it proves too early, revert this document, the fixture, and
`scripts/semantic_retrieval_dry_run.py` / `scripts/semantic_fixture_candidates.py` /
`scripts/semantic_fixture_review.py` / `scripts/semantic_context_bundle.py` /
`scripts/semantic_role_coverage.py` / `scripts/semantic_answer_boundary_review.py` /
`tests/fixtures/answers/` without affecting
`search_agama.py`, platform validation, runtime evidence, or installed Skill behavior.
