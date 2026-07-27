# Contributing to Zilan Agent

Thank you for your interest in contributing to Zilan Agent.

This project follows the [Contributor Covenant](CODE_OF_CONDUCT.md). Please follow it when participating in discussions, opening issues, or submitting pull requests.

## 🪜 Contributor Ladder

You don't need to be a Buddhist scholar or a senior engineer to help. Below are four progressive tiers of participation, each with clear **skill requirements**, **time commitment**, and a **concrete first task**. Start at Level 1 and work your way up.

### Level 1: Evidence Runner

> **What**: Run ZC regression cases on Claude Code / Codex / new providers and submit runtime evidence.
> **Skills needed**: Command-line basics
> **Time**: ~30 minutes per run
> **Does NOT require**: Python, Buddhist knowledge, or code changes

**🎯 First task: Run a Claude Code regression validation**

1. Load `agents/zilan-claude-code.md` as an agent in Claude Code
2. Send the ZC-01 through ZC-06 prompts from `tests/regression_cases.yaml`
3. Save responses (redact personal info) to `docs/runtime-evidence/`
4. Submit a PR — use existing files in `docs/runtime-evidence/` as a template

**If you hit issues**: Open an Issue with the `[Evidence]` prefix and paste the error.

---

### Level 2: Documentation Reviewer

> **What**: Review Chinese / English translation consistency, Agama citation accuracy, and CBETA ID correctness.
> **Skills needed**: Bilingual reading (Chinese + English) + basic Buddhist terminology
> **Time**: 1-2 hours per review
> **Does NOT require**: Python or CI/CD knowledge

**🎯 First task: Cross-check terminology between SKILL.md and SKILL-en.md**

1. Open `SKILL.md` and `SKILL-en.md`
2. Compare the "output contract" sections (search for `输出契约` / `output contract`)
3. Check whether key terms are translated consistently (e.g. `待校勘`, `因三相`, `应成论式`)
4. Document inconsistencies — open an Issue with the `[Docs]` prefix

**Common contribution areas**:

- CBETA IDs and scroll numbers in Agama citations
- README paths vs actual file locations
- Ambiguity in concept definitions under `context/`

---

### Level 3: Contract Reviewer

> **What**: Review reasoning-contract fixtures for correctness; audit answer-contract pass/fail samples.
> **Skills needed**: Foundational knowledge in at least one of: Hetuvidya, Collected Topics, Madhyamaka, or Cognitive Analysis
> **Time**: 2-4 hours per review
> **Does NOT require**: Python coding (but YAML literacy helps)

**🎯 First task: Audit an answer-contract sample**

1. Read `tests/reasoning_cases.yaml` and pick a domain you know (e.g. ZR-01 Hetuvidya or ZR-03 Madhyamaka)
2. Find the corresponding pass/fail samples: `tests/fixtures/answers/srq*-pass.md` and `srq*-fail.md`
3. Evaluate: Does the fail sample genuinely demonstrate a contract violation? Does the pass sample have edge cases that slip through?
4. Open an Issue with the `[Contract]` prefix and your analysis

**Common contribution areas**:

- Proposing new reasoning cases (new ZR entries)
- Improving boundary_statement definitions in existing fixtures
- Discussing whether a forbidden term is too strict or too loose

---

### Level 4: Code Contributor

> **What**: Implement new provider harnesses, extend validators, improve zilanlib architecture.
> **Skills needed**: Python + pytest
> **Time**: Ongoing participation
> **Recommendation**: Complete at least one item from Levels 1-3 before writing code, so you're familiar with the project structure.

**🎯 First task: Add a harness for a new provider**

1. Read `scripts/zilanlib/reasoning/hetuvidya_validator.py` to understand the validator pattern
2. If you have API access to a provider (e.g. DeepSeek, GLM, Qwen, or a new Claude Code release), write a harness following the pattern in `scripts/openai_api_harness.py`
3. Run ZC-01 through ZC-03 regression cases
4. Submit a PR with the harness script + redacted runtime evidence

**Common contribution areas**:

- Extending validators in `zilanlib/reasoning/`
- Improving search performance in `scripts/search_agama.py`
- CI pipeline improvements
- zilanlib architecture refactoring

---

## How to Contribute

### Option 1: Submit an Issue

- Found a bug or have a suggestion? Open a GitHub Issue.
- Please provide a clear description.

### Option 2: Fork & Pull Request

1. Fork this repository
2. Create your branch (`git checkout -b feature/your-feature-name`)
3. Commit your changes (`git commit -m 'Add some feature'`)
4. Push (`git push origin feature/your-feature-name`)
5. Submit a Pull Request

### Commit Guidelines

- Use Chinese or English — keep messages concise
- When modifying core definitions, update `SKILL.md`, relevant `context/` files, `CHANGELOG.md`, and required validation documents
- For significant changes, please open an Issue for discussion first

## Local Validation

After changing `SKILL.md`, `agents/`, `context/`, the Agama corpus, or scripts, run at least:

```bash
python scripts/validate_zilan_repo.py --check-generated
python -m pytest
python scripts/search_agama.py --terms "無我|非我|緣起" --limit 10
```

`validate_zilan_repo.py` checks required files, the Codex regression matrix, key Agent prompt fragments, Agama search smoke tests, and optionally verifies that Markdown generated from CBETA XML is stable.

## Becoming a Co-Maintainer

A co-maintainer role is not just a title; it means taking sustained responsibility for a reviewable area of work. The most useful areas right now are:

- Documentation review and Chinese / English consistency checks
- Runtime validation for Claude Code, Codex, OpenAI API, or OpenAI-compatible providers
- Scholarly collation of Agama citations against CBETA XML sources and boundary notes
- Review of reasoning-contract fixtures, answer-contract samples, and runtime evidence

If you would like to become a regular collaborator, please open an issue first and describe the scope you want to help with, your expected cadence, and the validation environment you can run. Changes that affect platform status, output contracts, Agama corpus files, or core prompts should still go through small PRs, full repository checks, and explicit evidence records.

## Knowledge Co-Building

This skill is a living learning system. Core knowledge is maintained in:

- `SKILL.md` — Main definition file
- `context/摄类学工具箱.md` — Conceptual analysis & logical reasoning toolkit
- `context/因明推理引擎.md` — Buddhist logic engine
- `CHANGELOG.md` — User-visible release notes
- `docs/runtime-validation-log.md` — Manual runtime validation records

Contributions via PR are welcome.

---

*诸行无常，诸法无我，涅槃寂静。*
