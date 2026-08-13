# 2026-08-10 CBETA Anchor / Parallel Candidate Local Replay

## Scope

This note records local evidence for the P2-C / P2-D collation aids and the P1 reasoning/retrieval contract replay
refresh. It uses only committed repository files and checked-in answer excerpts. It does not run Claude Code, Codex,
OpenAI, or any OpenAI-compatible provider, and it does not generate a new model answer.

Platform validation status remains unchanged. `docs/platform-validation.md` was not edited.

## Commands

```powershell
python scripts\cbeta_collation_preflight.py --check-anchors --json
python scripts\reasoning_answer_review_batch.py --batch docs\runtime-evidence\2026-08-06-zc-05-srq-01-runtime-spot-review-batch.yaml --json
python scripts\reasoning_answer_review_batch.py --batch docs\runtime-evidence\2026-07-20-latest-zc-answer-excerpt-review-batch.yaml --json
python scripts\semantic_answer_contract_review.py --query-id SRQ-01 --answer-file docs\runtime-evidence\2026-08-06-claude-code-zc-05-srq-01-runtime-spot-answer.md
python -m pytest tests\test_cbeta_collation_preflight.py tests\test_collation_validation.py tests\test_validation_suite.py tests\test_validate_zilan_repo.py -q
```

## Results

| Check | Result | Notes |
|---|---:|---|
| CBETA XML-P5 route preflight | pass | `works=4`, `ready=4`, `issues=0`. |
| Markdown-line to XML anchor locator | pass | Current default report: `probes=4`, `located=4`, `blocked=0`, `issues=0`. |
| Collation fixture validator tests | pass | Targeted suite result: `48 passed`. |
| Current broad `ZC-05` runtime spot replay | fail expected | `pass=2`, `fail=2`; `SRQ-01` and `SRQ-04` pass, while `SRQ-03` / `SRQ-08` still miss strict broad-answer slots. |
| Earlier broad `ZC-05` committed excerpt replay | pass | `pass=5`, `fail=0`; confirms the local contracts still pass when the required slots are present. |
| Direct `SRQ-01` calibrated review | pass | Missing required terms: none; present forbidden terms: none; missing required slots: none. |

## Anchor Fixtures

The checked anchor probes are stored in `tests/fixtures/collation/cbeta_anchor_probes.yaml`.

| Probe | Markdown range | XML source | Located anchors |
|---|---|---|---|
| `cbeta-anchor:T02n0099:line-147` | `context/agama/T0099-za-agama.md:147-149` | `context/agama/_source/T02n0099.xml` | `T02.0099.0002a`, `0002a03` through `0002a10`; text hash `sha256:fc7fcddb9c1c41ee8825df15c994be2ab6978575210fa8de8264774657e04e4c`. |
| `cbeta-anchor:T01n0001:line-3997` | `context/agama/T0001-chang-agama.md:3997` | `context/agama/_source/T01n0001.xml` | `T01.0001.0061c`, `0061c06` through `0061c22`; text hash `sha256:20ddc44c76009bfd6341d627e0772b4a17f67aa3f7aed2ff736b71c0bdf760d8`. |
| `cbeta-anchor:T01n0001:line-881` | `context/agama/T0001-chang-agama.md:881` | `context/agama/_source/T01n0001.xml` | `T01.0001.0009b`, `0009b12`; text hash `sha256:89372a4f6f93f7aa3cdb58d51ccc103a064636f7c5f3a6a00d4a85fecc13abcd`. |
| `cbeta-anchor:T01n0001:line-1829` | `context/agama/T0001-chang-agama.md:1829` | `context/agama/_source/T01n0001.xml` | `T01.0001.0021a`, `0021a18`; text hash `sha256:2215c02d0e8da74dfcdb2b2cd5931b22992cc739f552aa8e8a2a9398f12a2277`. |

## Parallel Candidate Map

The high-value no-self candidate map is stored in
`tests/fixtures/collation/high_value_no_self_parallel_candidates.yaml`.

Current reviewed candidate sets:

- `no-self-five-aggregates-and-feeling`
- source: `cbeta-anchor:T02n0099:line-147` / `agama:T02n0099:juan-1:line-147`
- candidate: `cbeta-anchor:T01n0001:line-3997` / `agama:T01n0001:juan-10:line-3997`
- current status after the 2026-08-12 follow-up: `manual_collation_reviewed`
- confidence: `manual_limited_theme_parallel`
- collation status: `manual_xml_p5_theme_parallel_reviewed`
- evidence note: `docs/runtime-evidence/2026-08-12-no-self-parallel-manual-collation.md`
- `long-agama-no-self-verse-and-aggregates`
- source: `cbeta-anchor:T01n0001:line-881` / `agama:T01n0001:juan-1:line-881`
- candidate: `cbeta-anchor:T01n0001:line-1829` / `agama:T01n0001:juan-3:line-1829`
- current status after the 2026-08-12 follow-up: `manual_collation_reviewed`
- confidence: `manual_limited_theme_parallel`
- collation status: `manual_xml_p5_theme_parallel_reviewed`
- evidence note: `docs/runtime-evidence/2026-08-12-long-agama-no-self-verse-manual-collation.md`

These remain limited manual XML-P5 theme-parallel reviews, not textual-equivalence or publication-ready collation claims.
They do not prove source dependence, full doctrinal equivalence, or runtime answer quality.

## Reasoning / Retrieval Replay Interpretation

The replay refresh preserves the current distinction between prepared prompt/contract surfaces and runtime evidence:

- the 2026-08-06 broad `ZC-05` answer still passes `SRQ-01` and `SRQ-04` under the current calibrated contracts;
- the same 2026-08-06 answer still fails strict `SRQ-03` and `SRQ-08` broad-answer checks, so broad runtime status remains
  `prompt prepared, runtime pending`;
- the 2026-07-20 committed excerpt batch still passes, showing the replay contracts did not regress;
- the new collation locator and candidate-map fixtures improve local citation evidence, but they do not change runtime or
  platform validation status.

## Boundary

This is summary-only local evidence. Do not use this file as `answer_file` input for batch review. It does not call
providers, does not upgrade `agents/openai.yaml`, does not edit `docs/platform-validation.md`, and does not grade Buddhist
doctrine.
