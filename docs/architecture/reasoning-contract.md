# Reasoning Contract v0

> Status: draft contract, schema-validated only.

This document defines the first structured reasoning contract for Zilan. It turns existing prompt-level reasoning expectations into versioned data that can be checked by repository tooling before any larger reasoning engine, semantic retrieval layer, or multi-agent workflow is added.

## Purpose

Zilan already has rich reasoning materials in `context/因明推理引擎.md`, `context/摄类学工具箱.md`, `context/心类学认知分析.md`, and `context/中观应成精要.md`. The current gap is that answer quality is mostly reviewed manually through ZC runtime cases. Reasoning Contract v0 creates a small machine-readable surface for the structures those answers should preserve.

The contract is intentionally conservative:

- It validates data shape, local references, and boundary markers.
- It can check minimum answer structure through fixture-defined answer slots, but only as an explicitness guard.
- It does not claim to automatically decide Buddhist doctrinal correctness.
- It does not replace manual ZC runtime review.
- It does not change platform validation status.

## Non-Goals

Do not use this v0 contract to:

- introduce a vector database or semantic retrieval dependency
- rewrite agent prompts around a new framework
- mark any provider route as `tested`
- implement an LLM judge
- claim that schema validity equals valid Buddhist reasoning

## Contract Families

### `hetuvidya`

Use for Buddhist logic and inference validation.

Required structure:

- `subject`: 有法
- `predicate`: 所立法
- `reason`: 因
- `checks.paksa_dharmata`: 遍是宗法性
- `checks.sapaksa_sattva`: 同品定有性
- `checks.vipaksa_asattva`: 异品遍无性
- `result`: one of `positive_reason`, `reason_unestablished`, `non_pervasive`, `inconclusive_or_contradictory`, or `boundary_only`

This contract only records the expected shape and declared result. It does not prove that the declared result is correct.

`scripts/hetuvidya_validator.py` consumes only checked-in `hetuvidya` fixtures and emits
`hetuvidya-validator-output-v0.1`. The output preserves legacy fields such as `checks` and `classification`, and adds
structured `trairupya_checks`, `judgment`, and `diagnostics` fields so future tooling can consume verdicts without
claiming natural-language parsing or doctrinal grading.

`scripts/reasoning_contract_runner.py` combines the local semantic retrieval dry run, role coverage review,
answer-contract review, and Hetuvidya structured validator into one fixture-only entrypoint. Its `pass`, `fail`, and
`review_needed` statuses are contract-review statuses only; they do not generate answers, call providers, grade doctrine,
or change platform validation status.
When answer-contract review passes, the runner also checks that each structured validator role declared in `needs` has an actual selected reasoning case; otherwise the run fails to prevent answer-contract / validator drift.

`scripts/reasoning_answer_review.py` is a thinner manual-review wrapper over the runner. It returns compact JSON and
Markdown focused on a provided answer source (`--answer-text`, `--answer-file`, or checked-in `--sample-id`), including
missing answer-contract terms and slots, role-coverage gaps, selected validator families, and prototype limitations.
It does not call providers, generate answers, alter prompts, or promote platform validation status. It also preserves the runner answer-validator alignment summary so a batch report can distinguish answer-surface contract failures from missing structured validator cases.

`scripts/reasoning_answer_review_batch.py` reads a small YAML manifest (`version: 1`, `reviews: [...]`) and runs the same
compact answer review for each listed `query_id` / answer source pair. This is intended for transcript or answer-excerpt
review batches; it only summarizes local contract-review statuses and still does not grade doctrine or validate a
platform route.

### `collected_topics`

Use for concept, category, pervasion, tetralemma, and debate-protocol analysis.

Required structure:

- `concepts`: the concepts or terms under comparison
- `relation_checks`: the expected relation checks, such as 总别, 四句, 周遍, or 应成论式 response
- `error_type`: optional label such as `不周遍`, `因不成`, or `总别误置`

### `cognitive_analysis`

Use for daily-practice cognitive analysis grounded in `context/心类学认知分析.md`.

Required structure:

- `chain`: a five-step sequence containing `触`, `作意`, `受`, `想`, and `思`
- `afflictions`: relevant afflictive mental factors, if any
- `corrective_factors`: relevant wholesome or corrective factors

This contract must keep practice advice bounded and must not present itself as therapy or clinical assessment.

### `madhyamaka_prasanga`

Use for Madhyamaka prasaṅga-style critique.

Required structure:

- `opponent_premise`: the premise accepted for critique
- `accepted_commitments`: claims used from the opponent's or conventional framework
- `contradiction`: the contradiction or consequence derived
- `no_independent_thesis`: must be `true` when the case is framed as prasaṅga

This contract records contradiction analysis only. It does not assert direct realization or final doctrinal settlement.

### `agama_evidence`

Use when reasoning depends on Agama evidence.

Required structure:

- `citation_required`: whether an answer must cite sutra name, CBETA ID, and local reference
- `search_scope`: the expected search scope, such as representative search or exhaustive search
- `collation_boundary`: whether publication-level claims require CBETA XML or parallel-text verification

`scripts/agama_evidence_checker.py` consumes checked-in `agama_evidence` fixtures plus the semantic retrieval fixture and emits
`agama-evidence-checker-output-v0.1`. The output makes citation requirements, representative-search scope, local
`context/agama/` references, and collation boundaries explicit. It also verifies that checked-in Agama passage chunks point to
existing local Markdown files, matching CBETA IDs, valid line ranges, and fixture text anchors. It still does not run
`search_agama.py`, perform CBETA XML collation, call providers, or grade whether a produced answer cited the right passage.

## Data File

The initial fixture file is `tests/reasoning_cases.yaml`.

Each case must include:

- `id`: stable `ZR-XX` identifier
- `title`: short human-readable name
- `source_regression_cases`: optional list of related ZC cases
- `contracts`: one or more contract families listed above
- `prompt`: representative user prompt or reasoning task
- `reference_files`: local files that ground the case
- `expected`: contract-specific expected structure
- `boundary_statement`: boolean indicating whether the final answer must include a boundary statement

## Integration Path

1. Keep v0 as documentation plus YAML fixtures.
2. Validate only schema, references, allowed statuses, and boundary fields.
3. Map ZC-02, ZC-03, and ZC-05 to reasoning cases before changing prompt behavior.
4. Use runtime review to compare real answers against these cases.
5. Only after this contract stabilizes, design citation-preserving semantic chunks that can feed these structures.

## Validator Output Contract v0

The local structured validators share a shallow top-level output envelope so downstream tools can consume them without knowing each validator's internal payload shape. This envelope is additive and preserves the existing family-specific payload keys such as `validations`, `analyses`, `critiques`, `mappings`, and `evidence_reviews`.

Common fields:

- `status`: `run` or `not_applicable`
- `validator`: stable local tool identifier, such as `hetuvidya_validator`
- `contract_family`: reasoning contract family, such as `hetuvidya` or `madhyamaka_prasanga`
- `mode`: validator runtime mode when the validator ran
- `output_schema`: validator output schema identifier
- `source`: fixture source path
- `case_id`: requested case id for direct validator calls
- `case_ids`: selected reasoning case ids represented in the payload
- `count`: number of payload items when the validator ran
- `limitations`: explicit prototype boundaries

`not_applicable` validator entries intentionally keep the same `validator`, `contract_family`, `output_schema`, `source`, `case_ids`, payload key, and `limitations` fields. They omit `mode` and `count` because no validator execution occurred.

## Answer Contract v0.1

`tests/fixtures/retrieval_chunks/semantic_chunks.yaml` may attach `answer_contracts` to semantic query fixtures.
Each answer contract can include:

- `required_terms`: literal terms that must appear somewhere in the answer.
- `forbidden_terms`: literal terms that must not appear in the answer.
- `required_slots`: coarse answer-structure slots. Each slot has a `label` and a list of `terms`; at least one term
  in each slot must appear in the answer.

This slot check is still deliberately shallow. It confirms that an answer visibly includes a structural part such as
`argument_decomposition`, `trairupya_check`, `opponent_premise`, or `collation_boundary`; it does not grade the
doctrinal correctness of that part.

## Rollback Path

This contract is additive. If it blocks unrelated maintenance, revert the PR that introduced `docs/architecture/reasoning-contract.md`, `tests/reasoning_cases.yaml`, and the associated validation checks. No runtime prompt, provider harness, or platform status depends on it in v0.
