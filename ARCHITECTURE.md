# Architecture

## Overview

`zilan-agent` is a Buddhist Skill / Agent dual-track framework for AI coding and language-model runtimes.

- **Skill mode**: `SKILL.md` / `SKILL-en.md` define lightweight dialogue behavior for concept lookup, daily practice reflection, and bounded Dharma discussion.
- **Agent mode**: `agents/zilan-claude-code.md` / `agents/zilan-codex.md` define deeper research behavior for Agama retrieval, cross-domain reasoning, and long-form analysis.
- **Portable metadata**: `agents/openai.yaml` records cross-platform routing metadata without treating every provider as tested.

The project is intentionally local-first: repository checks, fixture validators, and dry-run harnesses run without model calls unless a runtime validation task explicitly invokes a provider or CLI.

## Directory Layout

```text
zilan-agent/
├── SKILL.md, SKILL-en.md              # Skill definitions
├── README.md, README.zh.md, README.en.md
├── CHANGELOG.md
├── THIRD_PARTY_NOTICES.md             # CBETA-derived corpus license boundary
├── agents/
│   ├── zilan-claude-code.md           # Claude Code agent prompt
│   ├── zilan-codex.md                 # Codex sub-agent prompt
│   └── openai.yaml                    # Cross-platform metadata
├── context/
│   ├── agama/                         # CBETA-derived Agama working corpus
│   ├── 摄类学工具箱.md                 # Collected Topics reasoning toolkit
│   ├── 因明推理引擎.md                 # Hetuvidya logic engine
│   ├── 心类学认知分析.md               # Cognitive-analysis framework
│   ├── 中观应成精要.md                 # Madhyamaka prasaṅga framework
│   ├── 南传观禅指南.md                 # Vipassana practice framework
│   └── 模因机器视角下的佛教结集与传播.md
├── scripts/
│   ├── zilanlib/                      # Shared Python library modules
│   │   ├── agama/                     # Search / fixture review helpers
│   │   ├── reasoning/                 # Structured reasoning validators
│   │   └── semantic/                  # Semantic fixture and answer-contract helpers
│   ├── *_validator.py                 # Stable CLI wrappers
│   ├── *_mapper.py / *_engine.py      # Stable CLI wrappers
│   ├── search_agama.py                # Stable Agama Markdown search CLI
│   ├── openai_api_harness.py          # Dry-run/live API harness
│   └── validate_zilan_repo.py         # Repository invariant checks
├── tests/
│   ├── fixtures/                      # YAML and Markdown test fixtures
│   ├── regression_cases.yaml          # ZC regression inventory
│   └── reasoning_cases.yaml           # ZR reasoning-contract cases
├── docs/
│   ├── architecture/                  # Reasoning contract and interface notes
│   ├── runtime-evidence/              # Redacted runtime evidence excerpts
│   ├── platform-validation.md         # Platform status source of truth
│   ├── runtime-validation-log.md      # Manual runtime validation log
│   ├── maintenance-roadmap.md         # Maintenance baseline and priorities
│   └── provider-routes.md             # Provider route triage
└── .github/workflows/ci.yml
```

## Core Design Decisions

### 1. Skill / Agent Dual Track

The Skill surface is optimized for short, direct interactions. The Agent prompts are optimized for explicit research tasks that may need local file reads, Agama search, structured reasoning, or report output. This avoids forcing every lightweight exchange through a heavy research workflow.

### 2. Conservative Platform Status

Platform status is not inferred from configuration. `agents/openai.yaml` is the machine-readable metadata source, but `docs/platform-validation.md` is the human-readable source of truth for whether a route is `tested`, `harness-ready`, `config-only`, or blocked. Native OpenAI API, OpenAI-compatible providers, Claude Code, Codex, DeepSeek, GLM, and Qwen are tracked separately.

### 3. Output Contracts Before Infrastructure

The project improves answer reliability through explicit contracts before adding heavier infrastructure. Current contract families include:

- **Agama evidence**: cite sutra name, CBETA ID, local `context/agama/` anchor, search scope, representative status, and collation boundary.
- **Hetuvidya**: preserve subject, predicate, reason, and the three trairupya checks.
- **Collected Topics**: preserve total/part, defining-mark/definiendum, pervasion, and category-boundary checks.
- **Madhyamaka prasaṅga**: critique from the opponent's premise, expose contradiction, and avoid independent thesis overclaim.
- **Cognitive-analysis / practice boundary**: map daily experience through cognitive-analysis and vipassana terms while avoiding therapy or attainment claims.

### 4. Deterministic Local Validators

The local validators read checked-in YAML / Markdown fixtures and emit deterministic JSON or text results. They do not call model providers and do not claim to grade final Buddhist doctrinal correctness.

Key wrappers include:

- `scripts/reasoning_contract_runner.py`
- `scripts/hetuvidya_validator.py`
- `scripts/collected_topics_analyzer.py`
- `scripts/madhyamaka_critique_engine.py`
- `scripts/cognitive_analysis_mapper.py`
- `scripts/agama_evidence_checker.py`
- `scripts/semantic_retrieval_dry_run.py`
- `scripts/semantic_answer_contract_review.py`

### 5. Stable CLI Wrappers Plus `zilanlib`

Root-level `scripts/*.py` files remain stable CLI entrypoints for users and CI. Reusable logic lives under `scripts/zilanlib/` so implementation can be refactored without breaking existing commands.

### 6. Local Agama Corpus Boundary

`context/agama/` is a searchable working corpus derived from CBETA XML-P5. Project-original code and documentation are MIT-licensed, but CBETA-derived text and excerpts remain governed by CBETA terms and are not relicensed by this repository. Publication-level work should verify Markdown hits against CBETA XML and relevant parallels.

## Validation Workflow

Run the standard local checks before merging prompt, context, script, fixture, or platform metadata changes:

```powershell
python scripts\validate_zilan_repo.py --check-generated --strict-yaml
python -m pytest
python -m ruff check scripts tests
python -m mypy
```

For targeted reasoning-contract review, use:

```powershell
python scripts\reasoning_contract_runner.py --query-id SRQ-11 --sample-id srq11-collected-topics-definition-scope-pass --json
```

For provider request construction without a live API call, use:

```powershell
python scripts\openai_api_harness.py --case ZC-02 --json
```

## CI Pipeline

GitHub Actions runs:

1. install development dependencies
2. `ruff`
3. `mypy`
4. repository invariant validation
5. `pytest`
6. OpenAI API harness smoke test
7. mock Claude Code install smoke test
8. Agama search CLI smoke test

CI proves repository structure, fixtures, and deterministic helpers are coherent. It does not replace manual runtime answer review.

## Runtime Evidence

Runtime evidence belongs in:

- `docs/runtime-validation-log.md`
- `docs/runtime-evidence/`

Do not upgrade a route to `tested` unless the validation log records the date, provider or runtime, prompt set, known limits, and evidence summary required by `docs/platform-validation.md` and `docs/validation-evidence.md`.

## Documentation Map

- Installation: `docs/installation.md`
- Platform validation: `docs/platform-validation.md`
- Provider route triage: `docs/provider-routes.md`
- Runtime evidence policy: `docs/validation-evidence.md`
- Maintenance baseline: `docs/maintenance-roadmap.md`
- Regression matrix: `CODEX_REGRESSION_TESTS.md` and `tests/regression_cases.yaml`
- Reasoning contract design: `docs/architecture/reasoning-contract.md`
- Semantic retrieval interface: `docs/architecture/semantic-retrieval-interface.md`

## What Not To Add Yet

The current architecture intentionally does not require LangChain, LlamaIndex, a vector database, FastAPI, Docker, Kubernetes, or an LLM judge. Add those only after the repository has a concrete interface, evidence, and scale requirement that justifies the extra moving parts.
