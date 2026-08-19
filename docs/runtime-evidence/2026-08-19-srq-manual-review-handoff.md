# 2026-08-19 SRQ Evidence Manual Review Handoff

This handoff is for human review of conservative evidence gaps surfaced by
`scripts/srq_coverage_report.py`. It is not runtime evidence by itself and must not be used as an `answer_file`.

The completed reviewer note for this handoff is
`docs/runtime-evidence/2026-08-19-srq-manual-review-note.md`.

Later committed standalone answer excerpts and exact alias-group replays supersede the original `not_reviewed`
observations for `SRQ-06`, `SRQ-07`, and `SRQ-10`; the committed `SRQ-11` excerpt is now tracked as explicit fail
evidence after the shallow forbidden collision was narrowed. Use `docs/runtime-evidence/evidence_manifest.yaml` and
`scripts/srq_coverage_report.py` for the current machine-readable status.

## Scope

Run the local coverage report first:

```powershell
python scripts\srq_coverage_report.py
python scripts\srq_coverage_report.py --json
```

Expected current triage:

| Case | Coverage status | Runtime evidence status | Reviewer task |
| --- | --- | --- | --- |
| `SRQ-04` | `manual_review_required` | `pass`, `fail_expected`, `manual_review_required` | Review manual XML-P5 collation notes and confirm the semantic boundary is limited theme-parallel evidence, not textual equivalence or runtime pass. |
| `SRQ-06` | `ready` | `pass` | Current committed excerpt passes local exact alias-group replay; no new runtime run or platform-status change. |
| `SRQ-07` | `ready` | `pass` | Current committed excerpt passes local exact alias-group replay; no new runtime run or platform-status change. |
| `SRQ-10` | `ready` | `pass` | Current committed excerpt passes local exact alias-group replay; no new runtime run or platform-status change. |
| `SRQ-11` | `fail` | `fail` | Current committed excerpt no longer hits the `性相成立` heading collision, but still fails missing explicit defining-mark boundary slots; no new runtime run or platform-status change. |

## Global Rules

- Do not update `docs/platform-validation.md`.
- Do not update `agents/openai.yaml`.
- Do not call providers unless a separate runtime-validation task explicitly asks for it.
- Do not treat local replay, fixture pass, batch manifest, summary-only evidence, or manual collation as runtime pass.
- Do not use `summary_only`, `batch_manifest`, `batch_report`, `manual_collation`, or `provider_smoke` files as `answer_file`.
- Only a standalone answer excerpt can be reviewed as `answer_file`.
- If evidence is insufficient, keep or recommend `not_reviewed`, `runtime_pending`, or `manual_review_required`.

## Common Local Checks

Run these before and after the review if any file is changed:

```powershell
python scripts\validate_zilan_repo.py --strict-yaml
python scripts\srq_coverage_report.py
python scripts\srq_coverage_report.py --json
```

Use these commands to sanity-check the checked-in pass/fail answer samples. These are fixture checks only; they are not runtime evidence:

```powershell
python scripts\semantic_answer_contract_review.py --query-id SRQ-04 --sample-id srq04-agama-citation-boundary-pass --json
python scripts\semantic_answer_contract_review.py --query-id SRQ-04 --sample-id srq04-agama-citation-boundary-fail --json
python scripts\semantic_answer_contract_review.py --query-id SRQ-06 --sample-id srq06-hetuvidya-indeterminate-pass --json
python scripts\semantic_answer_contract_review.py --query-id SRQ-06 --sample-id srq06-hetuvidya-indeterminate-fail --json
python scripts\semantic_answer_contract_review.py --query-id SRQ-07 --sample-id srq07-collected-topics-total-part-pass --json
python scripts\semantic_answer_contract_review.py --query-id SRQ-07 --sample-id srq07-collected-topics-total-part-fail --json
python scripts\semantic_answer_contract_review.py --query-id SRQ-10 --sample-id srq10-cognitive-caregiving-boundary-pass --json
python scripts\semantic_answer_contract_review.py --query-id SRQ-10 --sample-id srq10-cognitive-caregiving-boundary-fail --json
python scripts\semantic_answer_contract_review.py --query-id SRQ-11 --sample-id srq11-collected-topics-definition-scope-pass --json
python scripts\semantic_answer_contract_review.py --query-id SRQ-11 --sample-id srq11-collected-topics-definition-scope-fail --json
```

If a reviewer has a new standalone answer excerpt, review it with:

```powershell
python scripts\semantic_answer_contract_review.py --query-id <SRQ-ID> --answer-file docs\runtime-evidence\<dated-answer-excerpt>.md --json
```

## SRQ-04 Manual Collation Review

Review files:

- `docs/runtime-evidence/2026-08-12-no-self-parallel-manual-collation.md`
- `docs/runtime-evidence/2026-08-12-long-agama-no-self-verse-manual-collation.md`
- `tests/fixtures/collation/high_value_no_self_parallel_candidates.yaml`
- `docs/runtime-evidence/evidence_manifest.yaml`

Optional local preflight:

```powershell
python scripts\cbeta_collation_preflight.py --check-anchors --json
```

Reviewer must decide:

- Are the dated manual XML-P5 notes correctly limited to theme-parallel or candidate-level evidence?
- Do they avoid claiming textual equivalence, source dependence, publication-level collation, or runtime answer pass?
- Is `manual_review_required` still the right manifest-facing status?

Acceptable outcomes:

- Keep `manual_review_required` if evidence is still limited manual collation.
- Recommend a new dated manual collation note only if the reviewer has checked concrete XML-P5 anchors and can state the limitation.
- Do not recommend `pass` unless there is a separate standalone answer excerpt reviewed against `SRQ-04`.

## SRQ-06 Runtime Evidence Gap

Scope: Hetuvidya `不定因` / `inconclusive_or_contradictory` case.

Local structure check:

```powershell
python scripts\reasoning_contract_runner.py --query-id SRQ-06 --json
```

Reviewer must decide:

- Is there a committed standalone runtime answer excerpt for `SRQ-06`?
- If yes, does it pass direct `SRQ-06` contract review as an `answer_file`?
- If no, keep `not_reviewed`.

Do not treat fixture sample pass as runtime pass.

## SRQ-07 Runtime Evidence Gap

Scope: Collected Topics total/part overgeneralization case.

Local structure check:

```powershell
python scripts\reasoning_contract_runner.py --query-id SRQ-07 --json
```

Reviewer must decide:

- Is there a committed standalone runtime answer excerpt for `SRQ-07`?
- If yes, does it pass direct `SRQ-07` contract review as an `answer_file`?
- If no, keep `not_reviewed`.

Do not treat fixture sample pass as runtime pass.

## SRQ-10 Runtime Evidence Gap

Scope: cognitive-analysis and practice-boundary case for caregiving-pressure attribution.

Local structure check:

```powershell
python scripts\reasoning_contract_runner.py --query-id SRQ-10 --json
```

Reviewer must decide:

- Is there a committed standalone runtime answer excerpt for `SRQ-10`?
- If yes, does it pass direct `SRQ-10` contract review as an `answer_file`?
- If no, keep `not_reviewed`.

Do not treat fixture sample pass as runtime pass.

## SRQ-11 Runtime Evidence Gap

Scope: Collected Topics definition-scope case for `瓶的性相是能盛水者`.

Local structure check:

```powershell
python scripts\reasoning_contract_runner.py --query-id SRQ-11 --json
```

Reviewer must decide:

- Historical note: the original handoff only saw fixture sample review, not standalone runtime answer evidence.
- Current note: a committed standalone runtime answer excerpt exists and remains `fail` after the shallow heading
  collision is cleared.
- Future reviewer task: decide whether a later prompt or answer-contract change can make the defining-mark boundary
  terms explicit without turning local replay into runtime pass evidence.

Do not treat the 2026-07-17 reasoning answer review batch as runtime pass.

## Reviewer Output Template

Use this template in the reviewer handoff note or PR comment:

```text
Reviewer:
Date:
Repository branch / commit:

Commands run:
- python scripts\srq_coverage_report.py
- python scripts\srq_coverage_report.py --json
- ...

Files inspected:
- ...

Case decisions:
- SRQ-04:
- SRQ-06:
- SRQ-07:
- SRQ-10:
- SRQ-11:

Evidence recommendation:
- Keep manifest unchanged:
- Update manifest status:
- Add standalone answer excerpt:
- Add summary-only/manual collation note:

Platform status:
- No docs/platform-validation.md change.
- No agents/openai.yaml change.

Limits / blockers:
- ...
```

## Done Criteria

The review is complete when:

- Each scoped SRQ has an explicit decision: keep current status, add limited evidence, or add a new standalone answer excerpt for contract review.
- Any proposed manifest update preserves `platform_status_change: false`.
- Any proposed answer review uses only a standalone answer excerpt.
- The final note says clearly whether the result is runtime pass, runtime fail, runtime pending, not reviewed, or manual review required.
