# 贡献指南

感谢对孜澜 skill 的关注。

本项目遵循 [Contributor Covenant](CODE_OF_CONDUCT.md) 行为准则。参与讨论、提交 Issue 或 Pull Request 时，请遵守该准则。

## 🪜 贡献者阶梯

不需要成为佛学专家或资深工程师才能帮忙。以下是四个递进的参与层级，每一层都有明确的**技能要求**、**时间投入**和**首个任务**。从 Level 1 开始，逐步深入。

### Level 1：证据跑分者

> **做什么**：在 Claude Code / Codex / 新 provider 上运行 ZC 回归用例，提交运行时证据。
> **技能要求**：会用命令行
> **时间**：约 30 分钟 / 次
> **不要求**：Python、佛学知识、代码修改

**🎯 第一个任务：跑一次 Claude Code 回归验证**

1. 在 Claude Code 中加载 `agents/zilan-claude-code.md` 作为 agent
2. 依次发送 `tests/regression_cases.yaml` 中的 ZC-01 到 ZC-06 的 prompt
3. 保存回答（脱敏后）到 `docs/runtime-evidence/` 目录
4. 提交 PR，格式参考 `docs/runtime-evidence/` 中已有文件

**如果遇到问题**：开 Issue，标题用 `[Evidence]` 前缀，贴上你遇到的错误信息。

---

### Level 2：文档审阅者

> **做什么**：校对中英文文档一致性、阿含引用准确性、CBETA 编号正确性。
> **技能要求**：中英文阅读能力 + 基本佛学术语
> **时间**：1-2 小时 / 次
> **不要求**：Python、CI/CD 知识

**🎯 第一个任务：校对 SKILL.md 与 SKILL-en.md 的术语一致性**

1. 打开 `SKILL.md` 和 `SKILL-en.md`
2. 比较"输出契约"相关段落（搜索 `输出契约` / `output contract`）
3. 检查关键术语的翻译是否一致（如"待校勘"、"因三相"、"应成论式"）
4. 记录不一致的地方，开 Issue 标题用 `[Docs]` 前缀

**常见贡献方向**：

- 阿含引用中的 CBETA 编号与卷数是否正确
- README 与实际文件路径是否一致
- `context/` 文件中的概念定义有无歧义

---

### Level 3：契约审阅者

> **做什么**：复核 reasoning-contract fixture 的合理性，审阅 answer-contract sample 的 pass/fail 判定。
> **技能要求**：因明 / 摄类学 / 中观 / 心类学中至少一个领域的基础
> **时间**：2-4 小时 / 次
> **不要求**：Python 编程（但能读懂 YAML 更好）

**🎯 第一个任务：复核一个 answer-contract sample**

1. 阅读 `tests/reasoning_cases.yaml`，选一个你熟悉的领域（如 ZR-01 因明或 ZR-03 中观）
2. 找到对应的 pass/fail sample：`tests/fixtures/answers/srq*-pass.md` 和 `srq*-fail.md`
3. 判断：fail sample 是否真的好地展示了契约违规？pass sample 是否有边缘情况被漏判？
4. 开 Issue 标题用 `[Contract]` 前缀，附上你的分析

**常见贡献方向**：

- 新增推理用例（新的 ZR case）
- 对现有 fixture 的 boundary_statement 提出改进
- 讨论某个 forbidden term 是否过于严格或过于宽松

---

### Level 4：代码贡献者

> **做什么**：实现新 provider harness、扩展验证器、优化 zilanlib 架构。
> **技能要求**：Python + pytest
> **时间**：持续参与
> **建议**：先从 Level 1-3 中至少完成一个任务再进入 Level 4，熟悉项目结构后再写代码。

**🎯 第一个任务：为新 provider 添加 harness**

1. 阅读 `scripts/zilanlib/reasoning/hetuvidya_validator.py` 了解验证器模式
2. 如果你有某个 provider 的 API 权限（如 DeepSeek、GLM、Qwen），参考 `scripts/openai_api_harness.py` 写一个对应的 harness
3. 跑 ZC-01 到 ZC-03 的回归用例
4. 提交 PR，包含 harness 脚本 + 脱敏运行时证据

**常见贡献方向**：

- 扩展 `zilanlib/reasoning/` 中的验证器
- 优化 `scripts/search_agama.py` 的检索性能
- 改进 CI 流程
- zilanlib 架构重构

---

## 如何贡献

### 方式一：提交 Issue

- 发现 bug 或有改善建议，欢迎提交 GitHub Issue
- 请使用清晰的问题描述

### 方式二：Fork & Pull Request

1. Fork 本仓库
2. 创建分支（`git checkout -b feature/你的功能名`）
3. 提交更改（`git commit -m '你的提交信息'`）
4. Push（`git push origin feature/你的功能名`）
5. 提交 Pull Request

### 提交规范

- Commit 信息使用中文或英文，简洁描述
- 涉及核心定义修改的，请同步更新 `SKILL.md`、相关 `context/` 文件、`CHANGELOG.md` 和必要的验证文档
- 大幅修改请先提 Issue 讨论

## 本地验证

修改 `SKILL.md`、`agents/`、`context/`、阿含语料或脚本后，请至少运行：

```bash
python scripts/validate_zilan_repo.py --check-generated
python -m pytest
python scripts/search_agama.py --terms "無我|非我|緣起" --limit 10
```

`validate_zilan_repo.py` 会检查必要文件、Codex 回归矩阵、Agent prompt 关键片段、阿含检索 smoke test，并可验证 CBETA XML 生成的 Markdown 是否稳定。

## 成为协作维护者

协作维护者不是名义身份，而是持续承担一类可复查工作的角色。当前最适合的协作方向包括：

- 文档审阅与中英文一致性检查
- Claude Code、Codex、OpenAI API 或 OpenAI-compatible provider 的运行验证
- 阿含语料引用的 CBETA XML 回校与边界标注
- reasoning-contract fixture、answer-contract sample 和 runtime evidence 的复核

如果你希望成为长期协作者，请先提交 Issue，说明你希望负责的范围、可投入的频率，以及你能运行的验证环境。涉及平台状态、输出合约、阿含语料或核心 prompt 的变更，仍需通过小 PR、完整仓库检查和明确证据记录。

## 知识共建说明

本 skill 是活的学习系统，会随修学进展持续更新。核心知识沉淀在：

- `SKILL.md` — 主定义文件
- `context/摄类学工具箱.md` — 概念分析与逻辑推理工具链
- `context/因明推理引擎.md` — 因明逻辑引擎
- `CHANGELOG.md` — 用户可见变更记录
- `docs/runtime-validation-log.md` — 人工运行验证记录

欢迎通过 PR 共建。

---

*诸行无常，诸法无我，涅槃寂静。*
