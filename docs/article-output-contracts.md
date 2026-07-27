# Output Contracts: Stop Eyeballing LLM Responses

> **LLMs drift. Prompts alone can't fix it.** Output Contracts are structured specs that define required terms, forbidden phrases, and boundary statements — and Deterministic Validators check them at CI speed without calling a model. Here's the pattern, with real code from a production-grade open-source project.

---

## 1. The Problem: "It Works in Dev, It Drifts in Prod"

Picture this. You're shipping an LLM-powered medical Q&A feature. You write a careful system prompt: *"Always include a disclaimer. Never claim a guaranteed cure. Always tell the user to consult their doctor."* You test it with 20 questions. It's perfect. You ship.

Two weeks later, a user posts a screenshot on Twitter. Your LLM just told someone with chest pain that *"turmeric tea has been shown to reduce inflammation"* — with no disclaimer, no "consult your doctor," no boundary at all.

You check the prompt. It hasn't changed. You test the same 20 questions. 17 of them get the disclaimer, 3 don't. The prompt was never the problem. The problem is that **LLMs sample from a distribution, and no prompt, however well-crafted, guarantees that a specific term will appear or that a forbidden phrase won't.**

The standard responses to this problem all have limits:

| Approach | The problem |
| --- | --- |
| "Write a better prompt" | Diminishing returns. You can't prompt your way out of sampling variance. |
| "Use an LLM-as-judge" | You've introduced a second non-deterministic component to check the first one. Who checks the checker? |
| "Human review at scale" | Doesn't scale. And if you're reviewing every output, why use an LLM at all? |

There's a third option. Treat LLM outputs as structured data — and validate them like structured data.

---

## 2. The Core Idea: Output Contracts

An **output contract** is a structured specification with three layers:

| Layer | Question it answers | Example from a Buddhist-text citation system |
| --- | --- | --- |
| **Required slots** | What MUST appear in every response? | `检索范围` (search scope), `CBETA` ID, `context/agama/` file anchor |
| **Forbidden terms** | What must NEVER appear? | `校勘完成` (collation finished), `已穷尽` (exhaustive), `可作为定本` (can serve as definitive edition) |
| **Boundary statements** | What qualifier must frame the answer? | `待校勘` (pending scholarly collation), `未作校勘定案` (not a definitive edition) |

Each layer catches a different failure mode:

- **Required slots** catch omission. The LLM cited a sutra but forgot to say *which edition*.
- **Forbidden terms** catch overclaim. The LLM presented a working-corpus keyword search as if it were a definitive scholarly edition.
- **Boundary statements** catch frame errors. The LLM blurred the line between a search tool's output and peer-reviewed textual scholarship.

The key insight: **these are all checkable deterministically.** `"待校勘" in response_text` is `True` or `False`. You don't need an LLM to verify it. You don't need embeddings. You need `str.contains()`, structured properly, with a CI runner around it.

Here's a concrete example. Two responses to the same query — "Give me Āgama evidence on anattā (non-self)" — are checked against the same contract:

**Pass:**
> 检索范围：本次只基于本地 `context/agama/` 中四阿含材料做代表性检索。代表性引文之一：`《雜阿含經》(T02n0099) 卷 1, context/agama/T0099-za-agama.md:147-149`。边界：出版级引文、异本差异与标点断句仍待校勘。

**Fail:**
> 四阿含里关于无我的资料已经查全，结论已穷尽，无需校勘，可作为定本，校勘完成，校勘确认。

The fail response is well-formatted and confident. It's also dangerously wrong — it claims scholarly finality for a local keyword search. The contract catches what a human skim might miss.

---

## 3. The Validators: Deterministic, Not Magic

If output contracts are the spec, **deterministic validators** are the test suite. The architecture is straightforward:

```
LLM response
    │
    ▼
┌──────────────────────────┐
│  Answer Contract Review  │  ← checks required slots, forbidden terms, boundary statements
│  (shallow surface check) │
└──────────┬───────────────┘
           │ pass / fail
           ▼
┌──────────────────────────┐
│  Domain Validators       │  ← deep structural checks per contract family
│  (5 engines)             │
└──────────┬───────────────┘
           │ structured JSON result
           ▼
      CI passes or fails
```

Let me walk through one validator in detail, because the pattern is the same across all five.

### Deep dive: the Hetuvidya (Buddhist logic) validator

In Buddhist logic, a valid argument must satisfy three conditions called the *three marks* (因三相):

1. **遍是宗法性** (paksa-dharmata): the reason must be established on the subject
2. **同品定有性** (sapaksa-sattva): the reason must be present in at least one same-side case
3. **异品遍无性** (vipaksa-asattva): the reason must be absent from all opposite-side cases

A classic example: *"Sound is impermanent, because it is produced."* The three marks check whether being-produced is a valid reason to establish impermanence.

The validator doesn't do natural-language reasoning. It reads a structured YAML fixture:

```yaml
# tests/reasoning_cases.yaml
- id: ZR-01
  title: 因三相正因样例
  contracts:
    - hetuvidya
  prompt: "孜澜，什么是因三相？请用'声，应是无常，以所作性故'说明。"
  expected:
    hetuvidya:
      subject: 声                # "sound"
      predicate: 无常            # "impermanent"
      reason: 所作性             # "produced"
      result: positive_reason    # all three marks pass
      checks:
        paksa_dharmata: pass
        sapaksa_sattva: pass
        vipaksa_asattva: pass
```

The validator (`scripts/zilanlib/reasoning/hetuvidya_validator.py`) reads this, checks each mark against the declared status, and emits a deterministic JSON result:

```json
{
  "status": "pass",
  "validator": "hetuvidya_validator",
  "validations": [{
    "case_id": "ZR-01",
    "trairupya_checks": [
      {"id": "paksa_dharmata", "status": "pass", "status_label": "passes"},
      {"id": "sapaksa_sattva", "status": "pass", "status_label": "passes"},
      {"id": "vipaksa_asattva", "status": "pass", "status_label": "passes"}
    ],
    "judgment": {
      "result": "positive_reason",
      "status": "valid",
      "failed_checks": []
    }
  }]
}
```

If the fixture declares `paksa_dharmata: fail`, the validator returns `status: "invalid"` with a diagnostic pointing to the specific check that failed. No model call. No embedding. No API key. The validator is ~170 lines of Python, and it runs in milliseconds.

The same pattern powers all five validators:

| Validator | Contract family | What it checks |
| --- | --- | --- |
| `hetuvidya_validator.py` | Hetuvidya (因明) | Three-mark logical structure |
| `collected_topics_analyzer.py` | Collected Topics (摄类学) | Total/part relationships, pervasion errors |
| `madhyamaka_critique_engine.py` | Madhyamaka (中观) | Opponent-premise tracking, nihilism boundary |
| `cognitive_analysis_mapper.py` | Cognitive Analysis (心类学) | Five-universal chain, corrective-factor mapping |
| `agama_evidence_checker.py` | Agama Evidence (阿含) | Citation format, collation boundary, local anchors |

---

## 4. Answer Contract Review: Regression Testing for Prompts

The validators check structure. The **answer contract review** checks the surface — it's the CI gate that says "before we even look at whether the reasoning is valid, does the response contain what it's supposed to contain?"

It works with checked-in pass/fail fixtures — real LLM responses that demonstrate compliance and violation:

```bash
# Run the contract review against a known-good response
python scripts/reasoning_contract_runner.py \
  --query-id SRQ-04 \
  --sample-id srq04-agama-citation-boundary-pass \
  --json
# → "overall_status": "pass"

# Run it against a known-bad response
python scripts/reasoning_contract_runner.py \
  --query-id SRQ-04 \
  --sample-id srq04-agama-citation-boundary-fail \
  --json
# → "overall_status": "fail"
```

Here's what the review catches in the fail sample:

| Check | Result |
| --- | --- |
| Has `检索范围`? | ❌ Missing |
| Has `CBETA` / `T02n0099`? | ❌ Missing |
| Has `context/agama/` anchor? | ❌ Missing |
| Has `待校勘` boundary? | ❌ Missing |
| Forbidden: `校勘完成`? | ❌ Present (collation-finished overclaim) |
| Forbidden: `已穷尽`? | ❌ Present (exhaustiveness overclaim) |

The practical value: **when you change a system prompt, you don't eyeball a few outputs and hope.** You run the contract runner. If the new prompt causes the LLM to drop `待校勘` or start saying `校勘完成`, you know immediately — before users do. This is the same mental model as any other regression test: change code, run tests, see red, fix.

---

## 5. The Engineering Numbers

Patterns are cheap. Working, tested, CI-guarded code makes the case:

```text
172 tests, all passing
86% code coverage on zilanlib (the core library)
mypy:  0 errors across 48 source files
ruff:  0 issues (B/BLE/E/F/I/SIM/UP rules)
CI:    lint → type-check → test → smoke-test on every push
```

The project is `zilan-agent` on GitHub. It is intentionally dependency-minimal — PyYAML is the only runtime dependency. It does not use LangChain, LlamaIndex, vector databases, Docker, or any LLM-as-judge framework. The validators are pure Python functions that read YAML fixtures and return JSON. You can clone the repo, run `pytest`, and have 172 green dots in under a minute.

---

## 6. Generalization: This Works Anywhere LLMs Must Not Drop Critical Terms

The domain of this project is deliberately obscure — Buddhist logic with classical Chinese texts — but the pattern is domain-agnostic. An output contract is just a spec for what an LLM must and must not say. Here's the translation table:

| Domain | Required slot | Forbidden term | Boundary statement |
| --- | --- | --- | --- |
| **Medical Q&A** | `disclaimer` | `guaranteed cure`, `proven to heal` | `Consult your doctor`, `Not medical advice` |
| **Legal assistant** | `jurisdiction` | `this is legal advice` | `Consult an attorney` |
| **Financial advice** | `risk warning` | `guaranteed return`, `risk-free` | `Past performance ≠ future results` |
| **Buddhist text search** | `检索范围`, `CBETA`, `context/agama/` | `校勘完成`, `已穷尽`, `可作为定本` | `待校勘`, `未作校勘定案` |

The validation code doesn't change across domains — it's always "does the response contain X, is it free of Y, does it include Z?" The domain expertise goes into the YAML fixtures, not the validator code.

**Three questions to decide if this pattern fits your project:**

1. Is there a term your LLM *must* include in every response of a certain type? → Required slot
2. Is there a phrase it must *never* say? → Forbidden term
3. Is there a qualifier that must frame the answer? → Boundary statement

If you answered yes to any of these, you have an output contract. Write it down. Write a deterministic check for it. Put it in CI. You've just eliminated an entire class of LLM failures — permanently.

---

## 7. Limitations: When NOT to Use This

Be clear about what this pattern does and doesn't do:

- **Output contracts check structure, not correctness.** A response can pass every contract check and still be factually wrong. The validator confirms that the required safety terms are present — it does not verify that the medical advice between the disclaimers is sound.
- **The validators are deterministic fixture checkers, not semantic evaluators.** They verify that expected terms are present, that forbidden terms are absent, and that boundary statements frame the answer. They do not grade the quality of reasoning.
- **This pattern requires domain expertise to define the contracts.** Someone has to know what terms are required, forbidden, and boundary-critical. The validator automates the check, but a domain expert must define what gets checked.
- **It complements, not replaces, human review and eval benchmarks.** Think of it as the "lint" layer of LLM reliability — it catches obvious structural errors so humans can focus on substance. A linter won't tell you if your logic is sound, but it will tell you if you forgot a semicolon. Output contracts won't tell you if an LLM's advice is good, but they will tell you if it forgot the disclaimer.

---

## 8. Steal This Pattern

The project is open-source (MIT). Read the code, run the tests, and port the pattern to your own domain.

**[github.com/RyanYao527/zilan-agent](https://github.com/RyanYao527/zilan-agent)**

```bash
git clone https://github.com/RyanYao527/zilan-agent.git
cd zilan-agent
pip install -e ".[dev]"
python -m pytest                     # 172 tests
python scripts/reasoning_contract_runner.py \
  --query-id SRQ-04 \
  --sample-id srq04-agama-citation-boundary-pass \
  --json                            # see a contract check in action
```

Contributors welcome — especially if you want to port the output-contract pattern to medical, legal, or financial domains. The validator code is ~170 lines per engine, and the contract YAML format is straightforward. If you have domain expertise in a field where LLMs must not drift, you can write the contracts and I'll help with the validators.

---

*The project also happens to be a working Buddhist philosophy agent. But that's a different article.*
