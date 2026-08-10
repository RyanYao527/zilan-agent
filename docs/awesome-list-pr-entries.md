# Awesome-List PR Entries for zilan-agent

Pre-written entries for submitting zilan-agent to curated awesome lists.
Each section contains the exact text to paste into a PR.

---

## 1. `travisvn/awesome-claude-skills` (~14k ⭐)

**URL**: <https://github.com/travisvn/awesome-claude-skills>
**Section**: Claude Code Skills (or create one if it doesn't exist)
**Format**: Link + one-line description

**PR entry:**

```markdown
- **[zilan-agent](https://github.com/RyanYao527/zilan-agent)** - Buddhist philosophy Agent/Skill dual-track framework with 5 deterministic output-contract validators, 277 CI-guarded tests, and an 87K-line Āgama search corpus. Dual-language (Chinese/English).
```

**PR description:**

```markdown
Add zilan-agent, a Buddhist philosophy Claude Code Skill + Agent with:

- Dual-track architecture: lightweight Skill for dialogue, deep Agent for research
- Five deterministic output-contract validators (no LLM-as-judge)
- 277 tests, 84% coverage, mypy + ruff clean
- Built-in Āgama (Buddhist scripture) search with CBETA citation anchors
- Full Chinese + English documentation

Install: copy `zilan-agent` to `~/.claude/skills/`
Agent: copy `agents/zilan-claude-code.md` to `~/.claude/agents/zilan.md`
```

---

## 2. `promptslab/Awesome-Prompt-Engineering` (~6k ⭐)

**URL**: <https://github.com/promptslab/Awesome-Prompt-Engineering>
**Section**: "Tools & Frameworks" or "Prompt Testing & Evaluation"

**PR entry:**

```markdown
- **[zilan-agent](https://github.com/RyanYao527/zilan-agent)** — Open-source demo of the *Output Contract* pattern: structured specs (required slots, forbidden terms, boundary statements) + deterministic validators that check LLM outputs at CI speed without model calls. 277 tests, Python, MIT license.
```

**PR description:**

```markdown
Add zilan-agent as a reference implementation of the Output Contract pattern for LLM reliability.

Notable for prompt engineers:
- Defines 5 contract families (Hetuvidya logic, Collected Topics, Madhyamaka, Cognitive Analysis, Agama evidence)
- Each contract specifies required terms, forbidden phrases, and boundary statements
- Deterministic validators (pure Python, zero model calls) verify contract compliance
- Answer-contract review with checked-in pass/fail fixtures for regression testing
- Full CI pipeline: ruff → mypy → pytest → smoke tests

Unlike LLM-as-judge approaches, these validators are deterministic, fast, and CI-friendly.
```

---

## 3. `kyrolabs/awesome-agents` (~5k ⭐)

**URL**: <https://github.com/kyrolabs/awesome-agents>
**Section**: "Agent Frameworks" or "Domain-Specific Agents"

**PR entry:**

```markdown
- **[zilan-agent](https://github.com/RyanYao527/zilan-agent)** — Buddhist philosophy AI agent with Skill/Agent dual-track architecture, output-contract validators, and built-in Agama scripture search engine (87K lines). Supports Claude Code, Codex, and OpenAI-compatible providers.
```

---

## 4. `Hannibal046/Awesome-LLM` (~18k ⭐)

**URL**: <https://github.com/Hannibal046/Awesome-LLM>
**Section**: "LLM Applications" or "LLM Reliability & Safety"

**PR entry:**

```markdown
- **[zilan-agent](https://github.com/RyanYao527/zilan-agent)** — Demonstrates the *Output Contract* pattern for LLM reliability: deterministic validators check required terms, forbidden phrases, and boundary statements in LLM responses without calling another model. 277 tests, MIT license.
```

---

## PR submission checklist

For each list, before submitting:

- [ ] Read the list's CONTRIBUTING.md
- [ ] Check if a similar entry already exists
- [ ] Fork → create branch → add entry → PR
- [ ] Use the exact format shown in each list (some use `|` tables, some use `-` bullets)
- [ ] One PR per list (don't batch them)

### Submission order (highest impact first)

1. `travisvn/awesome-claude-skills` — most directly relevant, most likely to drive Claude Code users
2. `promptslab/Awesome-Prompt-Engineering` — positions the output contract angle
3. `Hannibal046/Awesome-LLM` — largest audience
4. `kyrolabs/awesome-agents` — broad agent ecosystem exposure
