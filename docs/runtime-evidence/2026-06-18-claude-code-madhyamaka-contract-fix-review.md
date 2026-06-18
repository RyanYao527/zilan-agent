# 2026-06-18 Claude Code Madhyamaka Contract Fix Review

## Summary

| Field | Value |
|---|---|
| Date | 2026-06-18 |
| Route | Claude Code UTF-8 stdin |
| Tool version | Claude Code 2.1.169 |
| System prompt | `agents/zilan-claude-code.md` |
| Repository base | `4970810` plus this branch's Madhyamaka prasaṅga output-contract changes |
| Prompt set | One broad `ZC-05` cross-domain prompt |
| Transcript status | Compact answer excerpt committed; raw Claude JSON output kept local only under `C:\tmp\zilan-madhyamaka-contract-20260618` |
| Platform status effect | None. This is target contract review evidence, not a route promotion or downgrade. |

## Prompt Set

| ID | Prompt |
|---|---|
| `ZC-05` | `请 spawn 一个 zilan agent，用应成论式分析诸法无我，并串联阿含、摄类学、因明和观禅。` |

## Contract Changes Under Review

- Agent prompts now define an explicit `中观应成输出契约`.
- Madhyamaka prasaṅga answers must distinguish `对方承许` from Zilan's own conclusion boundary.
- Broad cross-domain answers involving no-self, emptiness, dependent arising, or prasaṅga must preserve `自性有`, `归谬`, `缘起`, `矛盾`, and `不立自宗` in the relevant Madhyamaka section.
- Boundary language should avoid presenting emptiness as absolute nonexistence and should say the prasaṅga only shows the `自性有` premise cannot stand.

## Answer Excerpt

| ID | Committed excerpt |
|---|---|
| `ZC-05` | `docs/runtime-evidence/2026-06-18-claude-code-madhyamaka-contract-fix-zc-05-answer.md` |

## Contract Review Commands

```powershell
python scripts\semantic_answer_contract_review.py --query-id SRQ-03 --answer-file docs\runtime-evidence\2026-06-18-claude-code-madhyamaka-contract-fix-zc-05-answer.md --json
python scripts\semantic_answer_contract_review.py --query-id SRQ-04 --answer-file docs\runtime-evidence\2026-06-18-claude-code-madhyamaka-contract-fix-zc-05-answer.md --json
```

## Contract Results

| Answer | Contract | Result | Missing required terms | Present forbidden terms | Review note |
|---|---|---:|---|---|---|
| `ZC-05` answer | `SRQ-03` Madhyamaka prasaṅga boundary | `pass` | none | none | Broad answer now preserves `对方承许`, `归谬`, `自性有`, `缘起`, `矛盾`, and `不立自宗`. |
| `ZC-05` answer | `SRQ-04` Agama citation boundary | `pass` | none | none | The prior Agama evidence output contract remains intact in the broad answer. |

## Findings

- The broad `ZC-05` prompt now passes the current `SRQ-03` Madhyamaka prasaṅga-boundary contract on Claude Code UTF-8 stdin.
- The same broad answer still passes `SRQ-04`, so the Madhyamaka prompt hardening did not regress the Agama citation-boundary terms.
- This closes the residual `对方承许` gap recorded in the Agama contract fix review.

## Limitations

- This review validates the local Claude Code UTF-8 stdin route only.
- This is not a full ZC-01 through ZC-06 rerun and does not change platform status.
- `semantic_answer_contract_review.py` is a minimum keyword contract, not doctrinal grading.
- Native OpenAI API remains `harness-ready`; this evidence does not validate it.
