# 2026-08-07 ZC-05 / SRQ-03 SRQ-08 Local Replay Evidence

## Scope

This note records the P1-C local replay evidence after the broad `ZC-05` second-round prompt hardening for `SRQ-03`
and `SRQ-08`. It uses only committed answer excerpts and checked-in fixture samples. It does not run Claude Code, Codex,
OpenAI, or any OpenAI-compatible provider, and it does not generate a new model answer.

This replay asks whether the local answer contracts and prompt invariants can distinguish:

- a committed broad `ZC-05` excerpt that still misses the target slots;
- a committed broad `ZC-05` excerpt that already contains the target slots;
- checked-in pass/fail fixture samples for the same `SRQ-03` and `SRQ-08` contracts.

## Commands

```powershell
python -m pytest tests\test_validate_zilan_repo.py::test_agent_prompt_validator_requires_broad_zc05_prasanga_nihilism_slots tests\test_validate_zilan_repo.py::test_broad_zc05_recommended_structure_keeps_prasanga_nihilism_slots tests\test_openai_api_harness.py::test_openai_harness_default_prompt_preserves_broad_zc05_prasanga_nihilism_slots -q
python scripts\reasoning_answer_review_batch.py --batch docs\runtime-evidence\2026-08-06-zc-05-srq-01-runtime-spot-review-batch.yaml --json
python scripts\reasoning_answer_review_batch.py --batch docs\runtime-evidence\2026-07-20-latest-zc-answer-excerpt-review-batch.yaml --json
python scripts\semantic_answer_contract_review.py --query-id SRQ-03 --sample-id srq03-madhyamaka-prasanga-pass
python scripts\semantic_answer_contract_review.py --query-id SRQ-03 --sample-id srq03-madhyamaka-prasanga-fail
python scripts\semantic_answer_contract_review.py --query-id SRQ-08 --sample-id srq08-madhyamaka-nihilism-boundary-pass
python scripts\semantic_answer_contract_review.py --query-id SRQ-08 --sample-id srq08-madhyamaka-nihilism-boundary-fail
```

## Results

| Check | Input | Result | Target finding |
|---|---|---:|---|
| Prompt invariant tests | Codex / Claude Code prompts plus OpenAI harness default prompt | pass | `3 passed`; prompt surfaces require `SRQ-03`, `SRQ-08`, `不立自宗`, `二谛`, and `proposition_decomposition`. |
| Current broad `ZC-05` runtime spot replay | `2026-08-06-zc-05-srq-01-runtime-spot-review-batch.yaml` | fail expected | `pass=2, fail=2`; `SRQ-03` misses `madhyamaka_prasanga_boundary:不立自宗`; `SRQ-08` misses `madhyamaka_nihilism_boundary:二谛` and `madhyamaka_nihilism_boundary:proposition_decomposition`. |
| Earlier broad `ZC-05` committed excerpt replay | `2026-07-20-latest-zc-answer-excerpt-review-batch.yaml` | pass | `pass=5, fail=0`; the 2026-07-14 broad `ZC-05` excerpt still passes `SRQ-03` and `SRQ-08`, showing the contracts can pass when the slots are present. |
| `SRQ-03` pass sample | `srq03-madhyamaka-prasanga-pass` | pass | Missing required terms: none; missing required slots: none. |
| `SRQ-03` fail sample | `srq03-madhyamaka-prasanga-fail` | fail expected | Missing required terms include `不立自宗`; missing slots include `opponent_premise`, `prasanga_move`, `contradiction`, and `thesis_boundary`. |
| `SRQ-08` pass sample | `srq08-madhyamaka-nihilism-boundary-pass` | pass | Missing required terms: none; missing required slots: none. |
| `SRQ-08` fail sample | `srq08-madhyamaka-nihilism-boundary-fail` | fail expected | Missing required slot includes `proposition_decomposition`; forbidden terms include `无需二谛`. |

## Interpretation

The local replay proves the target gap is mechanically visible:

- the 2026-08-06 broad `ZC-05` runtime spot answer is not being promoted; it still fails the strict `SRQ-03` and
  `SRQ-08` reviews;
- the same contracts pass for an earlier committed broad `ZC-05` excerpt and for checked-in pass samples, so the current
  failure is not a broken-contract false negative;
- the checked-in fail samples still fail with the intended missing terms, forbidden terms, and missing slots;
- the prompt invariant tests now protect the prompt surfaces that should prepare the next runtime attempt.

Status: `prompt prepared, runtime pending`. A future runtime spot rerun must capture a new standalone answer excerpt
before broad `ZC-05` can be recorded as passing the combined `SRQ-01`, `SRQ-03`, `SRQ-04`, and `SRQ-08` review batch.

## Boundary

This is local replay evidence only. It does not change `docs/platform-validation.md`, does not promote any route to
`tested`, does not call providers, and does not grade Buddhist doctrine.
