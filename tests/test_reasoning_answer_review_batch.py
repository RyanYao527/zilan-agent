from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest
from zilanlib.reasoning.answer_review_batch import (
    MODE,
    BatchReviewError,
    build_reasoning_answer_review_batch,
)

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "reasoning_answer_review_batch.py"


def _write_batch(path: Path) -> None:
    path.write_text(
        """
version: 1
reviews:
  - id: agama-pass
    query_id: SRQ-04
    sample_id: srq04-agama-citation-boundary-pass
  - id: agama-fail
    query_id: SRQ-04
    sample_id: srq04-agama-citation-boundary-fail
  - id: hetuvidya-review-needed
    query_id: SRQ-05
""".strip()
        + "\n",
        encoding="utf-8",
    )


def test_reasoning_answer_review_batch_summarizes_mixed_statuses(tmp_path: Path) -> None:
    batch_path = tmp_path / "answer-review-batch.yaml"
    _write_batch(batch_path)

    result = build_reasoning_answer_review_batch(batch_path)

    assert result["mode"] == MODE
    assert result["output_schema"] == "reasoning-answer-review-batch-output-v0"
    assert result["overall_status"] == "fail"
    assert result["summary"] == {
        "total": 3,
        "pass": 1,
        "fail": 1,
        "review_needed": 1,
        "other": 0,
    }
    assert [item["id"] for item in result["reviews"]] == [
        "agama-pass",
        "agama-fail",
        "hetuvidya-review-needed",
    ]
    assert result["reviews"][0]["validator_families"][-1] == {
        "family": "agama_evidence",
        "status": "run",
        "case_ids": ["ZR-05"],
    }
    assert "agama_citation_boundary:CBETA" in result["reviews"][1]["missing_required_terms"]
    assert result["reviews"][2]["answer_source"] is None
    assert result["reviews"][2]["overall_status"] == "review_needed"
    assert "- agama-fail: fail" in result["review_text"]


def test_reasoning_answer_review_batch_rejects_missing_review_id(tmp_path: Path) -> None:
    batch_path = tmp_path / "invalid-batch.yaml"
    batch_path.write_text(
        """
version: 1
reviews:
  - query_id: SRQ-04
    sample_id: srq04-agama-citation-boundary-pass
""".strip()
        + "\n",
        encoding="utf-8",
    )

    with pytest.raises(BatchReviewError, match=r"reviews\[0\]\.id"):
        build_reasoning_answer_review_batch(batch_path)


def test_reasoning_answer_review_batch_cli_json_output_is_machine_readable(tmp_path: Path) -> None:
    batch_path = tmp_path / "answer-review-batch.yaml"
    _write_batch(batch_path)

    completed = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--batch",
            str(batch_path),
            "--json",
        ],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=True,
    )
    data = json.loads(completed.stdout)

    assert data["mode"] == MODE
    assert data["overall_status"] == "fail"
    assert data["summary"]["total"] == 3
    assert data["reviews"][0]["id"] == "agama-pass"
