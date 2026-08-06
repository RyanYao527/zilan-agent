# Runtime Evidence Index

> Last updated: 2026-08-06

This index is a navigation aid for `docs/runtime-evidence/`. It does not change platform validation status. Platform status remains governed by `agents/openai.yaml` and `docs/platform-validation.md`.

## Evidence Classes

| Class | Use | May be used as `answer_file`? |
|---|---|---:|
| Standalone answer excerpt | Model answer text captured for contract review. | yes |
| Batch manifest | YAML input for `scripts/reasoning_answer_review_batch.py`. | no |
| Batch report | Human-readable saved output from a batch review. | no |
| Summary-only evidence | Runtime scenario summary, command shape, findings, and limits. | no |
| Provider/smoke evidence | Clean install, route preflight/smoke, or live-provider response summary. | no |

Do not use summary-only evidence as `answer_file` input. Use the standalone answer excerpts listed below.

## Batch Replay Reports

| Report | Inputs | Status | Notes |
|---|---|---|---|
| `2026-08-06-zc-05-srq-01-runtime-spot-review.md` | Reviews the 2026-08-06 Claude Code broad `ZC-05` runtime spot answer against `SRQ-01`, `SRQ-03`, `SRQ-04`, and `SRQ-08` | partial / fail | Final committed excerpt passes `SRQ-04` but still fails `SRQ-01`, `SRQ-03`, and `SRQ-08`; no platform-status changes. |
| `2026-08-06-srq-01-zc-05-integrated-contract-replay.md` | Replays the existing 2026-07-14 broad `ZC-05` answer excerpt against the new integrated `SRQ-01` answer contract | fail expected | Confirms the older broad answer still has explicitness gaps for `阿含证据`, `代表性检索`, `因明校验`, cognitive terms, and the `不等于修证` boundary; no provider calls or platform-status changes. |
| `2026-07-30-post-alignment-answer-review-replay.md` | Replays the 2026-07-17 and 2026-07-20 answer-review batch manifests after #150/#151 answer-validator alignment reporting | pass / fail expected | No missing structured validator cases were found; the compact `ZC-04` progression keeps its expected historical shallow-contract fail. |

## Batch Review Index

| Batch | Manifest | Inputs | Status | Notes |
|---|---|---|---|---|
| 2026-08-06 ZC-05 SRQ-01 runtime spot review | `2026-08-06-zc-05-srq-01-runtime-spot-review-batch.yaml` | 2026-08-06 Claude Code broad `ZC-05` as `SRQ-01`, `SRQ-03`, `SRQ-04`, and `SRQ-08` | partial / fail | `SRQ-04` passes; `SRQ-01`, `SRQ-03`, and `SRQ-08` still fail strict answer-contract review. |
| 2026-08-06 SRQ-01 integrated ZC-05 replay | `2026-08-06-srq-01-zc-05-integrated-contract-replay-batch.yaml` | post-#124 broad `ZC-05` as `SRQ-01` | fail expected | Strict integrated contract replay over existing evidence; records a quality gap, not a platform-status change. |
| 2026-07-20 latest ZC answer excerpt review | `2026-07-20-latest-zc-answer-excerpt-review-batch.yaml` | `ZC-03` as `SRQ-09`; post-#126 `ZC-04` as `SRQ-04`; post-#124 `ZC-05` as `SRQ-04`, `SRQ-03`, `SRQ-08` | pass | Current broad-answer pass set for the latest committed excerpts. |
| 2026-07-20 compact ZC-04 progression review | `2026-07-20-compact-zc-04-answer-excerpt-progression-batch.yaml` | direct `SRQ-04`; compact `ZC-04` before #119; compact `ZC-04` after #119 | fail expected | Records the pass -> shallow-contract fail -> pass progression. The middle fail is historical evidence. |
| 2026-07-17 runtime answer excerpt review | `2026-07-17-runtime-answer-excerpt-review-batch.yaml` | committed Claude Code runtime excerpts for `SRQ-02`, `SRQ-03`, `SRQ-04`, `SRQ-05`, and broad `ZC-05` | pass | Earlier committed runtime-answer baseline. |
| 2026-07-17 reasoning answer review | `2026-07-17-reasoning-answer-review-batch.yaml` | checked-in answer samples for `SRQ-04`, `SRQ-08`, `SRQ-09`, `SRQ-11` | pass | Fixture sample review, not runtime evidence. |

## Standalone Runtime Answer Excerpts

| Answer excerpt | Runtime source | Reviewed as | Batch/report | Status |
|---|---|---|---|---|
| `2026-08-06-claude-code-zc-05-srq-01-runtime-spot-answer.md` | broad `ZC-05` after 2026-08-06 minimum-template prompt hardening | `SRQ-01`, `SRQ-03`, `SRQ-04`, `SRQ-08` | ZC-05 SRQ-01 runtime spot review | partial / fail: `SRQ-04` pass; `SRQ-01`, `SRQ-03`, `SRQ-08` fail |
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
python scripts\reasoning_answer_review_batch.py --batch docs\runtime-evidence\2026-07-20-latest-zc-answer-excerpt-review-batch.yaml
python scripts\reasoning_answer_review_batch.py --batch docs\runtime-evidence\2026-08-06-srq-01-zc-05-integrated-contract-replay-batch.yaml
python scripts\reasoning_answer_review_batch.py --batch docs\runtime-evidence\2026-07-20-compact-zc-04-answer-excerpt-progression-batch.yaml
python scripts\reasoning_answer_review_batch.py --batch docs\runtime-evidence\2026-07-17-runtime-answer-excerpt-review-batch.yaml
```

Use direct review for an individual answer excerpt:

```powershell
python scripts\semantic_answer_contract_review.py --query-id SRQ-04 --answer-file docs\runtime-evidence\<answer-excerpt>.md
```
