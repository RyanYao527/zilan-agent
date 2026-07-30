# 2026-07-30 Post-Alignment Answer Review Replay

Date: 2026-07-30
Repository commit: `929cc76`
Scenario: local replay of committed reasoning answer-review batch manifests after #150/#151 exposed answer-validator alignment guards and summaries.
Route: local fixture review only; no provider calls, no answer generation, no platform-status change.
Standalone answer excerpt status: no new answer excerpts were captured; this replay reused existing committed sample IDs and answer files.
Redaction note: no API keys, provider payloads, account identifiers, or private transcripts were used.

## Commands

```powershell
python scripts\reasoning_answer_review_batch.py --batch docs\runtime-evidence\2026-07-17-reasoning-answer-review-batch.yaml --json
python scripts\reasoning_answer_review_batch.py --batch docs\runtime-evidence\2026-07-17-runtime-answer-excerpt-review-batch.yaml --json
python scripts\reasoning_answer_review_batch.py --batch docs\runtime-evidence\2026-07-20-latest-zc-answer-excerpt-review-batch.yaml --json
python scripts\reasoning_answer_review_batch.py --batch docs\runtime-evidence\2026-07-20-compact-zc-04-answer-excerpt-progression-batch.yaml --json
```

## Batch Results

| Batch manifest | Overall status | Summary | Alignment finding | Notes |
|---|---|---|---|---|
| `2026-07-17-reasoning-answer-review-batch.yaml` | pass | pass=4, fail=0, review_needed=0, other=0 | no missing validator cases | Checked-in answer samples for `SRQ-04`, `SRQ-08`, `SRQ-09`, and `SRQ-11` remain aligned with their structured validator cases. |
| `2026-07-17-runtime-answer-excerpt-review-batch.yaml` | pass | pass=6, fail=0, review_needed=0, other=0 | no missing validator cases | Existing Claude Code runtime answer excerpts for `SRQ-02`, `SRQ-03`, `SRQ-04`, `SRQ-05`, and broad `ZC-05` still have matching structured validator coverage. |
| `2026-07-20-latest-zc-answer-excerpt-review-batch.yaml` | pass | pass=5, fail=0, review_needed=0, other=0 | no missing validator cases | Latest committed broad-answer excerpts still satisfy their answer contracts and validator alignment checks. |
| `2026-07-20-compact-zc-04-answer-excerpt-progression-batch.yaml` | fail expected | pass=2, fail=1, review_needed=0, other=0 | no missing validator cases; one historical fail has alignment `not_applicable` | The middle compact `ZC-04` item remains the expected pre-#119 shallow-contract fail. Direct and post-fix items pass with `agama_evidence` case `ZR-05`. |

## Per-Review Alignment

| Review | Query | Overall | Contract | Alignment | Structured validator case |
|---|---|---:|---:|---:|---|
| `srq04-agama-citation-boundary-pass` | `SRQ-04` | pass | pass | pass | `agama_evidence: ZR-05` |
| `srq08-madhyamaka-nihilism-boundary-pass` | `SRQ-08` | pass | pass | pass | `madhyamaka_prasanga: ZR-09` |
| `srq09-cognitive-practice-boundary-pass` | `SRQ-09` | pass | pass | pass | `cognitive_analysis: ZR-10` |
| `srq11-collected-topics-definition-scope-pass` | `SRQ-11` | pass | pass | pass | `collected_topics: ZR-12` |
| `2026-06-18-srq-02-hetuvidya-error` | `SRQ-02` | pass | pass | pass | `hetuvidya: ZR-03` |
| `2026-06-18-srq-03-prasanga-boundary` | `SRQ-03` | pass | pass | pass | `madhyamaka_prasanga: ZR-04` |
| `2026-06-18-srq-04-agama-boundary-fixed` | `SRQ-04` | pass | pass | pass | `agama_evidence: ZR-05` |
| `2026-06-18-zc-05-agama-boundary-fixed` | `SRQ-04` | pass | pass | pass | `agama_evidence: ZR-05` |
| `2026-06-18-zc-05-prasanga-boundary-fixed` | `SRQ-03` | pass | pass | pass | `madhyamaka_prasanga: ZR-04` |
| `2026-06-20-srq-05-hetuvidya-non-pervasive` | `SRQ-05` | pass | pass | pass | `hetuvidya: ZR-07` |
| `2026-07-14-zc-03-post-prompt-cognitive-boundary` | `SRQ-09` | pass | pass | pass | `cognitive_analysis: ZR-10` |
| `2026-07-14-zc-04-post-126-agama-boundary` | `SRQ-04` | pass | pass | pass | `agama_evidence: ZR-05` |
| `2026-07-14-zc-05-broad-postfix-agama-boundary` | `SRQ-04` | pass | pass | pass | `agama_evidence: ZR-05` |
| `2026-07-14-zc-05-broad-postfix-prasanga-boundary` | `SRQ-03` | pass | pass | pass | `madhyamaka_prasanga: ZR-04` |
| `2026-07-14-zc-05-broad-postfix-nihilism-boundary` | `SRQ-08` | pass | pass | pass | `madhyamaka_prasanga: ZR-09` |
| `2026-07-14-srq-04-agama-boundary-spot` | `SRQ-04` | pass | pass | pass | `agama_evidence: ZR-05` |
| `2026-07-14-zc-04-compact-spot-before-boundary-wording-fix` | `SRQ-04` | fail | fail | not_applicable | `agama_evidence: ZR-05`; historical shallow-contract fail |
| `2026-07-14-zc-04-compact-rerun-after-boundary-wording-fix` | `SRQ-04` | pass | pass | pass | `agama_evidence: ZR-05` |

## Interpretation

- The #150/#151 alignment guard did not reveal any unexpected drift in the committed answer-review batch set.
- Every passing answer-contract review has a corresponding structured validator family with a selected reasoning case.
- The only non-pass batch result is the already-indexed compact `ZC-04` progression case, where the pre-fix answer is intentionally retained as a historical shallow-contract failure.
- This replay supports the local contract-review baseline only. It does not validate new runtime behavior or promote any provider route in `docs/platform-validation.md`.

## Limitations

- Fixture-only replay; no Codex, Claude Code, OpenAI API, Volcengine, or other provider invocation was performed.
- The checks verify explicit answer-contract slots and fixture-linked validator coverage; they do not grade doctrinal correctness.
- The replay depends on existing committed answer excerpts and samples, not newly captured transcripts.
