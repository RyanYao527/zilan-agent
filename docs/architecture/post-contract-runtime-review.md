# Post-Contract Runtime Review

> Date: 2026-06-18  
> Base commit: `743b7cf`  
> Status: review of committed runtime evidence summaries, not a new runtime validation pass.

This note checks existing ZC runtime evidence against the newer `SRQ-02` through `SRQ-04` answer contracts. It does not run a provider, does not generate answers, does not use an LLM judge, and does not change any platform status.

## Scope

User-requested runtime outputs:

- `ZC-02`: concept lookup, "孜澜，什么是因三相？"
- `ZC-03`: cross-domain explanation, "收到批评后我很受挫"
- `ZC-05`: cross-domain research, "用应成论式分析诸法无我，并串联阿含、摄类学、因明和观禅"

Contracts checked:

- `SRQ-02` / `hetuvidya_error_detection`: the target edge case is "声，应是可见，以是色形故。"
- `SRQ-03` / `madhyamaka_prasanga_boundary`: the target edge case is "若有人承许诸法自性有，如何用应成法指出矛盾？"
- `SRQ-04` / `agama_citation_boundary`: the target edge case is "查四阿含中关于无我的经文，并说明检索范围与待校勘边界。"

Evidence inputs:

- `docs/runtime-evidence/2026-06-16-volcengine-openai-compatible-zc-02-live.md`
- `docs/runtime-evidence/2026-06-16-volcengine-openai-compatible-zc-01-zc-03-live.md`
- `docs/runtime-evidence/2026-06-15-codex-v245-runtime-rerun.md`
- `docs/runtime-evidence/2026-06-16-claude-code-utf8-rerun.md`
- `docs/runtime-validation-log.md`
- `tests/fixtures/retrieval_chunks/semantic_chunks.yaml`

Important boundary: the committed runtime evidence files are compact summaries, not full answer transcripts. A mechanical contract failure below means the committed evidence excerpt does not prove the contract was satisfied. It does not prove the original full runtime answer failed unless a full transcript is available.

## Mechanical Checks

These local checks used the committed evidence excerpts as `--answer-file` input:

```powershell
python scripts\semantic_answer_contract_review.py --query-id SRQ-02 --answer-file docs\runtime-evidence\2026-06-16-volcengine-openai-compatible-zc-02-live.md --json
python scripts\semantic_answer_contract_review.py --query-id SRQ-02 --answer-file docs\runtime-evidence\2026-06-16-volcengine-openai-compatible-zc-01-zc-03-live.md --json
python scripts\semantic_answer_contract_review.py --query-id SRQ-03 --answer-file docs\runtime-evidence\2026-06-15-codex-v245-runtime-rerun.md --json
python scripts\semantic_answer_contract_review.py --query-id SRQ-03 --answer-file docs\runtime-evidence\2026-06-16-claude-code-utf8-rerun.md --json
python scripts\semantic_answer_contract_review.py --query-id SRQ-04 --answer-file docs\runtime-evidence\2026-06-15-codex-v245-runtime-rerun.md --json
python scripts\semantic_answer_contract_review.py --query-id SRQ-04 --answer-file docs\runtime-evidence\2026-06-16-claude-code-utf8-rerun.md --json
```

| Contract | Evidence file | Mechanical result | Missing required terms | Interpretation |
|---|---|---:|---|---|
| `SRQ-02` Hetuvidya error detection | Volcengine `ZC-02` live excerpt | `fail` | `因不成`, `色形`, `不成立` | Expected. `ZC-02` explains positive `因三相`; it does not test the negative edge case "声可见，以是色形故". |
| `SRQ-02` Hetuvidya error detection | Volcengine `ZC-03` live excerpt | `fail` | `因不成`, `遍是宗法性`, `色形`, `声`, `不成立` | Expected. `ZC-03` covers a work-feedback `不周遍` cognitive case, not the `色形` reason-unestablished prompt. |
| `SRQ-03` Madhyamaka prasaṅga boundary | Codex `ZC-05` v2.4.5 excerpt | `fail` | `对方承许`, `归谬`, `自性有`, `缘起`, `矛盾`, `不立自宗` | Evidence summary says ZC-05 connected Madhyamaka and boundaries, but it does not preserve enough transcript detail to prove the prasaṅga boundary contract. |
| `SRQ-03` Madhyamaka prasaṅga boundary | Claude Code `ZC-05` UTF-8 excerpt | `fail` | `对方承许`, `归谬`, `自性有`, `缘起`, `矛盾`, `不立自宗` | Same evidence-granularity gap. The committed excerpt is too compact for contract-level confirmation. |
| `SRQ-04` Agama citation boundary | Codex `ZC-05` v2.4.5 excerpt | `fail` | `CBETA`, `T02n0099`, `context/agama/`, `检索范围`, `代表性`, `待校勘` | Evidence summary says local citations and textual boundaries existed, but it does not prove CBETA identity, representative-status language, or collation boundary in the answer text. |
| `SRQ-04` Agama citation boundary | Claude Code `ZC-05` UTF-8 excerpt | `fail` | `CBETA`, `T02n0099`, `context/agama/`, `检索范围`, `代表性`, `待校勘` | Same evidence-granularity gap. The compact excerpt is not enough for SRQ-04. |

## Findings

1. `ZC-02` remains valid for the original concept-lookup regression, but it does not cover `SRQ-02`. The real gap is that the targeted "声，应是可见，以是色形故" prompt has not been runtime-tested.
2. `ZC-03` remains valid for the work-feedback cognitive-analysis regression and maps better to `ZR-02`, not to `SRQ-02` through `SRQ-04`. Its `不周遍` reasoning is useful, but it is not a substitute for the Hetuvidya error-detection prompt.
3. `ZC-05` has summary-level evidence for broad cross-domain reasoning, but the committed evidence is too compressed to prove `SRQ-03` or `SRQ-04`. This is primarily an evidence-capture gap; it may also hide answer-quality gaps, but the current repository cannot distinguish those without transcript-backed excerpts.
4. None of these results should downgrade Codex, Claude Code, or Volcengine platform status. The existing platform validation was scoped to the old ZC expectations; `SRQ-02` through `SRQ-04` are newer, narrower answer-contract checks.

## Highest-ROI Next Step

Follow-up executed on 2026-06-18: `docs/runtime-evidence/2026-06-18-claude-code-post-contract-target-review.md` records a Claude Code UTF-8 target review with committed answer excerpts for `SRQ-02`, `SRQ-03`, `SRQ-04`, and `ZC-05`.

Result: targeted `SRQ-02` and `SRQ-03` passed their current answer contracts. Targeted `SRQ-04` failed only the local-anchor / representative-status terms (`context/agama/`, `代表性`). Broad `ZC-05` still failed the narrow `SRQ-03` and `SRQ-04` contracts, showing that the cross-domain prompt needs stronger output-contract guidance if those boundaries should be guaranteed in broad answers.

Second follow-up executed on 2026-06-18: `docs/runtime-evidence/2026-06-18-claude-code-agama-contract-fix-review.md` records the narrow Agama evidence output-contract fix. Result: direct `SRQ-04` and broad `ZC-05` now pass the `SRQ-04` Agama citation-boundary contract on Claude Code UTF-8 stdin. Broad `ZC-05` still fails `SRQ-03` only on the missing literal `对方承许`, which remains the next Madhyamaka/prasaṅga boundary task.

Run a small transcript-backed target review instead of changing prompts immediately:

1. Run the exact `SRQ-02`, `SRQ-03`, and `SRQ-04` prompts in one selected tested route, preferably Codex or Claude Code.
2. Run `ZC-05` once with transcript capture or a redacted answer excerpt that preserves the specific prasaṅga and Agama citation passages.
3. Store compact answer excerpts under `docs/runtime-evidence/`.
4. Re-run `semantic_answer_contract_review.py --answer-file` against those excerpts.
5. Only change agent prompts if the transcript-backed outputs actually miss the contracts.

## Non-Actions

- Do not mark native OpenAI API as `tested`.
- Do not promote Volcengine beyond its current ZC-01 through ZC-03 scope.
- Do not introduce an LLM judge for this review.
- Do not treat keyword-contract checks as doctrinal grading.
- Do not rewrite the prompt before transcript-backed failures identify a concrete wording gap.
