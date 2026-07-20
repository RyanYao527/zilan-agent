# 2026-07-20 Compact ZC-04 Answer Excerpt Progression Batch

## Scope

This batch review applies `scripts/reasoning_answer_review_batch.py` to newly committed standalone answer excerpts from the 2026-07-14 compact `SRQ-04` / `ZC-04` Agama citation-boundary runtime reviews.

Included excerpts:

- direct `SRQ-04` Agama citation-boundary spot-review answer from repository base `512a333`
- compact `ZC-04` spot-review answer from repository base `512a333`
- compact `ZC-04` boundary rerun answer after the #119 Agama collation-boundary wording fix from repository base `25bdb5d`

This batch intentionally includes the pre-#119 compact `ZC-04` answer that fails the shallow forbidden-term contract because it used the negated phrase `校勘确认`. The later compact rerun passes after the prompt wording change. The purpose is to make the failure and fix progression mechanically auditable, not to claim a new runtime platform pass.

## Command

```powershell
python scripts\reasoning_answer_review_batch.py --batch docs\runtime-evidence\2026-07-20-compact-zc-04-answer-excerpt-progression-batch.yaml
```

## Boundary

This is a local review over already generated and newly committed runtime answer excerpts. It does not call Claude Code, Codex, OpenAI, or any OpenAI-compatible provider; it does not generate answers; it does not grade doctrine; and it does not change platform validation status in `agents/openai.yaml` or `docs/platform-validation.md`.

## Output

```text
# Reasoning Answer Review Batch

Batch: docs/runtime-evidence/2026-07-20-compact-zc-04-answer-excerpt-progression-batch.yaml
Overall status: fail
Summary: pass=2, fail=1, review_needed=0, other=0

Boundary: batch fixture review only; this is not runtime platform validation.

## Reviews
- 2026-07-14-srq-04-agama-boundary-spot: pass (SRQ-04)
- 2026-07-14-zc-04-compact-spot-before-boundary-wording-fix: fail (SRQ-04)
- 2026-07-14-zc-04-compact-rerun-after-boundary-wording-fix: pass (SRQ-04)

## Limitations
- Batch review only orchestrates local fixture answer reviews; it does not call providers or generate answers.
- Each batch item uses the same shallow answer-contract and structured-validator limitations as a single review.
- Batch status is a review convenience signal, not platform validation or doctrinal grading.
```

## Interpretation

The failed middle item is retained as historical evidence of the pre-#119 wording gap. The final item shows the compact `ZC-04` path passing `SRQ-04` after the wording fix, while the broader post-#126 `ZC-04` path is covered separately in `docs/runtime-evidence/2026-07-20-latest-zc-answer-excerpt-review-batch.md`.
