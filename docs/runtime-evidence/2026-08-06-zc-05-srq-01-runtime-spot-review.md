# 2026-08-06 ZC-05 / SRQ-01 Runtime Spot Review

| Field | Value |
|---|---|
| Date | 2026-08-06 |
| Scenario | Broad `ZC-05` runtime spot rerun after integrated `SRQ-01` prompt hardening |
| Route / provider | Claude Code UTF-8 stdin |
| Tool version | Claude Code 2.1.220 |
| System prompt | `agents/zilan-claude-code.md` from branch-local minimum-template hardening |
| Repository base | `9ef4a76` (`Harden broad ZC-05 SRQ-01 prompt slots`) plus this branch's prompt / fixture cleanup |
| Branch | `codex/zc05-srq01-runtime-spot` |
| Source location | Raw Claude JSON and extracted answer Markdown kept local only under `C:\tmp\zilan-zc05-srq01-runtime-spot-20260806` |
| Redaction note | No secrets are included here. Raw JSON, session metadata, token/cost details, and full unredacted local paths are not committed. |
| Standalone answer excerpt | `docs/runtime-evidence/2026-08-06-claude-code-zc-05-srq-01-runtime-spot-answer.md` |
| Runtime log entry | `docs/runtime-validation-log.md#2026-08-06-claude-code-zc-05--srq-01-runtime-spot-review` |

## Commands Or Prompts

Command shape:

```powershell
$OutputEncoding = [System.Text.UTF8Encoding]::new($false)
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)
[Console]::InputEncoding = [System.Text.UTF8Encoding]::new($false)
$sys = Get-Content -Raw -Encoding UTF8 -LiteralPath 'agents\zilan-claude-code.md'
$prompt = '请 spawn 一个 zilan agent，用应成论式分析诸法无我，并串联阿含、摄类学、因明和观禅。'
$prompt | claude -p --output-format json --system-prompt $sys --add-dir . --dangerously-skip-permissions
```

Batch review command:

```powershell
python scripts\reasoning_answer_review_batch.py --batch docs\runtime-evidence\2026-08-06-zc-05-srq-01-runtime-spot-review-batch.yaml
```

## Runtime Result

| Attempt | Local answer file | Claude subtype | Turns | Answer chars | Contract result | Notes |
|---|---|---:|---:|---:|---|---|
| Initial post-#182 run | `ZC-05.answer.md` | `success` | 1 | 1686 | partial / fail | `SRQ-03` and `SRQ-08` passed; `SRQ-01` and `SRQ-04` failed. The run also exposed a shallow `SRQ-01` forbidden-term collision with negated nihilism-boundary wording. |
| Literal-label prompt rerun | `ZC-05.post-tightening.answer.md` | `success` | 1 | 1107 | fail | Failed all four reviewed contracts because the answer summarized labels and omitted required literal slots. |
| Minimum-template rerun | `ZC-05.minimum-template.answer.md` | `success` | 1 | 1372 | partial / fail | Committed as the standalone answer excerpt. `SRQ-04` passed, but `SRQ-01`, `SRQ-03`, and `SRQ-08` still failed strict answer-contract review. |

The minimum-template rerun also wrote an unrequested local report file in the workspace root. That untracked generated
file was removed before this PR because `ZC-05` did not request file output and this branch is limited to prompt,
contract, and evidence maintenance.

## Contract Results

```text
# Reasoning Answer Review Batch

Batch: docs/runtime-evidence/2026-08-06-zc-05-srq-01-runtime-spot-review-batch.yaml
Overall status: fail
Summary: pass=1, fail=3, review_needed=0, other=0

Boundary: batch fixture review only; this is not runtime platform validation.

## Reviews
- 2026-08-06-zc-05-runtime-spot-srq-01-integrated: fail (SRQ-01)
  missing: cross_domain_no_self_analysis:阿含证据, cross_domain_no_self_analysis:代表性检索, cross_domain_no_self_analysis:因明校验
- 2026-08-06-zc-05-runtime-spot-srq-03-prasanga: fail (SRQ-03)
  missing: madhyamaka_prasanga_boundary:不立自宗
- 2026-08-06-zc-05-runtime-spot-srq-04-agama: pass (SRQ-04)
- 2026-08-06-zc-05-runtime-spot-srq-08-nihilism: fail (SRQ-08)
  missing: madhyamaka_nihilism_boundary:二谛, madhyamaka_nihilism_boundary:proposition_decomposition

## Limitations
- Batch review only orchestrates local fixture answer reviews; it does not call providers or generate answers.
- Each batch item uses the same shallow answer-contract and structured-validator limitations as a single review.
- Batch status is a review convenience signal, not platform validation or doctrinal grading.
```

## Findings

- The `SRQ-01` fixture now avoids the shallow false positive where a negated boundary sentence containing
  `因果不存在` could fail the integrated no-self contract.
- Prompt hardening improved the final broad `ZC-05` answer enough for `SRQ-04` Agama citation-boundary review to pass.
- The runtime route still does not reliably preserve the integrated `SRQ-01` literal labels or the prior `SRQ-03` /
  `SRQ-08` literal boundary slots in the same broad answer.
- The final answer includes `context/agama/` in the search-scope sentence, but its representative citation bullets use
  shortened file anchors such as `T0099-za-agama.md:147` rather than full `context/agama/...` anchors. This remains a
  runtime explicitness gap even though the shallow `SRQ-04` contract passes.
- Current status for broad `ZC-05` integrated `SRQ-01`: runtime pending / strict replay fail.

## Boundary

This is a targeted runtime spot review, not a full `ZC-01` through `ZC-06` rerun. It does not change
`docs/platform-validation.md`, does not promote or demote any platform route, does not validate native OpenAI API, and
does not grade doctrinal correctness or publication-level Agama collation.
