# 2026-06-18 Claude Code Post-Contract Target Review

## Summary

| Field | Value |
|---|---|
| Date | 2026-06-18 |
| Route | Claude Code UTF-8 stdin |
| Tool version | Claude Code 2.1.169 |
| System prompt | `agents/zilan-claude-code.md` |
| Repository base | `af90038` |
| Prompt set | `SRQ-02`, `SRQ-03`, `SRQ-04`, and `ZC-05` target prompts |
| Transcript status | Compact answer excerpts committed; raw Claude JSON outputs kept local only under `C:\tmp\zilan-post-contract-20260618` |
| Platform status effect | None. This is target contract review evidence, not a route promotion or downgrade. |

## Prompt Set

| ID | Prompt |
|---|---|
| `SRQ-02` | `检验论式：声，应是可见，以是色形故。` |
| `SRQ-03` | `若有人承许诸法自性有，如何用应成法指出矛盾？` |
| `SRQ-04` | `查四阿含中关于无我的经文，并说明检索范围与待校勘边界。` |
| `ZC-05` | `请 spawn 一个 zilan agent，用应成论式分析诸法无我，并串联阿含、摄类学、因明和观禅。` |

## Command Shape

```powershell
$OutputEncoding = [System.Text.UTF8Encoding]::new($false)
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)
$sp = Get-Content -Raw -Encoding UTF8 -LiteralPath 'agents\zilan-claude-code.md'
$prompt | claude -p --safe-mode --output-format json --permission-mode bypassPermissions --allowedTools Read,Grep,Glob,Bash,Write --system-prompt "$sp"
```

## Answer Excerpts

| ID | Committed excerpt |
|---|---|
| `SRQ-02` | `docs/runtime-evidence/2026-06-18-claude-code-post-contract-srq-02-answer.md` |
| `SRQ-03` | `docs/runtime-evidence/2026-06-18-claude-code-post-contract-srq-03-answer.md` |
| `SRQ-04` | `docs/runtime-evidence/2026-06-18-claude-code-post-contract-srq-04-answer.md` |
| `ZC-05` | `docs/runtime-evidence/2026-06-18-claude-code-post-contract-zc-05-answer.md` |

## Contract Review Commands

```powershell
python scripts\semantic_answer_contract_review.py --query-id SRQ-02 --answer-file docs\runtime-evidence\2026-06-18-claude-code-post-contract-srq-02-answer.md --json
python scripts\semantic_answer_contract_review.py --query-id SRQ-03 --answer-file docs\runtime-evidence\2026-06-18-claude-code-post-contract-srq-03-answer.md --json
python scripts\semantic_answer_contract_review.py --query-id SRQ-04 --answer-file docs\runtime-evidence\2026-06-18-claude-code-post-contract-srq-04-answer.md --json
python scripts\semantic_answer_contract_review.py --query-id SRQ-03 --answer-file docs\runtime-evidence\2026-06-18-claude-code-post-contract-zc-05-answer.md --json
python scripts\semantic_answer_contract_review.py --query-id SRQ-04 --answer-file docs\runtime-evidence\2026-06-18-claude-code-post-contract-zc-05-answer.md --json
```

## Contract Results

| Answer | Contract | Result | Missing required terms | Present forbidden terms | Review note |
|---|---|---:|---|---|---|
| `SRQ-02` answer | `SRQ-02` Hetuvidya error detection | `pass` | none | none | Correctly identified `因不成`, failed `遍是宗法性`, and the `声` / `色形` mismatch. |
| `SRQ-03` answer | `SRQ-03` Madhyamaka prasaṅga boundary | `pass` | none | none | Preserved the `对方承许` / `归谬` / `自性有` / `缘起` / `矛盾` / `不立自宗` boundary. |
| `SRQ-04` answer | `SRQ-04` Agama citation boundary | `fail` | `context/agama/`, `代表性` | none | Answer included CBETA IDs, search scope, and collation boundaries, but did not include local `context/agama/` anchors or explicit representative-status wording required by the contract. |
| `ZC-05` answer | `SRQ-03` Madhyamaka prasaṅga boundary | `fail` | `对方承许`, `自性有`, `不立自宗` | `断灭` | The `断灭` hit is likely a substring false positive because the answer warns to avoid `断灭见`; however, the missing explicit terms are real contract gaps. |
| `ZC-05` answer | `SRQ-04` Agama citation boundary | `fail` | `CBETA`, `检索范围`, `代表性`, `待校勘` | none | The answer included one local `context/agama/` citation and `T02n0099`, but did not satisfy the full Agama citation-boundary contract. |

## Findings

- The targeted `SRQ-02` and `SRQ-03` prompts pass the current contract checks on Claude Code UTF-8 stdin.
- The targeted `SRQ-04` prompt partially satisfies the intent but fails the machine contract because the answer does not preserve local `context/agama/` anchors or say the citations are representative.
- The broad `ZC-05` answer remains too broad to satisfy the narrow `SRQ-03` and `SRQ-04` answer contracts without stronger prompt or output-contract guidance.
- The `断灭` forbidden-term hit on `ZC-05` should be treated carefully: the answer says to avoid falling into `断灭见`, not that Zilan endorses annihilationism. This exposes a future improvement for the keyword-only reviewer, but does not erase the missing required terms.

## Limitations

- This review validates target-contract behavior only on the local Claude Code UTF-8 stdin route.
- It does not change Claude Code's existing platform status, and it does not validate native OpenAI API.
- `semantic_answer_contract_review.py` is a minimum keyword contract, not doctrinal grading.
- Raw JSON outputs are not committed to avoid storing large runtime payloads; committed answer excerpts preserve the reviewed answer text.
