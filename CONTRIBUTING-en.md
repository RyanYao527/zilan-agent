# Contributing to Zilan Agent

Thank you for your interest in contributing to Zilan Agent.

This project follows the [Contributor Covenant](CODE_OF_CONDUCT.md). Please follow it when participating in discussions, opening issues, or submitting pull requests.

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
