# Codex 手动操作清单

以下 4 项任务需要在本地手工执行。每项独立，可按任意顺序完成。

---

## 任务 A：录制 CLI 演示 GIF

### 前提

```bash
# 安装 vhs（charmbracelet 出品）
# macOS:  brew install vhs
# Linux: 参考 https://github.com/charmbracelet/vhs#installation
# Windows: 用 WSL 或 asciinema 替代
```

### 步骤

```bash
cd zilan-agent/
vhs scripts/demo.tape
# 生成 demo.gif（约 5-10 秒）
```

### 完成后

把 `demo.gif` 放在仓库根目录，然后在 README.md 的 "30 秒快速上手" 板块上方加一行：

```markdown
![demo](demo.gif)
```

---

## 任务 B：上传 HuggingFace Dataset

### 前提

```bash
pip install datasets huggingface_hub
huggingface-cli login
# 需要 HF 账号 + write token
```

### 步骤

```bash
cd zilan-agent/

# 先 dry-run，确认数据正确
python scripts/hf_upload_dataset.py --dry-run

# 输出应显示：
#   Total: 1844 passages (Agama) + 6 files (knowledge base)
#   Combined: 2,082,249 characters, 1850 rows

# 确认无误后上传
python scripts/hf_upload_dataset.py --repo <你的HF用户名>/zilan-agent-kb
```

### 完成后

数据集将出现在 `https://huggingface.co/datasets/<你的用户名>/zilan-agent-kb`

在 README.md 的工程指标板块下方可以加：

```markdown
📦 Also available as a HuggingFace Dataset: [`<用户名>/zilan-agent-kb`](https://huggingface.co/datasets/<用户名>/zilan-agent-kb)
```

---

## 任务 C：提 Awesome-List PR

4 个列表的 PR 条目已写好，见 `docs/awesome-list-pr-entries.md`。

### 通用操作流程（每个列表重复一遍）

```bash
# 1. 在 GitHub 网页 fork 目标仓库
# 2. Clone 你的 fork
git clone https://github.com/<你的用户名>/<awesome-list>.git
cd <awesome-list>

# 3. 创建分支
git checkout -b add-zilan-agent

# 4. 编辑 README.md，按字母序插入条目（见 docs/awesome-list-pr-entries.md）

# 5. 提交
git add README.md
git commit -m "Add zilan-agent: Buddhist philosophy Agent/Skill with output-contract validators"
git push origin add-zilan-agent

# 6. 在 GitHub 网页上从你的 fork 提 Pull Request 到原仓库
```

### 推荐提 PR 顺序

| 顺序 | 仓库 | Stars | 目标板块 |
| ------ | ------ | ------- | --------- |
| 1 | `travisvn/awesome-claude-skills` | ~14k | Claude Code Skills |
| 2 | `promptslab/Awesome-Prompt-Engineering` | ~6k | Tools & Frameworks |
| 3 | `Hannibal046/Awesome-LLM` | ~18k | LLM Applications |
| 4 | `kyrolabs/awesome-agents` | ~5k | Domain-Specific Agents |

---

## 任务 D：发布技术文章

文章已写好，见 `docs/article-output-contracts.md`（~1973 词，8 章节）。

### 发布渠道（建议按顺序）

**1. dev.to**（最优先，自带开发者流量）

```
标题：Output Contracts: Stop Eyeballing LLM Responses
标签：llm, promptengineering, python, testing, opensource
正文：docs/article-output-contracts.md 内容
```

**2. Medium**

```
标题：同上
标签：LLM, Prompt Engineering, Python, Open Source
```

**3. Hacker News — Show HN**

```
标题：Show HN: Output Contracts — deterministic validators for LLM responses
URL：你的 dev.to 或 Medium 文章链接
```

**4. Reddit**

```
r/LocalLLaMA：发链接 + 一句话说明
r/MachineLearning：发链接 + 一句话说明
```

**5. Twitter / X**

直接用文章 TL;DR 发推：

> LLMs drift. Prompts alone can't fix it. Output Contracts are structured specs (required terms, forbidden phrases, boundary statements) + Deterministic Validators that check them at CI speed without calling a model. Here's the pattern with real code: [链接]

---

## 依赖关系

```
任务 A（录 GIF）          → 可独立执行
任务 B（上传 HF Dataset）  → 可独立执行
任务 C（提 Awesome PR）    → 可独立执行
任务 D（发文章）           → 建议在 A/B 之后（文章里可以链到 HF Dataset 和 GIF demo）
```

四项全部独立，没有先后依赖。
