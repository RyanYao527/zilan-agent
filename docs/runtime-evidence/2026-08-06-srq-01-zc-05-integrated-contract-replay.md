# 2026-08-06 SRQ-01 / ZC-05 Integrated Contract Replay

## Scope

This batch review applies the newly added `SRQ-01` `cross_domain_no_self_analysis` answer contract to an existing standalone
Claude Code broad `ZC-05` answer excerpt:

- `docs/runtime-evidence/2026-07-14-claude-code-zc-05-broad-boundary-postfix-answer.md`

The same excerpt remains useful historical evidence for the narrower `SRQ-03`, `SRQ-04`, and `SRQ-08` checks. This replay
asks a different question: whether that older broad answer also satisfies the newer integrated `SRQ-01` answer surface.

## Command

```powershell
python scripts\reasoning_answer_review_batch.py --batch docs\runtime-evidence\2026-08-06-srq-01-zc-05-integrated-contract-replay-batch.yaml
```

## Boundary

This is a local review over already committed runtime answer evidence. It does not call Claude Code, Codex, OpenAI, or any
OpenAI-compatible provider; it does not generate a new answer; it does not grade doctrine; and it does not change platform
validation status in `agents/openai.yaml` or `docs/platform-validation.md`.

## Output

```text
# Reasoning Answer Review Batch

Batch: docs/runtime-evidence/2026-08-06-srq-01-zc-05-integrated-contract-replay-batch.yaml
Overall status: fail
Summary: pass=0, fail=1, review_needed=0, other=0

Boundary: batch fixture review only; this is not runtime platform validation.

## Reviews
- 2026-07-14-zc-05-broad-postfix-srq-01-integrated-replay: fail (SRQ-01)
  missing: cross_domain_no_self_analysis:阿含证据, cross_domain_no_self_analysis:代表性检索, cross_domain_no_self_analysis:因明校验, cross_domain_no_self_analysis:我所, cross_domain_no_self_analysis:触, cross_domain_no_self_analysis:作意, cross_domain_no_self_analysis:想, cross_domain_no_self_analysis:思, cross_domain_no_self_analysis:不等于修证

## Limitations
- Batch review only orchestrates local fixture answer reviews; it does not call providers or generate answers.
- Each batch item uses the same shallow answer-contract and structured-validator limitations as a single review.
- Batch status is a review convenience signal, not platform validation or doctrinal grading.
```

## Findings

The replay is an expected strict-contract failure. The older broad `ZC-05` excerpt preserves the narrower Agama,
Madhyamaka prasaṅga, and nihilism-boundary surfaces, but it does not explicitly expose the full integrated `SRQ-01`
surface now required for cross-domain no-self answers.

This does not invalidate the prior `SRQ-03`, `SRQ-04`, or `SRQ-08` pass evidence. It records the next quality gap: future
broad `ZC-05` runtime work should preserve the integrated `SRQ-01` terms and cognitive/practice boundary slots when a
new answer is generated or prompt wording is intentionally changed.
