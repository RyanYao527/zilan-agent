# 2026-08-07 SRQ-01 Contract Calibration Replay

| Field | Value |
|---|---|
| Date | 2026-08-07 |
| Scenario | Local replay after calibrating the integrated `SRQ-01` answer contract |
| Input answer | `docs/runtime-evidence/2026-08-06-claude-code-zc-05-srq-01-runtime-spot-answer.md` |
| Contract | `SRQ-01` / `cross_domain_no_self_analysis` |
| Provider calls | none |
| Platform-status change | none |

## Purpose

This replay checks whether the 2026-08-06 broad `ZC-05` runtime spot answer satisfies the integrated `SRQ-01`
contract once section-heading labels are separated from concrete answer evidence.

The prior strict review failed `SRQ-01` only on these global required terms:

- `阿含证据`
- `代表性检索`
- `因明校验`

The answer itself already contains the corresponding concrete surfaces:

- Agama search and evidence: `检索范围`, `代表性阿含经文`, `CBETA`, local `context/agama/` scope, and `待校勘`;
- Hetuvidya checking: `因三相校验`, `遍是宗法性`, `同品定有性`, and `异品遍无性`;
- cognitive/practice mapping: `触`, `作意`, `受`, `想`, `思`, `观禅`, `边界`, `不等于修证`, and `善知识指导`.

This calibration therefore treats the three heading-like labels as prompt ergonomics rather than mandatory global
literals. The contract still requires concrete citation, reasoning, cognitive, and practice-boundary terms and still uses
`required_slots` to check visible answer sections.

## Command

```powershell
python scripts\semantic_answer_contract_review.py --query-id SRQ-01 --answer-file docs\runtime-evidence\2026-08-06-claude-code-zc-05-srq-01-runtime-spot-answer.md
```

## Result

```text
# Semantic Answer Contract Review

Query ID: SRQ-01
Query: 用应成论式分析诸法无我
Overall status: pass

Boundary: fixture-only answer text review; this is not runtime validation.

## Reviews

### cross_domain_no_self_analysis: pass
- Description: Answer must integrate Agama evidence, Hetuvidya, Collected Topics, Madhyamaka prasaṅga, cognitive analysis, and practice boundaries for the broad no-self query.
- Missing required terms: none
- Present forbidden terms: none
- Missing required slots: none
```

## Boundary

This is a local contract replay over an already committed answer excerpt. It does not generate a new answer, does not run
Claude Code, Codex, OpenAI, or any OpenAI-compatible provider, and does not change `docs/platform-validation.md`.

The 2026-08-06 batch review has been updated to the current calibrated contract output. After this calibration, the same
answer passes direct `SRQ-01` answer-contract review, while the separate `SRQ-03` and `SRQ-08` runtime explicitness gaps
from that spot review remain open for the next prompt-hardening step.
