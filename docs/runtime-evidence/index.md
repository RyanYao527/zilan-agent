# Runtime Evidence Index

> Last updated: 2026-09-02

This index is a navigation aid for `docs/runtime-evidence/`. It does not change platform validation status. Platform status remains governed by `agents/openai.yaml` and `docs/platform-validation.md`.

`docs/runtime-evidence/evidence_manifest.yaml` is the machine-readable v1 evidence index used by
`scripts/srq_coverage_report.py`. This Markdown file remains the human navigation surface; if the two disagree, treat
the discrepancy as manual review required rather than platform validation evidence.

## Evidence Classes

| Class | Use | May be used as `answer_file`? |
|---|---|---:|
| Standalone answer excerpt | Model answer text captured for contract review. | yes |
| Batch manifest | YAML input for `scripts/reasoning_answer_review_batch.py`. | no |
| Batch report | Human-readable saved output from a batch review. | no |
| Summary-only evidence | Runtime scenario summary, command shape, findings, and limits. | no |
| Provider/smoke evidence | Clean install, route preflight/smoke, or live-provider response summary. | no |
| Manual collation | Dated human XML-P5 or parallel-text review notes. | no |

Do not use summary-only evidence as `answer_file` input. Use the standalone answer excerpts listed below.

## Batch Replay Reports

| Report | Inputs | Status | Notes |
|---|---|---|---|
| `2026-08-20-srq11-definition-violation-alias-replay.md` | Replays the committed Volcengine OpenAI-compatible `SRQ-11` answer excerpt after exact fixture-local definition-violation marker calibration | pass | Accepts `违②` or `违三要素校验之②` as exact marker surfaces; no new provider call, prompt change, public API change, native OpenAI validation, or platform-status change. |
| `2026-08-20-volcengine-srq11-definition-live.md` | Reviews one Volcengine OpenAI-compatible live `SRQ-11` definition answer excerpt | fail | #202 route returned an answer, but the pre-calibration exact-literal answer contract failed on missing literal `违②`; not native OpenAI API evidence and no platform-status change. |
| `2026-08-19-srq11-forbidden-collision-replay.md` | Replays the committed 2026-08-19 direct `SRQ-11` runtime answer excerpt after narrowing the shallow forbidden term collision | fail | Collision with heading `性相成立的标准` is cleared; `SRQ-11` still fails missing `性相过宽`, `唯在所表上成立`, `违②`, and `definiendum_boundary`. |
| `2026-08-19-srq10-contract-calibration-replay.md` | Replays the committed 2026-08-19 direct `SRQ-10` runtime answer excerpt after exact alias-group contract calibration | pass | `SRQ-10` passes the current calibrated answer contract; no new provider call, runtime rerun, prompt change, or platform-status change. |
| `2026-08-19-srq06-srq07-contract-calibration-replay.md` | Replays the committed 2026-08-19 direct `SRQ-06` and `SRQ-07` runtime answer excerpts after exact alias-group contract calibration | pass | `SRQ-06` / `SRQ-07` pass the current calibrated answer contracts; no new provider call, runtime rerun, prompt change, or platform-status change. |
| `2026-08-19-srq06-srq07-srq10-srq11-runtime-spot-review.md` | Reviews 2026-08-19 Claude Code direct runtime spot answers for `SRQ-06`, `SRQ-07`, `SRQ-10`, and `SRQ-11` | partial | Original #193 evidence recorded four strict literal fails; current calibrated replay reports `SRQ-06` / `SRQ-07` / `SRQ-10` pass and keeps `SRQ-11` fail without the earlier heading collision. |
| `2026-08-10-zc-05-broad-runtime-rerun.md` | Reviews the 2026-08-10 Claude Code broad `ZC-05` runtime rerun answer against `SRQ-01`, `SRQ-03`, `SRQ-04`, and `SRQ-08` | pass | Confirms the new broad answer preserves the integrated no-self, prasaṅga, Agama, and nihilism-boundary slots; no provider calls through native harnesses or platform-status changes. |
| `2026-08-10-cbeta-anchor-parallel-local-replay.md` | Replays committed broad `ZC-05` evidence while recording local CBETA XML anchor probes and a high-value no-self candidate map | pass / fail expected | Confirms `SRQ-01` / `SRQ-04` still pass for the current broad spot excerpt, `SRQ-03` / `SRQ-08` remain runtime pending, and collation aids are local-only; no provider calls or platform-status changes. |
| `2026-08-07-zc05-srq03-srq08-local-replay.md` | Replays committed broad `ZC-05` excerpts plus `SRQ-03` / `SRQ-08` fixture samples after second-round prompt hardening | pass / fail expected | Confirms the local contracts and prompt invariants can see the target `不立自宗`, `二谛`, and `proposition_decomposition` gaps; no provider calls or platform-status changes. |
| `2026-08-07-srq-01-contract-calibration-replay.md` | Replays the 2026-08-06 broad `ZC-05` answer excerpt after `SRQ-01` contract calibration | pass | Confirms the same answer passes direct `SRQ-01` review once heading-like labels are separated from concrete evidence terms; no provider calls or platform-status changes. |
| `2026-08-06-zc-05-srq-01-runtime-spot-review.md` | Reviews the 2026-08-06 Claude Code broad `ZC-05` runtime spot answer against `SRQ-01`, `SRQ-03`, `SRQ-04`, and `SRQ-08` | partial / fail | After 2026-08-07 contract calibration, final committed excerpt passes `SRQ-01` and `SRQ-04`; `SRQ-03` and `SRQ-08` still fail. |
| `2026-08-06-srq-01-zc-05-integrated-contract-replay.md` | Replays the existing 2026-07-14 broad `ZC-05` answer excerpt against the new integrated `SRQ-01` answer contract | fail expected | Confirms the older broad answer still has explicitness gaps for `阿含证据`, `代表性检索`, `因明校验`, cognitive terms, and the `不等于修证` boundary; no provider calls or platform-status changes. |
| `2026-07-30-post-alignment-answer-review-replay.md` | Replays the 2026-07-17 and 2026-07-20 answer-review batch manifests after #150/#151 answer-validator alignment reporting | pass / fail expected | No missing structured validator cases were found; the compact `ZC-04` progression keeps its expected historical shallow-contract fail. |

## Batch Review Index

| Batch | Manifest | Inputs | Status | Notes |
|---|---|---|---|---|
| 2026-08-20 SRQ-11 definition violation alias replay | `2026-08-20-srq11-definition-violation-alias-replay-batch.yaml` | committed Volcengine OpenAI-compatible live answer excerpt for direct `SRQ-11` prompt | pass | `pass=1`, `fail=0`; local replay only after exact fixture-local alias calibration, while the original #202 live evidence remains historical exact-contract fail evidence. |
| 2026-08-20 Volcengine SRQ-11 definition live spot | `2026-08-20-volcengine-srq11-definition-live-batch.yaml` | Volcengine OpenAI-compatible live answer excerpt for direct `SRQ-11` prompt | fail | #202 historical batch reported `pass=0`, `fail=1`; route returned an answer, but the pre-calibration exact-literal contract missed `违②`. |
| 2026-08-19 SRQ-11 forbidden collision replay | `2026-08-19-srq11-forbidden-collision-replay-batch.yaml` | committed Claude Code direct runtime spot answer for `SRQ-11` | fail | `pass=0`, `fail=1`; collision with heading `性相成立的标准` is cleared, but explicit defining-mark boundary terms remain missing. |
| 2026-08-19 SRQ-10 contract calibration replay | `2026-08-19-srq10-contract-calibration-replay-batch.yaml` | committed Claude Code direct runtime spot answer for `SRQ-10` | pass | `pass=1`, `fail=0`; local replay only, using exact alias groups and keeping platform status unchanged. |
| 2026-08-19 SRQ-06/SRQ-07 contract calibration replay | `2026-08-19-srq06-srq07-contract-calibration-replay-batch.yaml` | committed Claude Code direct runtime spot answers for `SRQ-06` and `SRQ-07` | pass | `pass=2`, `fail=0`; local replay only, using exact alias groups and keeping platform status unchanged. |
| 2026-08-19 SRQ-06/SRQ-07/SRQ-10/SRQ-11 runtime spot review | `2026-08-19-srq06-srq07-srq10-srq11-runtime-spot-review-batch.yaml` | Claude Code direct runtime spot answers for `SRQ-06`, `SRQ-07`, `SRQ-10`, and `SRQ-11` | partial | Original #193 strict-literal snapshot was `pass=0`, `fail=4`; current calibrated replay is `pass=3`, `fail=1`, with `SRQ-11` still failing. |
| 2026-08-10 ZC-05 broad runtime rerun | `2026-08-10-zc-05-broad-runtime-rerun-batch.yaml` | 2026-08-10 Claude Code broad `ZC-05` as `SRQ-01`, `SRQ-03`, `SRQ-04`, and `SRQ-08` | pass | `pass=4`, `fail=0`; prompt-hardening follow-up not needed for `SRQ-03` / `SRQ-08` in this run. |
| 2026-08-06 ZC-05 SRQ-01 runtime spot review | `2026-08-06-zc-05-srq-01-runtime-spot-review-batch.yaml` | 2026-08-06 Claude Code broad `ZC-05` as `SRQ-01`, `SRQ-03`, `SRQ-04`, and `SRQ-08` | partial / fail | After 2026-08-07 contract calibration, `SRQ-01` and `SRQ-04` pass; `SRQ-03` and `SRQ-08` still fail strict answer-contract review. |
| 2026-08-06 SRQ-01 integrated ZC-05 replay | `2026-08-06-srq-01-zc-05-integrated-contract-replay-batch.yaml` | post-#124 broad `ZC-05` as `SRQ-01` | fail expected | Strict integrated contract replay over existing evidence; records a quality gap, not a platform-status change. |
| 2026-07-20 latest ZC answer excerpt review | `2026-07-20-latest-zc-answer-excerpt-review-batch.yaml` | `ZC-03` as `SRQ-09`; post-#126 `ZC-04` as `SRQ-04`; post-#124 `ZC-05` as `SRQ-04`, `SRQ-03`, `SRQ-08` | pass | Current broad-answer pass set for the latest committed excerpts. |
| 2026-07-20 compact ZC-04 progression review | `2026-07-20-compact-zc-04-answer-excerpt-progression-batch.yaml` | direct `SRQ-04`; compact `ZC-04` before #119; compact `ZC-04` after #119 | fail expected | Records the pass -> shallow-contract fail -> pass progression. The middle fail is historical evidence. |
| 2026-07-17 runtime answer excerpt review | `2026-07-17-runtime-answer-excerpt-review-batch.yaml` | committed Claude Code runtime excerpts for `SRQ-02`, `SRQ-03`, `SRQ-04`, `SRQ-05`, and broad `ZC-05` | pass | Earlier committed runtime-answer baseline. |
| 2026-07-17 reasoning answer review | `2026-07-17-reasoning-answer-review-batch.yaml` | checked-in answer samples for `SRQ-04`, `SRQ-08`, `SRQ-09`, `SRQ-11` | pass | Fixture sample review, not runtime evidence. |

## Standalone Runtime Answer Excerpts

| Answer excerpt | Runtime source | Reviewed as | Batch/report | Status |
|---|---|---|---|---|
| `2026-08-20-volcengine-srq11-definition-live-answer.md` | Volcengine OpenAI-compatible direct `SRQ-11` live spot | `SRQ-11` | 2026-08-20 Volcengine SRQ-11 definition live spot; definition violation alias replay | #202 historical pre-calibration exact-contract fail on missing literal `违②`; current calibrated replay pass via exact marker `违三要素校验之②` |
| `2026-08-19-claude-code-srq-06-runtime-spot-answer.md` | direct `SRQ-06` Claude Code spot | `SRQ-06` | 2026-08-19 SRQ runtime spot review; contract calibration replay | current calibrated replay pass via exact alias `无法决定`; original #193 strict-literal note recorded missing `不能决定` |
| `2026-08-19-claude-code-srq-07-runtime-spot-answer.md` | direct `SRQ-07` Claude Code spot | `SRQ-07` | 2026-08-19 SRQ runtime spot review; contract calibration replay | current calibrated replay pass via exact alias `总与别`; original #193 strict-literal note recorded missing `摄类学` |
| `2026-08-19-claude-code-srq-10-runtime-spot-answer.md` | direct `SRQ-10` Claude Code spot | `SRQ-10` | 2026-08-19 SRQ runtime spot review; contract calibration replay | current calibrated replay pass via exact cognitive-analysis alias groups; original #193 strict-literal note recorded missing explicit cognitive and corrective-factor terms |
| `2026-08-19-claude-code-srq-11-runtime-spot-answer.md` | direct `SRQ-11` Claude Code spot | `SRQ-11` | 2026-08-19 SRQ runtime spot review; forbidden collision replay | fail; heading collision cleared, but still missing explicit defining-mark boundary terms |
| `2026-08-10-claude-code-zc-05-broad-runtime-rerun-answer.md` | broad `ZC-05` after CBETA anchor and parallel-candidate preflight merge | `SRQ-01`, `SRQ-03`, `SRQ-04`, `SRQ-08` | 2026-08-10 ZC-05 broad runtime rerun | pass for all four reviewed contracts |
| `2026-08-06-claude-code-zc-05-srq-01-runtime-spot-answer.md` | broad `ZC-05` after 2026-08-06 minimum-template prompt hardening | `SRQ-01`, `SRQ-03`, `SRQ-04`, `SRQ-08` | ZC-05 SRQ-01 runtime spot review; SRQ-01 contract calibration replay | current direct `SRQ-01` pass after calibration; historical batch still records `SRQ-03` and `SRQ-08` fails |
| `2026-07-14-claude-code-srq-04-agama-boundary-spot-answer.md` | direct `SRQ-04` Agama spot review | `SRQ-04` | compact ZC-04 progression | pass |
| `2026-07-14-claude-code-zc-04-compact-spot-answer.md` | compact `ZC-04` before #119 wording fix | `SRQ-04` | compact ZC-04 progression | fail expected |
| `2026-07-14-claude-code-zc-04-compact-boundary-rerun-answer.md` | compact `ZC-04` after #119 wording fix | `SRQ-04` | compact ZC-04 progression | pass |
| `2026-07-14-claude-code-zc-03-post-prompt-answer.md` | post-prompt full rerun | `SRQ-09` | latest ZC batch | pass |
| `2026-07-14-claude-code-zc-04-post-126-answer.md` | broad `ZC-04` after #126 wording fix | `SRQ-04` | latest ZC batch | pass |
| `2026-07-14-claude-code-zc-05-broad-boundary-postfix-answer.md` | broad `ZC-05` after #124 wording fix | `SRQ-04`, `SRQ-03`, `SRQ-08`; replayed as `SRQ-01` | latest ZC batch; SRQ-01 integrated replay | pass for `SRQ-03`/`SRQ-04`/`SRQ-08`; `SRQ-01` fail expected |
| `2026-07-14-claude-code-zc-06-post-prompt-main-answer.md` | post-prompt `ZC-06` main response | not reviewed as `answer_file` | not in batch | file-completion notice only; local report path redacted |
| `2026-06-20-claude-code-srq-05-spot-review-answer.md` | `SRQ-05` Hetuvidya spot review | `SRQ-05` | 2026-07-17 runtime batch | pass |
| `2026-06-18-claude-code-post-contract-srq-02-answer.md` | post-contract target review | `SRQ-02` | 2026-07-17 runtime batch | pass |
| `2026-06-18-claude-code-post-contract-srq-03-answer.md` | post-contract target review | `SRQ-03` | 2026-07-17 runtime batch | pass |
| `2026-06-18-claude-code-agama-contract-fix-srq-04-answer.md` | Agama contract-fix target review | `SRQ-04` | 2026-07-17 runtime batch | pass |
| `2026-06-18-claude-code-agama-contract-fix-zc-05-answer.md` | broad `ZC-05` Agama contract-fix review | `SRQ-04` | 2026-07-17 runtime batch | pass |
| `2026-06-18-claude-code-madhyamaka-contract-fix-zc-05-answer.md` | broad `ZC-05` Madhyamaka contract-fix review | `SRQ-03` | 2026-07-17 runtime batch | pass |

## Standalone Excerpts Not In Current Batches

| Answer excerpt | Source | Notes |
|---|---|---|
| `2026-06-18-claude-code-post-contract-srq-04-answer.md` | post-contract target review | Retained as historical answer evidence; use direct `semantic_answer_contract_review.py --query-id SRQ-04 --answer-file ...` if needed. |
| `2026-06-18-claude-code-post-contract-zc-05-answer.md` | post-contract full rerun | Retained as historical broad `ZC-05` evidence; later fixed broad `ZC-05` excerpts are indexed above. |

## Summary-Only Runtime Evidence

| Evidence summary | Scope | Answer excerpt status |
|---|---|---|
| `2026-09-02-srq04-citation-anchor-section-refinement.md` | records per-chunk SRQ-04 citation anchor detail and confirms `agama:T01n0001:juan-3:line-1829` remains `section_label_status=source_unavailable` after local Markdown/XML-P5 inspection | summary-only citation refinement; XML anchor location is visible, but textual equivalence, source dependence, publication-ready collation, runtime answer pass, and platform validation remain unproven |
| `2026-09-01-srq04-reviewer-decision-ingestion-path.md` | documents the local ingestion path for future `SRQ-04` reviewer decisions, including dated evidence-note requirements for non-pending decisions | summary-only ingestion path; no new human conclusion, no answer excerpt, no candidate-map conclusion change, and `SRQ-04` remains `manual_review_required` |
| `2026-08-21-srq04-reviewer-decision-intake.md` | adds a structured pending reviewer-decision intake fixture for the three current `SRQ-04` XML-P5 no-self candidate sets | summary-only intake; all decisions remain pending and do not establish textual equivalence, source dependence, publication-ready collation, runtime answer evidence, or platform validation evidence |
| `2026-08-20-srq04-manual-semantic-boundary-queue.md` | queues the current `SRQ-04` manual semantic-boundary review over three existing XML-P5 no-self candidate sets | summary-only reviewer queue; anchor-located and limited theme-parallel evidence remains `manual_review_required`, not textual equivalence, source-dependence evidence, runtime answer evidence, or platform validation evidence |
| `2026-08-20-srq11-definition-violation-alias-replay.md` | local replay over committed Volcengine OpenAI-compatible `SRQ-11` answer excerpt after exact fixture-local definition-violation marker calibration | summary-only replay note; current calibrated batch pass for `SRQ-11`; not a new runtime run or platform validation evidence |
| `2026-08-20-volcengine-srq11-definition-live.md` | Volcengine OpenAI-compatible direct `SRQ-11` live spot with committed answer excerpt and batch review | links standalone answer excerpt; #202 batch status was pre-calibration fail on missing literal `违②`; not native OpenAI API evidence and not platform-status evidence |
| `2026-08-19-srq04-manual-collation-boundary-closeout.md` | consolidated `SRQ-04` manual XML-P5 collation boundary map for anchor-located, limited theme-parallel, and still-unreviewed source-dependence/publication claims | summary-only manual collation boundary note; not runtime answer evidence, not an `answer_file`, and still `manual_review_required` |
| `2026-08-19-srq11-definition-runtime-rerun.md` | bounded Claude Code runtime rerun attempt after `SRQ-11` definition-boundary prompt hardening | summary-only blocked note; no answer excerpt was produced because the local Claude Code custom DeepSeek model setting was rejected, so runtime remains pending |
| `2026-08-19-srq11-definition-prompt-hardening-local-replay.md` | local prompt-invariant evidence for `SRQ-11` definition-boundary slots | summary-only prompt-prepared note; existing committed `SRQ-11` runtime answer remains fail and a new runtime rerun is pending |
| `2026-08-19-srq11-forbidden-collision-replay.md` | local replay over committed direct `SRQ-11` runtime answer excerpt after narrowing the shallow forbidden collision | summary-only replay note; current calibrated batch remains fail for `SRQ-11`; not a new runtime run or platform validation evidence |
| `2026-08-19-srq10-contract-calibration-replay.md` | local replay over committed direct `SRQ-10` runtime answer excerpt after exact alias-group contract calibration | summary-only replay note; current calibrated batch pass for `SRQ-10`; not a new runtime run or platform validation evidence |
| `2026-08-19-srq06-srq07-contract-calibration-replay.md` | local replay over committed direct `SRQ-06` and `SRQ-07` runtime answer excerpts after exact alias-group contract calibration | summary-only replay note; current calibrated batch pass for `SRQ-06` / `SRQ-07`; not a new runtime run or platform validation evidence |
| `2026-08-19-pr-193-manual-review.md` | manual blocker scan and merge-readiness note for PR #193 | summary-only PR review; recommends converting #193 from Draft to Ready and squash merging when checks remain green; not runtime answer evidence, not provider validation evidence, and not platform-status evidence |
| `2026-08-19-za-long-agama-no-self-verse-manual-collation.md` | limited manual XML-P5 review for one cross-Agama `SRQ-04` no-self candidate pair from `T02n0099` / `T01n0001` | summary-only; limited theme parallel, not textual equivalence, source-dependence evidence, runtime answer evidence, or platform validation evidence |
| `2026-08-19-srq06-srq07-srq10-srq11-runtime-spot-review.md` | Claude Code direct runtime spot review for `SRQ-06`, `SRQ-07`, `SRQ-10`, and `SRQ-11` | links standalone answer excerpts; current calibrated replay passes `SRQ-06` / `SRQ-07` / `SRQ-10` and keeps `SRQ-11` fail |
| `2026-08-19-srq-manual-review-note.md` | reviewer record for earlier `SRQ-04`, `SRQ-06`, `SRQ-07`, `SRQ-10`, and `SRQ-11` manifest-facing evidence gaps | historical summary-only review record; later committed excerpts and exact alias-group replays supersede `SRQ-06` / `SRQ-07` / `SRQ-10` not-reviewed observations; not runtime answer evidence or platform validation evidence |
| `2026-08-19-srq-manual-review-handoff.md` | human handoff checklist for conservative SRQ evidence gaps surfaced by `scripts/srq_coverage_report.py` | summary-only handoff; not runtime evidence and not an `answer_file` |
| `2026-08-12-no-self-parallel-manual-collation.md` | limited manual XML-P5 review for one high-value no-self parallel candidate pair from `T02n0099` / `T01n0001` | summary-only; limited theme parallel, not textual equivalence, runtime answer evidence, or platform validation evidence |
| `2026-08-12-long-agama-no-self-verse-manual-collation.md` | limited manual XML-P5 review for one `SRQ-04` Long Agama no-self verse candidate pair from `T01n0001` | summary-only; limited theme parallel, not textual equivalence, runtime answer evidence, or platform validation evidence |
| `2026-08-10-zc-05-broad-runtime-rerun.md` | Claude Code broad `ZC-05` runtime rerun and local replay for `SRQ-01`, `SRQ-03`, `SRQ-04`, and `SRQ-08` | links standalone answer excerpt; batch status pass |
| `2026-08-10-cbeta-anchor-parallel-local-replay.md` | local CBETA XML anchor probes, high-value no-self candidate map, and reasoning/retrieval replay refresh | summary-only; anchor/candidate preflight plus later limited manual collation follow-up; broad runtime pending in that replay |
| `2026-08-07-zc05-srq03-srq08-local-replay.md` | local replay over committed broad `ZC-05` excerpts and `SRQ-03` / `SRQ-08` samples after second-round prompt hardening | summary-only; prompt prepared, runtime pending |
| `2026-08-07-zc05-srq03-srq08-prompt-hardening-local.md` | local broad `ZC-05` second-round prompt hardening for `SRQ-03` / `SRQ-08` literal slots | summary-only; prompt prepared, runtime pending |
| `2026-08-07-srq-01-contract-calibration-replay.md` | Local `SRQ-01` answer-contract replay after heading-label calibration | direct `SRQ-01` pass over the 2026-08-06 broad `ZC-05` excerpt |
| `2026-08-06-zc-05-srq-01-runtime-spot-review.md` | Claude Code broad `ZC-05` runtime spot review after integrated `SRQ-01` prompt hardening | links standalone answer excerpt; batch status partial / fail |
| `2026-08-06-zc05-srq01-prompt-hardening-local.md` | local broad `ZC-05` / integrated `SRQ-01` prompt hardening evidence | summary-only; prompt prepared, runtime pending |
| `2026-07-14-claude-code-post-prompt-zc-01-zc-06-rerun.md` | Claude Code `ZC-01` through `ZC-06` post-prompt rerun | links `ZC-03` and redacted `ZC-06` excerpts |
| `2026-07-14-claude-code-broad-boundary-postfix-review.md` | broad `ZC-04` / `ZC-05` post-#124 review | links broad `ZC-05` excerpt |
| `2026-07-14-claude-code-zc-04-post-126-agama-slot-rerun.md` | broad `ZC-04` post-#126 rerun | links broad `ZC-04` excerpt |
| `2026-07-14-claude-code-srq-04-zc-04-agama-boundary-spot-review.md` | direct `SRQ-04` plus compact `ZC-04` spot review | links direct `SRQ-04` and compact pre-fix excerpts |
| `2026-07-14-claude-code-zc-04-agama-boundary-rerun.md` | compact `ZC-04` post-#119 rerun | links compact post-fix excerpt |
| `2026-07-13-claude-code-srq-11-spot-review.md` | Collected Topics definition-scope spot review | summary-only |
| `2026-07-06-claude-code-srq-09-spot-review.md` | cognitive/practice-boundary spot review | summary-only |
| `2026-07-06-claude-code-srq-09-boundary-fix.md` | cognitive/practice-boundary fix evidence | summary-only |
| `2026-07-02-claude-code-srq-07-collected-topics-boundary-fix.md` | Collected Topics total/part boundary fix | summary-only |
| `2026-06-28-claude-code-srq-08-zc-05-spot-review.md` | `SRQ-08` / `ZC-05` spot review | summary-only |
| `2026-06-28-claude-code-srq-08-boundary-fix.md` | Madhyamaka nihilism-boundary fix | summary-only |
| `2026-06-18-claude-code-post-contract-target-review.md` | `SRQ-02` through `SRQ-04` target review | links historical answer excerpts |
| `2026-06-18-claude-code-post-contract-full-rerun.md` | Claude Code `ZC-01` through `ZC-06` post-contract rerun | summary-only |
| `2026-06-18-claude-code-agama-contract-fix-review.md` | Agama contract-fix review | links `SRQ-04` and broad `ZC-05` excerpts |
| `2026-06-18-claude-code-madhyamaka-contract-fix-review.md` | Madhyamaka contract-fix review | links broad `ZC-05` excerpt |

## Provider And Smoke Evidence

| Evidence file | Scope |
|---|---|
| `2026-08-20-volcengine-srq11-definition-live.md` | Volcengine OpenAI-compatible direct `SRQ-11` live spot; answer returned and contract-reviewed as fail on exact `违②`, without validating native OpenAI API or changing platform status |
| `2026-08-19-claude-code-route-preflight-local.md` | Claude Code local route preflight showing the CLI is present but the custom DeepSeek Anthropic-compatible model remains blocked before answer generation; no provider calls or platform-status changes |
| `2026-08-03-codex-desktop-maintenance-smoke.md` | Codex Desktop migration step 1 local maintenance baseline; repository validation, pytest, ruff, and mypy passed without changing platform status. |
| `2026-06-16-volcengine-openai-compatible-zc-01-zc-03-live.md` | Volcengine OpenAI-compatible `ZC-01` through `ZC-03` live summary |
| `2026-06-16-volcengine-openai-compatible-zc-02-live.md` | Volcengine OpenAI-compatible `ZC-02` live detail |
| `2026-08-05-openai-harness-preflight-local.md` | Native OpenAI and Volcengine-compatible local preflight route-resolution smoke; no provider calls or platform-status changes |
| `2026-06-16-claude-code-utf8-rerun.md` | Claude Code UTF-8 stdin rerun |
| `2026-06-15-codex-v245-runtime-rerun.md` | Codex v2.4.5 runtime rerun |
| `2026-06-15-clean-install-smoke.md` | clean install smoke |
| `2026-06-15-mock-claude-install-smoke.md` | mock Claude install smoke |

## Review Commands

Use batch manifests for grouped review:

```powershell
python scripts\reasoning_answer_review_batch.py --batch docs\runtime-evidence\2026-08-20-srq11-definition-violation-alias-replay-batch.yaml
python scripts\reasoning_answer_review_batch.py --batch docs\runtime-evidence\2026-08-19-srq11-forbidden-collision-replay-batch.yaml
python scripts\reasoning_answer_review_batch.py --batch docs\runtime-evidence\2026-08-20-volcengine-srq11-definition-live-batch.yaml
python scripts\reasoning_answer_review_batch.py --batch docs\runtime-evidence\2026-08-19-srq10-contract-calibration-replay-batch.yaml
python scripts\reasoning_answer_review_batch.py --batch docs\runtime-evidence\2026-08-19-srq06-srq07-contract-calibration-replay-batch.yaml
python scripts\reasoning_answer_review_batch.py --batch docs\runtime-evidence\2026-08-10-zc-05-broad-runtime-rerun-batch.yaml
python scripts\reasoning_answer_review_batch.py --batch docs\runtime-evidence\2026-08-19-srq06-srq07-srq10-srq11-runtime-spot-review-batch.yaml
python scripts\reasoning_answer_review_batch.py --batch docs\runtime-evidence\2026-07-20-latest-zc-answer-excerpt-review-batch.yaml
python scripts\reasoning_answer_review_batch.py --batch docs\runtime-evidence\2026-08-06-srq-01-zc-05-integrated-contract-replay-batch.yaml
python scripts\reasoning_answer_review_batch.py --batch docs\runtime-evidence\2026-07-20-compact-zc-04-answer-excerpt-progression-batch.yaml
python scripts\reasoning_answer_review_batch.py --batch docs\runtime-evidence\2026-07-17-runtime-answer-excerpt-review-batch.yaml
```

Build the local SRQ-04 human-review packet:

```powershell
python scripts\srq04_manual_review_packet.py
python scripts\srq04_manual_review_packet.py --json
```

Use direct review for an individual answer excerpt:

```powershell
python scripts\semantic_answer_contract_review.py --query-id SRQ-01 --answer-file docs\runtime-evidence\2026-08-06-claude-code-zc-05-srq-01-runtime-spot-answer.md
python scripts\semantic_answer_contract_review.py --query-id SRQ-04 --answer-file docs\runtime-evidence\<answer-excerpt>.md
```
