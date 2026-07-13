import importlib
import json
import sys

import pytest


def test_search_agama_root_wrapper_reexports_library_api() -> None:
    import search_agama as wrapper
    from zilanlib.agama import search as library

    assert wrapper.search_agama is library.search_agama
    assert wrapper.search_agama_passages is library.search_agama_passages
    assert wrapper.iter_agama_markdown_files is library.iter_agama_markdown_files
    assert wrapper.AgamaMatch is library.AgamaMatch
    assert wrapper.AgamaPassage is library.AgamaPassage


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