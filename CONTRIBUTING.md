# 贡献指南

感谢对孜澜 skill 的关注。

本项目遵循 [Contributor Covenant](CODE_OF_CONDUCT.md) 行为准则。参与讨论、提交 Issue 或 Pull Request 时，请遵守该准则。

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

*寻遍十方谁是我，波心圆月本无澜*
