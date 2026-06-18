# 2026-06-18 Claude Code Agama Contract Fix Review

## Summary

| Field | Value |
|---|---|
| Date | 2026-06-18 |
| Route | Claude Code UTF-8 stdin |
| Tool version | Claude Code 2.1.169 |
| System prompt | `agents/zilan-claude-code.md` |
| Repository base | `5d1de60` plus this branch's Agama evidence output-contract changes |
| Prompt set | `SRQ-04` and one broad `ZC-05` cross-domain prompt |
| Transcript status | Compact answer excerpts committed; raw Claude JSON outputs kept local only under `C:\tmp\zilan-agama-contract-20260618*` |
| Platform status effect | None. This is target contract review evidence, not a route promotion or downgrade. |

## Prompt Set

| ID | Prompt |
|---|---|
| `SRQ-04` | `查四阿含中关于无我的经文，并说明检索范围与待校勘边界。` |
| `ZC-05` | `请 spawn 一个 zilan agent，用应成论式分析诸法无我，并串联阿含、摄类学、因明和观禅。` |

## Contract Changes Under Review

- Agent prompts now define an explicit `阿含证据输出契约`.
- Agama evidence answers must state `检索范围`, provide CBETA IDs and local `context/agama/...` anchors, mark excerpts as `代表性`, and preserve `待校勘` boundaries.
- No-self / non-self answers must include a representative `《雜阿含經》(T02n0099)` citation when locally available.
- Non-file-output tasks must not use `Write` as the main delivery path; the main response must carry the core answer.
- `校勘完成` and `校勘确认` are now forbidden terms in the `SRQ-04` answer contract, alongside `已穷尽`, `无需校勘`, and `可作为定本`.

## Answer Excerpts

| ID | Committed excerpt |
|---|---|
| `SRQ-04` | `docs/runtime-evidence/2026-06-18-claude-code-agama-contract-fix-srq-04-answer.md` |
| `ZC-05` | `docs/runtime-evidence/2026-06-18-claude-code-agama-contract-fix-zc-05-answer.md` |

## Contract Review Commands

```powershell
python scripts\semantic_answer_contract_review.py --query-id SRQ-04 --answer-file docs\runtime-evidence\2026-06-18-claude-code-agama-contract-fix-srq-04-answer.md --json
python scripts\semantic_answer_contract_review.py --query-id SRQ-04 --answer-file docs\runtime-evidence\2026-06-18-claude-code-agama-contract-fix-zc-05-answer.md --json
python scripts\semantic_answer_contract_review.py --query-id SRQ-03 --answer-file docs\runtime-evidence\2026-06-18-claude-code-agama-contract-fix-zc-05-answer.md --json
```

## Contract Results

| Answer | Contract | Result | Missing required terms | Present forbidden terms | Review note |
|---|---|---:|---|---|---|
| `SRQ-04` answer | `SRQ-04` Agama citation boundary | `pass` | none | none | Direct no-self Agama search answer now includes search scope, representative status, `T02n0099`, local `context/agama/` anchors, and `待校勘` boundary language. |
| `ZC-05` answer | `SRQ-04` Agama citation boundary | `pass` | none | none | Broad cross-domain answer now carries Agama evidence in the main response instead of only writing a separate file. |
| `ZC-05` answer | `SRQ-03` Madhyamaka prasaṅga boundary | `fail` | `对方承许` | none | Expected residual gap for the next narrow PR; this branch only fixes the Agama citation boundary. |

## Findings

- The direct `SRQ-04` prompt now passes the current Agama citation-boundary contract on Claude Code UTF-8 stdin.
- The broad `ZC-05` prompt now passes `SRQ-04` in the main answer, including `CBETA`, `T02n0099`, local `context/agama/` anchors, `检索范围`, `代表性`, and `待校勘`.
- An intermediate `ZC-05` run wrote a file and returned only a summary, so this branch adds a no-file-output guard: unless the user asks for file output, the main response must contain the answer.
- `ZC-05` still fails `SRQ-03` because the broad answer omits the literal `对方承许` boundary term. That is a separate Madhyamaka/prasaṅga prompt-contract issue.

## Limitations

- This review validates the local Claude Code UTF-8 stdin route only.
- This is not a full ZC-01 through ZC-06 rerun and does not change platform status.
- `semantic_answer_contract_review.py` is a minimum keyword contract, not doctrinal grading.
- Native OpenAI API remains `harness-ready`; this evidence does not validate it.
