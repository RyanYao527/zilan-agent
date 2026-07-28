# 孜澜 · Zilan

> **Independent Buddhist practitioner** · **独立修行者**
>
> AI 大语言模型佛学 Agent / Skill 双轨框架 · Buddhist Agent / Skill framework for AI LLMs
>
> 基于优婆塞姚磊佛学体系 · Based on Upāsaka Yao Lei's Buddhist study system

---

## 🌐 Choose your language · 选择语言

| | 语言 | Language | 入口 Entry |
| --- | --- | --- | --- |
| 🇨🇳 | **中文** | Chinese | **[`README.zh.md`](README.zh.md)** |
| 🇺🇸 | **English** | English | **[`README.en.md`](README.en.md)** |

> 💡 *Tip: GitHub 会根据你的浏览器语言自动显示对应版本。如果你想切换,点击上表中的入口即可。*
> *GitHub auto-detects your browser language. Click an entry above to switch.*

---

## ⚡ 30 秒快速上手 · Quick start in 30 seconds

```bash
# 1. Clone
git clone https://github.com/RyanYao527/zilan-agent.git

# 2. Copy into your Claude Code skills directory
cp -r zilan-agent ~/.claude/skills/

# 3. Optional: install the Claude Code Agent definition
mkdir -p ~/.claude/agents
cp zilan-agent/agents/zilan-claude-code.md ~/.claude/agents/zilan.md

# 4. In any Claude session, mention 孜澜 / Zilan / 因明 / 摄类学 to activate
```

---

## 🏗️ For Engineers · 面向开发者

> **This is not just a Buddhist skill — it's a production-grade LLM reliability engineering demo.**
>
> 这不仅仅是一个佛学 skill——它是一个**面向 LLM 可靠性工程的生产级演示项目**。

### The hard problem · 要解决的问题

LLMs in specialized domains drift: they drop critical terms, overclaim certainty, or blur safety boundaries. Most projects respond with "better prompts + human review." zilan-agent takes a different approach.

专业领域中的 LLM 输出容易漂移：遗漏关键术语、夸大确定性、模糊安全边界。大多数项目的应对是「调 prompt + 人工复核」。zilan-agent 走了一条不同的路。

### The approach · 解决思路

| Layer 层 | What it does 作用 |
| --- | --- |
| **Output contracts** 输出契约 | Structured specification of required terms, forbidden phrases, and boundary statements that every LLM response must satisfy. 结构化的规范：定义每个 LLM 回答必须包含的词槽、禁区词汇和边界声明。 |
| **Deterministic validators** 确定性验证器 | 5 pure-Python validators that check contract compliance without calling any model or API — no LLM-as-judge, no embeddings, no vectors. 5 个纯 Python 验证器，在不调用任何模型或 API 的情况下检查契约合规性。 |
| **Answer-contract review** 答案契约审查 | Pass/fail fixture samples let you regression-test prompt changes against expected output structure. 通过 pass/fail 样本夹具，对 prompt 变更进行回归测试。 |

### The numbers · 工程指标

```text
176 tests    ·    86% code coverage (zilanlib)
mypy: 0 errors across 52 source files
ruff:  0 issues (B/BLE/E/F/I/SIM/UP rules)
CI:    lint → type-check → test → smoke-test on every push
```

### See it in action · 一分钟验证

```bash
# Run a reasoning-contract check — deterministic, no API call
python scripts/reasoning_contract_runner.py \
  --query-id SRQ-04 \
  --sample-id srq04-agama-citation-boundary-pass \
  --json

# Check if an LLM answer respects the Agama citation contract:
# - Must include 检索范围, CBETA ID, context/agama/ anchor
# - Must carry 待校勘 boundary statement
# - Must not claim exhaustive or publication-grade collation
```

### Why this generalizes · 泛化价值

The output-contract + deterministic-validator pattern works for **any domain where LLMs must not drop critical terms**: medical disclaimers, legal boundaries, compliance checklists, financial risk warnings. zilan-agent is a complete, tested, CI-guarded reference implementation — built in a deliberately challenging domain (Buddhist logic) to prove the pattern holds under complexity.

输出契约 + 确定性验证器模式适用于**任何 LLM 不能遗漏关键术语的领域**：医疗免责声明、法律边界、合规清单、金融风险警告。zilan-agent 提供了一个完整、有测试覆盖、CI 守护的参考实现——刻意选择了一个高复杂度领域（佛学逻辑）来证明模式的有效性。

---

## 📦 What's inside · 仓库内容

| 文件 File | 用途 Purpose |
| --- | --- |
| `SKILL.md` | 完整 skill 定义(中文) · Full skill definition (Chinese) |
| `SKILL-en.md` | 完整 skill 定义(英文) · Full skill definition (English) |
| `README.zh.md` | 完整文档 · Full documentation (Chinese) |
| `README.en.md` | 完整文档 · Full documentation (English) |
| `CONTRIBUTING.md` / `CONTRIBUTING-en.md` | 贡献指南(含四级贡献者阶梯) · How to contribute (with 4-tier contributor ladder) |
| `CHANGELOG.md` | 版本变更记录 · Release notes |
| `ARCHITECTURE.md` | 架构入口与设计决策 · Architecture overview and design decisions |
| `CODE_OF_CONDUCT.md` | 社区行为准则 · Community code of conduct |
| `LICENSE` / `THIRD_PARTY_NOTICES.md` | MIT for project-original code/docs; CBETA-derived Agama corpus follows CBETA terms |
| `agents/zilan-claude-code.md` | Claude Code Agent 定义 · Claude Code Agent definition |
| `agents/zilan-codex.md` | Codex sub-agent prompt · Codex sub-agent prompt |
| `agents/openai.yaml` | 跨平台 Agent 配置 · Cross-platform Agent metadata |
| `CODEX_REGRESSION_TESTS.md` | Codex 回归测试矩阵 · Codex regression matrix |
| `docs/platform-validation.md` | 平台验证状态 · Platform validation status |
| `docs/runtime-validation-log.md` | 运行验证记录 · Runtime validation log |
| `docs/runtime-evidence/` | 脱敏运行证据摘录 · Redacted runtime evidence excerpts |
| `docs/maintenance-roadmap.md` | 维护路线图 · Maintenance roadmap |
| `docs/installation.md` | 安装与运行指南 · Installation and runtime guide |
| `docs/validation-evidence.md` | 运行证据归档规范 · Runtime evidence policy |
| `docs/provider-routes.md` | Provider 路线归类 · Provider route triage |
| `docs/openai-api-harness.md` | OpenAI API harness 说明 · OpenAI API harness guide |
| `docs/article-output-contracts.md` | 输出契约技术文章 · Output Contracts technical article |
| `docs/zilan-contract-quickstart.md` | zilan_contract 快速上手 · zilan_contract quickstart |
| `docs/awesome-list-pr-entries.md` | Awesome-list PR 条目 · Awesome-list PR entries |
| `docs/codex-manual-tasks.md` | Codex 手动操作清单 · Codex manual task checklist |
| `docs/archive/` | 历史归档材料 · Historical archive |
| `zilan_contract/` | 独立 pip 包 (ContractRunner + 验证器) · Standalone pip package |
| `scripts/validate_zilan_repo.py` | 仓库结构与语料 smoke 校验 · Repository invariant checks |
| `scripts/search_agama.py` | 阿含 Markdown 检索工具 · Agama Markdown search helper |
| `scripts/openai_api_harness.py` | OpenAI Responses API dry-run/live harness |
| `scripts/hf_upload_dataset.py` | HuggingFace Dataset 上传 · HF dataset upload |
| `scripts/mock_install_smoke.py` | Claude Code mock install smoke test |
| `scripts/demo.sh` / `scripts/demo.tape` | CLI 演示录制 · CLI demo recording |
| `.github/workflows/ci.yml` | 自动化校验 · Automated CI checks |
| `context/摄类学工具箱.md` | 摄类学推理工具链 · Collected Topics reasoning toolkit |
| `context/因明推理引擎.md` | 因明逻辑引擎 · Buddhist logic engine |

---

## 🧭 Skill / Agent dual track · 双轨模式

- **Skill mode**: lightweight dialogue, daily practice reflection, and simple concept explanation.
- **Agent mode**: explicit deep research for Agama retrieval, Buddhist logic chains, cross-domain analysis, and long reports.
- **Codex**: use explicit prompts such as `spawn a zilan agent` / `让孜澜独立深入研究一下`; regression cases live in `CODEX_REGRESSION_TESTS.md`.

---

## ✅ Compatibility status · 兼容性状态

- **Platform status**: `agents/openai.yaml` is the machine-readable metadata source; `docs/platform-validation.md` records status definitions, validation evidence, and update rules.
- **Current validation**: Codex is `tested` for ZC-01 through ZC-06 as of 2026-06-15; Claude Code is `tested` for ZC-01 through ZC-06 through UTF-8 stdin as of the 2026-06-18 post-contract full rerun; Volcengine OpenAI-Compatible is `tested` for ZC-01 through ZC-03 as of 2026-06-16; native OpenAI API remains `harness-ready`.
- **Runtime boundary**: Codex, Claude Code, native OpenAI API, Volcengine OpenAI-Compatible, DeepSeek, GLM, and Qwen routes must not be described as tested unless the platform validation document says so.
- **Scholarly collation**: local Agama Markdown is a searchable working corpus; publication-level work should verify against CBETA XML and parallel texts.
- **Third-party data license boundary**: project-original code/docs are MIT; CBETA-derived Agama files and excerpts are governed by CBETA terms, not relicensed by this repository; see `THIRD_PARTY_NOTICES.md`.

---

## 🧪 Engineering checks · 工程校验

```bash
python scripts/validate_zilan_repo.py --check-generated
python -m pytest
python -m ruff check scripts tests
python -m mypy
python scripts/openai_api_harness.py --case ZC-02 --json
python scripts/mock_install_smoke.py
python scripts/search_agama.py --terms "無我|非我|緣起" --limit 10
python scripts/search_agama.py --terms "非我" --passages --group-by juan --limit 10
python scripts/search_agama.py --terms "緣起" --json --limit 5
```

GitHub Actions runs the same invariant checks, tests, and Agama search smoke test on push and pull request.

`search_agama.py` text and JSON output include stable citation fields with sutra name, CBETA ID,卷, and local Markdown line references, for example `《雜阿含經》(T02n0099) 卷 1, context/agama/T0099-za-agama.md:33`.

Maintenance priorities and release guardrails are tracked in `docs/maintenance-roadmap.md`.

Manual runtime validation evidence is tracked in `docs/runtime-validation-log.md`.

Installation paths are documented in `docs/installation.md`; evidence and transcript rules are documented in `docs/validation-evidence.md`; redacted evidence excerpts live in `docs/runtime-evidence/`; provider route triage is documented in `docs/provider-routes.md`; release notes are tracked in `CHANGELOG.md`.

---

## 🤝 Seeking co-maintainers · 寻找协作维护者

zilan-agent is currently maintained by one person. Regular contributors or co-maintainers are welcome, especially if you are:

- a Buddhist practitioner or student interested in the intersection of Dharma and AI
- a software engineer who cares about LLM reliability, output contracts, and validation evidence
- comfortable reviewing Chinese and English documentation

If you would like to help maintain or contribute regularly, please open an issue first so scope, expectations, and review boundaries can be discussed publicly.

Areas where help is most useful:

- Documentation review and translation consistency
- Platform validation on new Claude Code / Codex / provider releases
- Scholarly collation of Agama corpus references against CBETA XML sources
- Reasoning-contract fixture review for Hetuvidya, Collected Topics, Madhyamaka, and cognitive-analysis cases

---

## 🔑 唤醒关键字 · Activation keywords

**主关键字 Primary**: `孜澜` · `Zilan`
**身份 Identity**: `姚磊` · `优婆塞` · `Upāsaka` · `Yao Lei`
**经典 Scriptural**: `阿含经` · `Agama`
**逻辑 Logical**: `因明` · `摄类学` · `应成论式` · `因三相` · `四句逻辑`
**场景 Contextual**: `数字人佛学` · `数字人修学` · `Buddhist digital persona`

---

*诸行无常，诸法无我，涅槃寂静。*
