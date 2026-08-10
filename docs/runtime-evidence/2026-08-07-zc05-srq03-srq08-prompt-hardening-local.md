# 2026-08-07 ZC-05 / SRQ-03 SRQ-08 Prompt Hardening Local Evidence

## Scope

This note records local evidence for the second-round broad `ZC-05` prompt hardening. It does not run Claude Code,
Codex, OpenAI, or any OpenAI-compatible provider, and it does not generate a new model answer.

The hardening prepares broad `ZC-05` answers to keep the remaining strict answer-contract slots that were missing from
the 2026-08-06 runtime spot excerpt:

- `SRQ-03`: `不立自宗`
- `SRQ-08`: `二谛`
- `SRQ-08`: `proposition_decomposition`

## Changed Surfaces

- `agents/zilan-codex.md`
- `agents/zilan-claude-code.md`
- `SKILL.md`
- `SKILL-en.md`
- `agents/openai.yaml`
- `scripts/zilanlib/validation/agent_prompts.py`
- `tests/test_validate_zilan_repo.py`
- `tests/test_openai_api_harness.py`
- `docs/runtime-evidence/index.md`
- `CHANGELOG.md`

## Commands

```powershell
python -m pytest tests\test_validate_zilan_repo.py::test_agent_prompt_validator_requires_broad_zc05_prasanga_nihilism_slots tests\test_validate_zilan_repo.py::test_broad_zc05_recommended_structure_keeps_prasanga_nihilism_slots tests\test_openai_api_harness.py::test_openai_harness_default_prompt_preserves_broad_zc05_prasanga_nihilism_slots -q
python scripts\validate_zilan_repo.py --check-generated --strict-yaml
python scripts\reasoning_answer_review_batch.py --batch docs\runtime-evidence\2026-08-06-zc-05-srq-01-runtime-spot-review-batch.yaml
```

## Output

```text
3 passed.

zilan-agent validation passed.

# Reasoning Answer Review Batch

Batch: docs/runtime-evidence/2026-08-06-zc-05-srq-01-runtime-spot-review-batch.yaml
Overall status: fail
Summary: pass=2, fail=2, review_needed=0, other=0

Boundary: batch fixture review only; this is not runtime platform validation.

## Reviews
- 2026-08-06-zc-05-runtime-spot-srq-01-integrated: pass (SRQ-01)
- 2026-08-06-zc-05-runtime-spot-srq-03-prasanga: fail (SRQ-03)
  missing: madhyamaka_prasanga_boundary:不立自宗
- 2026-08-06-zc-05-runtime-spot-srq-04-agama: pass (SRQ-04)
- 2026-08-06-zc-05-runtime-spot-srq-08-nihilism: fail (SRQ-08)
  missing: madhyamaka_nihilism_boundary:二谛, madhyamaka_nihilism_boundary:proposition_decomposition
```

## Findings

The local prompt invariant now requires broad `ZC-05` agent prompts to preserve `SRQ-03`, `SRQ-08`, `不立自宗`,
`二谛`, and `proposition_decomposition`. The Codex, Claude Code, public Skill, and OpenAI metadata surfaces carry the
same second-round hardening language in the broad `ZC-05` minimum template. The OpenAI API harness default prompt
surface also preserves the same slots through `interface.default_prompt`.

The existing 2026-08-06 broad `ZC-05` runtime excerpt still fails the strict `SRQ-03` and `SRQ-08` reviews. This PR
therefore records `prompt prepared, runtime pending`: a future runtime spot rerun must produce a new standalone answer
excerpt before broad `ZC-05` can be recorded as passing the full `SRQ-01`, `SRQ-03`, `SRQ-04`, and `SRQ-08` batch.

## Boundary

This is local prompt and evidence maintenance only. It does not change `docs/platform-validation.md`, does not promote
any route to `tested`, and does not call providers.
