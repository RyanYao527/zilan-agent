# 2026-08-06 ZC-05 / SRQ-01 Prompt Hardening Local Evidence

## Scope

This note records local evidence for the broad `ZC-05` prompt hardening that prepares agent prompts for the integrated
`SRQ-01` answer contract. It does not run Claude Code, Codex, OpenAI, or any OpenAI-compatible provider, and it does not
generate a new model answer.

The hardening adds explicit prompt slots for broad `ZC-05` answers that analyze `诸法无我` across Agama evidence,
Collected Topics, Hetuvidya, Madhyamaka, and vipassanā:

- `阿含证据`
- `代表性检索`
- `因明校验`
- `我所`
- `触`
- `作意`
- `受`
- `想`
- `思`
- `不等于修证`

## Commands

```powershell
python -m pytest tests\test_validate_zilan_repo.py::test_agent_prompt_validator_requires_broad_zc05_srq01_integrated_slots -q
python scripts\validate_zilan_repo.py --check-generated --strict-yaml
python scripts\reasoning_answer_review_batch.py --batch docs\runtime-evidence\2026-08-06-srq-01-zc-05-integrated-contract-replay-batch.yaml
```

## Output

```text
tests\test_validate_zilan_repo.py::test_agent_prompt_validator_requires_broad_zc05_srq01_integrated_slots passed.

zilan-agent validation passed.

# Reasoning Answer Review Batch

Batch: docs/runtime-evidence/2026-08-06-srq-01-zc-05-integrated-contract-replay-batch.yaml
Overall status: fail
Summary: pass=0, fail=1, review_needed=0, other=0

Boundary: batch fixture review only; this is not runtime platform validation.

## Reviews
- 2026-07-14-zc-05-broad-postfix-srq-01-integrated-replay: fail (SRQ-01)
  missing: cross_domain_no_self_analysis:阿含证据, cross_domain_no_self_analysis:代表性检索, cross_domain_no_self_analysis:因明校验, cross_domain_no_self_analysis:我所, cross_domain_no_self_analysis:触, cross_domain_no_self_analysis:作意, cross_domain_no_self_analysis:想, cross_domain_no_self_analysis:思, cross_domain_no_self_analysis:不等于修证
```

## Findings

The local prompt invariant now requires the integrated `SRQ-01` slots in both `agents/zilan-codex.md` and
`agents/zilan-claude-code.md`. The portable OpenAI metadata and public Skill surfaces were updated to carry the same
contract language.

The existing 2026-07-14 broad `ZC-05` answer excerpt still fails the integrated `SRQ-01` contract, as expected. This PR
therefore records `prompt prepared, runtime pending`: a future runtime spot rerun must produce a new standalone answer
excerpt before any broad `ZC-05` answer can be recorded as passing `SRQ-01`.

The replay output above lists only missing terms. The older excerpt already contains `受`, so `受` is part of the new
prompt invariant but is not shown as missing in that historical replay.

## Boundary

This is local prompt and evidence maintenance only. It does not change `docs/platform-validation.md`, does not promote
any route to `tested`, and does not alter the prior `SRQ-03`, `SRQ-04`, or `SRQ-08` pass evidence for the older broad
`ZC-05` excerpt.
