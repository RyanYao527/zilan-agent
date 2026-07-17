import importlib
import json
import sys
from pathlib import Path

import pytest


def test_search_agama_root_wrapper_reexports_library_api() -> None:
    import search_agama as wrapper
    from zilanlib.agama import search as library

    assert wrapper.search_agama is library.search_agama
    assert wrapper.search_agama_passages is library.search_agama_passages
    assert wrapper.iter_agama_markdown_files is library.iter_agama_markdown_files
    assert wrapper.AgamaMatch is library.AgamaMatch
    assert wrapper.AgamaPassage is library.AgamaPassage


def test_reasoning_validator_output_root_wrapper_reexports_library_api() -> None:
    import reasoning_validator_output as wrapper
    from zilanlib.reasoning import validator_output as library

    assert wrapper.build_validator_output is library.build_validator_output
    assert wrapper.build_not_applicable_validator_output is library.build_not_applicable_validator_output
    assert wrapper.case_ids_from_items is library.case_ids_from_items


@pytest.mark.parametrize(
    ("module_name", "args", "expected_mode", "expected_query_id"),
    [
        (
            "semantic_retrieval_dry_run",
            ["--query-id", "SRQ-02", "--json"],
            "fixture-dry-run",
            "SRQ-02",
        ),
        (
            "semantic_context_bundle",
            ["--query-id", "SRQ-02", "--json"],
            "semantic-context-bundle",
            "SRQ-02",
        ),
        (
            "semantic_role_coverage",
            ["--query-id", "SRQ-02", "--json"],
            "semantic-role-coverage",
            "SRQ-02",
        ),
        (
            "semantic_answer_contract_review",
            ["--query-id", "SRQ-02", "--sample-id", "srq02-hetuvidya-error-pass", "--json"],
            "semantic-answer-contract-review",
            "SRQ-02",
        ),
        (
            "semantic_answer_boundary_review",
            ["--query-id", "SRQ-01", "--sample-id", "srq01-practice-boundary-pass", "--json"],
            "semantic-answer-boundary-review",
            "SRQ-01",
        ),
    ],
)
def test_semantic_root_cli_wrappers_run_json_in_process(
    module_name: str,
    args: list[str],
    expected_mode: str,
    expected_query_id: str,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    module = importlib.import_module(module_name)
    monkeypatch.setattr(sys, "argv", [f"{module_name}.py", *args])

    assert module.main() == 0
    captured = capsys.readouterr()
    data = json.loads(captured.out)

    assert data["mode"] == expected_mode
    assert data["query_id"] == expected_query_id

@pytest.mark.parametrize(
    ("module_name", "args", "expected_mode", "required_key"),
    [
        (
            "semantic_fixture_candidates",
            ["--terms", "\u975e\u6211", "--limit", "1", "--json"],
            "agama-fixture-candidates",
            "chunks",
        ),
        (
            "semantic_fixture_review",
            ["--terms", "\u975e\u6211", "--limit", "1", "--json"],
            "semantic-fixture-review",
            "summary",
        ),
    ],
)
def test_agama_fixture_root_cli_wrappers_run_json_in_process(
    module_name: str,
    args: list[str],
    expected_mode: str,
    required_key: str,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    module = importlib.import_module(module_name)
    monkeypatch.setattr(sys, "argv", [f"{module_name}.py", *args])

    assert module.main() == 0
    captured = capsys.readouterr()
    data = json.loads(captured.out)

    assert data["mode"] == expected_mode
    assert required_key in data

@pytest.mark.parametrize(
    ("module_name", "args", "expected_mode", "expected_case_ids"),
    [
        (
            "hetuvidya_validator",
            ["--case-id", "ZR-07", "--json"],
            "hetuvidya-validator-v0",
            ["ZR-07"],
        ),
        (
            "collected_topics_analyzer",
            ["--case-id", "ZR-02", "--json"],
            "collected-topics-analyzer-v0",
            ["ZR-02"],
        ),
        (
            "madhyamaka_critique_engine",
            ["--case-id", "ZR-09", "--json"],
            "madhyamaka-critique-engine-v0",
            ["ZR-09"],
        ),
        (
            "cognitive_analysis_mapper",
            ["--case-id", "ZR-10", "--json"],
            "cognitive-analysis-mapper-v0",
            ["ZR-10"],
        ),
        (
            "agama_evidence_checker",
            ["--case-id", "ZR-05", "--json"],
            "agama-evidence-checker-v0.1",
            ["ZR-05"],
        ),
    ],
)
def test_reasoning_root_cli_wrappers_run_json_in_process(
    module_name: str,
    args: list[str],
    expected_mode: str,
    expected_case_ids: list[str],
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    module = importlib.import_module(module_name)
    monkeypatch.setattr(sys, "argv", [f"{module_name}.py", *args])

    assert module.main() == 0
    captured = capsys.readouterr()
    data = json.loads(captured.out)

    assert data["mode"] == expected_mode
    assert data["case_ids"] == expected_case_ids


def test_reasoning_contract_runner_root_cli_wrapper_runs_json_in_process(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    import reasoning_contract_runner

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "reasoning_contract_runner.py",
            "--query-id",
            "SRQ-05",
            "--sample-id",
            "srq05-hetuvidya-non-pervasive-pass",
            "--json",
        ],
    )

    assert reasoning_contract_runner.main() == 0
    captured = capsys.readouterr()
    data = json.loads(captured.out)

    assert data["mode"] == "reasoning-contract-runner-v0"
    assert data["query_id"] == "SRQ-05"
    assert data["validators"]["hetuvidya"]["case_ids"] == ["ZR-07"]


def test_reasoning_answer_review_root_cli_wrapper_runs_json_in_process(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    import reasoning_answer_review

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "reasoning_answer_review.py",
            "--query-id",
            "SRQ-04",
            "--sample-id",
            "srq04-agama-citation-boundary-pass",
            "--json",
        ],
    )

    assert reasoning_answer_review.main() == 0
    captured = capsys.readouterr()
    data = json.loads(captured.out)

    assert data["mode"] == "reasoning-answer-review-v0"
    assert data["query_id"] == "SRQ-04"
    assert data["validator_summaries"][-1]["case_ids"] == ["ZR-05"]

def test_reasoning_answer_review_batch_root_cli_wrapper_runs_json_in_process(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    import reasoning_answer_review_batch

    batch_path = tmp_path / "answer-review-batch.yaml"
    batch_path.write_text(
        """
version: 1
reviews:
  - id: agama-pass
    query_id: SRQ-04
    sample_id: srq04-agama-citation-boundary-pass
""".strip()
        + "\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "reasoning_answer_review_batch.py",
            "--batch",
            str(batch_path),
            "--json",
        ],
    )

    assert reasoning_answer_review_batch.main() == 0
    captured = capsys.readouterr()
    data = json.loads(captured.out)

    assert data["mode"] == "reasoning-answer-review-batch-v0"
    assert data["overall_status"] == "pass"
    assert data["reviews"][0]["id"] == "agama-pass"
