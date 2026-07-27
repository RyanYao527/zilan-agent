"""
Upload the zilan-agent knowledge base as a Hugging Face Dataset.

Usage:
  pip install datasets huggingface_hub
  huggingface-cli login
  python scripts/hf_upload_dataset.py [--repo YOUR_NAME/zilan-agent-kb]

The dataset includes:
  - Agama corpus (4 sutra files, ~5.9MB, 87K lines): Chinese Buddhist scriptures
    from CBETA, split into passages with citation metadata
  - Knowledge base (6 files): 因明, 摄类学, 心类学, 中观, 南传观禅, 模因分析
  - agama-index: search index over the Agama corpus

Output: a Dataset on Hugging Face Hub with train split, ready for
retrieval-augmented generation (RAG), fine-tuning, or text analysis.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
AGAMA_DIR = ROOT / "context" / "agama"
CONTEXT_DIR = ROOT / "context"

HF_DEFAULT_REPO = "zilan-agent-knowledge-base"

KB_FILES = {
    "collected_topics": "摄类学工具箱.md",
    "hetuvidya": "因明推理引擎.md",
    "cognitive_analysis": "心类学认知分析.md",
    "madhyamaka": "中观应成精要.md",
    "vipassana": "南传观禅指南.md",
    "memetics": "模因机器视角下的佛教结集与传播.md",
}

AGAMA_FILES = {
    "T0001-chang-agama.md": {
        "sutra_name_cn": "長阿含經",
        "cbeta_id": "T01n0001",
    },
    "T0026-zhong-agama.md": {
        "sutra_name_cn": "中阿含經",
        "cbeta_id": "T01n0026",
    },
    "T0099-za-agama.md": {
        "sutra_name_cn": "雜阿含經",
        "cbeta_id": "T02n0099",
    },
    "T0125-ekottarika-agama.md": {
        "sutra_name_cn": "增壹阿含經",
        "cbeta_id": "T02n0125",
    },
}

DATASET_CARD = """---
license: mit
language:
  - zh
  - en
tags:
  - buddhism
  - religion
  - chinese-classics
  - agama
  - sutra
  - cbeta
  - philosophy
  - logic
  - madhyamaka
  - vipassana
pretty_name: Zilan Agent Knowledge Base
size_categories:
  - 1M<n<10M
task_categories:
  - text-generation
  - question-answering
viewer: false
---

# Zilan Agent Knowledge Base

A structured knowledge base for Buddhist philosophy AI agents, combining:

- **Agama corpus**: Four Chinese Agama sutras (長阿含, 中阿含, 雜阿含, 增壹阿含)
  derived from CBETA XML-P5, totaling ~87,000 lines with citation metadata
- **Knowledge base files**: Six structured frameworks covering Buddhist logic
  (Hetuvidya), Collected Topics (bsdus grwa), Madhyamaka, Cognitive Analysis,
  Vipassana meditation, and Memetics

## Dataset structure

### `agama` subset (train split)
Each row is a passage (~paragraph) from an Agama sutra with:
- `text`: the passage text (Chinese)
- `sutra_name_cn`: sutra name in Chinese
- `cbeta_id`: CBETA canonical ID (e.g. T02n0099)
- `file_name`: local source file name
- `passage_index`: 0-based passage number within the file

### `knowledge_base` subset (train split)
Each row is a complete knowledge base file with:
- `text`: full file content (Chinese)
- `domain`: one of collected_topics, hetuvidya, cognitive_analysis, madhyamaka, vipassana, memetics
- `file_name`: local source file name

## Usage

```python
from datasets import load_dataset

# Load Agama passages
ds = load_dataset("YOUR_NAME/zilan-agent-knowledge-base", "agama")
for row in ds["train"]:
    print(row["cbeta_id"], row["text"][:100])

# Load knowledge base files
ds = load_dataset("YOUR_NAME/zilan-agent-knowledge-base", "knowledge_base")
for row in ds["train"]:
    print(row["domain"], len(row["text"]))
```

## Provenance

- Agama texts: derived from CBETA (Chinese Buddhist Electronic Text Association)
  XML-P5 editions. These are working corpus files; publication-level work should
  verify against CBETA XML and parallel texts.
- Knowledge base: original structured frameworks by Upasaka Yao Lei.
- Project code and documentation: MIT license. CBETA-derived text follows CBETA terms
  (see THIRD_PARTY_NOTICES.md).

## Related

- GitHub: https://github.com/RyanYao527/zilan-agent
"""


def _parse_agama_passages(text: str) -> list[str]:
    """Split Agama markdown into passages on section/paragraph boundaries."""
    passages = re.split(r"\n(?=#{1,4}\s|（[一二三四五六七八九十百千]+）)", text)
    return [p.strip() for p in passages if p.strip() and not p.strip().startswith("# 長阿含經")]


def _build_agama_dataset() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for file_name, meta in AGAMA_FILES.items():
        file_path = AGAMA_DIR / file_name
        if not file_path.exists():
            print(f"  SKIP: {file_name} not found")
            continue

        text = file_path.read_text(encoding="utf-8")
        passages = _parse_agama_passages(text)
        print(f"  {file_name}: {len(passages)} passages ({len(text)} chars)")

        for i, passage in enumerate(passages):
            if len(passage) < 20:
                continue
            rows.append({
                "text": passage,
                "sutra_name_cn": meta["sutra_name_cn"],
                "cbeta_id": meta["cbeta_id"],
                "file_name": file_name,
                "passage_index": i,
            })
    return rows


def _build_kb_dataset() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for domain, file_name in KB_FILES.items():
        file_path = CONTEXT_DIR / file_name
        if not file_path.exists():
            print(f"  SKIP: {file_name} not found")
            continue

        text = file_path.read_text(encoding="utf-8")
        print(f"  {file_name}: {len(text)} chars")
        rows.append({
            "text": text,
            "domain": domain,
            "file_name": file_name,
        })
    return rows


def _upload_dataset(repo_id: str, agama_rows: list[dict[str, Any]], kb_rows: list[dict[str, Any]]) -> None:
    try:
        from datasets import Dataset, DatasetDict
    except ImportError:
        print("ERROR: pip install datasets")
        raise

    agama_ds = Dataset.from_list(agama_rows)
    kb_ds = Dataset.from_list(kb_rows)

    dataset_dict = DatasetDict({
        "agama": agama_ds,
        "knowledge_base": kb_ds,
    })

    # Write README card
    readme_path = ROOT / "docs" / "hf-dataset-card.md"
    readme_path.write_text(DATASET_CARD, encoding="utf-8")

    print(f"\nPushing to Hugging Face Hub: {repo_id}")
    dataset_dict.push_to_hub(
        repo_id,
        private=False,
        commit_message="Initial upload: Agama corpus + knowledge base files",
    )
    print(f"\nDone: https://huggingface.co/datasets/{repo_id}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Upload zilan-agent knowledge base to Hugging Face")
    parser.add_argument(
        "--repo",
        default=HF_DEFAULT_REPO,
        help=f"Hugging Face repo ID (default: {HF_DEFAULT_REPO})",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Build dataset locally without uploading",
    )
    args = parser.parse_args()

    print("=== Agama corpus ===")
    agama_rows = _build_agama_dataset()
    print(f"  Total: {len(agama_rows)} passages")

    print("\n=== Knowledge base ===")
    kb_rows = _build_kb_dataset()
    print(f"  Total: {len(kb_rows)} files")

    total_chars = sum(len(r["text"]) for r in agama_rows) + sum(len(r["text"]) for r in kb_rows)
    print(f"\n  Combined: {total_chars:,} characters, {len(agama_rows) + len(kb_rows)} rows")

    if args.dry_run:
        print("\n[Dry run complete — use --repo YOUR_NAME/zilan-agent-kb to upload]")
        return

    if "/" not in args.repo:
        print("\nNOTE: repo should be YOUR_USERNAME/REPO_NAME")
        print(f"  Current: {args.repo}")
        user_input = input("  Enter your HF username + repo (e.g. ryan/zilan-agent-kb): ").strip()
        if user_input:
            args.repo = user_input
        else:
            print("Aborting.")
            return

    _upload_dataset(args.repo, agama_rows, kb_rows)


if __name__ == "__main__":
    main()
