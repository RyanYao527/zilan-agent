# 2026-08-19 SRQ-11 Definition Prompt Hardening Local Replay

## Scope

This note records local prompt-invariant evidence for the `SRQ-11` Collected Topics definition-boundary prompt
hardening.

No provider call, live runtime rerun, answer excerpt rewrite, answer-contract change, fuzzy matching, semantic grading,
or platform-status update was performed.

## Prompt Change

The Codex, Claude Code, and OpenAI metadata prompt surfaces now require direct definition-boundary answers to preserve
these literal slots:

- `性相过宽`
- `唯在所表上成立`
- `违②`
- `definiendum_boundary`

The prompt wording targets questions such as `瓶的性相是能盛水者。这个定义成立吗？` and related 性相/所表 definition
checks. It asks the answer to include `名相/所表拆解` and to avoid only saying `定义过宽` or `周遍不成立` while omitting
the literal slots.

## Local Check

```powershell
python -m pytest tests\test_validate_zilan_repo.py::test_agent_prompt_validator_requires_srq11_definition_boundary_slots tests\test_validate_zilan_repo.py::test_openai_metadata_requires_srq11_definition_boundary_slots -q
```

Result: `2 passed`.

## Boundaries

- The already committed 2026-08-19 `SRQ-11` Claude Code answer excerpt remains fail evidence under the current
  answer contract.
- This note is prompt-prepared evidence only; `SRQ-11` runtime rerun is pending.
- `docs/platform-validation.md` remains unchanged.
