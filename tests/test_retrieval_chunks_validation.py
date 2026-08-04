from __future__ import annotations

from pathlib import Path

from zilanlib.validation.retrieval_chunks import validate_retrieval_chunks


def _write_retrieval_repo(tmp_path: Path, body: str) -> None:
    docs = tmp_path / "docs" / "architecture"
    docs.mkdir(parents=True)
    (docs / "semantic-retrieval-interface.md").write_text("# Semantic Retrieval\n", encoding="utf-8")

    context = tmp_path / "context"
    context.mkdir()
    (context / "sample.md").write_text("line one\nline two\nline three\n", encoding="utf-8")

    answers = tmp_path / "tests" / "fixtures" / "answers"
    answers.mkdir(parents=True)
    (answers / "pass.md").write_text("sample answer\n", encoding="utf-8")
    (answers / "fail.md").write_text("sample failing answer\n", encoding="utf-8")

    fixtures = tmp_path / "tests" / "fixtures" / "retrieval_chunks"
    fixtures.mkdir(parents=True)
    (fixtures / "semantic_chunks.yaml").write_text(body, encoding="utf-8")


def _valid_context_chunk(chunk_id: str = "chunk-1") -> str:
    return f"""  - chunk_id: {chunk_id}
    chunk_type: context_topic
    source_file: context/sample.md
    start_line: 1
    end_line: 1
    citation: "context/sample.md:1"
    passage_citation: "context/sample.md:1"
    text: "line one"
    metadata:
      topics:
        - sample
      reasoning_roles:
        - hetuvidya
"""


def _valid_query(query_id: str = "SRQ-01", chunk_id: str = "chunk-1") -> str:
    return f"""  - id: {query_id}
    query: "sample query"
    needs:
      - hetuvidya
    keywords:
      classical:
        - sample
      modern:
        - sample
    expected_sources:
      - context/sample.md
    expected_chunk_ids:
      - {chunk_id}
"""


def _retrieval_fixture(chunks: str, queries: str) -> str:
    return f"""version: 1
source: docs/architecture/semantic-retrieval-interface.md
purpose: Test retrieval chunks.
chunks:
{chunks}queries:
{queries}"""


def test_retrieval_chunks_accept_minimal_valid_context_fixture(tmp_path: Path) -> None:
    _write_retrieval_repo(
        tmp_path,
        _retrieval_fixture(_valid_context_chunk(), _valid_query()),
    )
    failures: list[str] = []
    warnings: list[str] = []

    validate_retrieval_chunks(tmp_path, failures, warnings, strict_yaml=True)

    assert warnings == []
    assert failures == []


def test_retrieval_chunks_report_duplicate_chunk_query_and_sample_ids(tmp_path: Path) -> None:
    query = """  - id: SRQ-01
    query: "sample query"
    needs:
      - hetuvidya
    answer_contracts:
      sample_contract:
        description: Sample contract.
        required_terms:
          - sample
    answer_contract_samples:
      - id: duplicate-sample
        file: tests/fixtures/answers/pass.md
        expected_status: pass
      - id: duplicate-sample
        file: tests/fixtures/answers/fail.md
        expected_status: fail
    keywords:
      classical:
        - sample
      modern:
        - sample
    expected_sources:
      - context/sample.md
    expected_chunk_ids:
      - chunk-1
  - id: SRQ-01
    query: "duplicate query"
    needs:
      - hetuvidya
    keywords:
      classical:
        - sample
      modern:
        - sample
    expected_sources:
      - context/sample.md
    expected_chunk_ids:
      - chunk-1
"""
    _write_retrieval_repo(
        tmp_path,
        _retrieval_fixture(_valid_context_chunk("chunk-1") + _valid_context_chunk("chunk-1"), query),
    )
    failures: list[str] = []
    warnings: list[str] = []

    validate_retrieval_chunks(tmp_path, failures, warnings, strict_yaml=True)

    assert warnings == []
    assert "tests/fixtures/retrieval_chunks/semantic_chunks.yaml contains duplicate chunk id: chunk-1" in failures
    assert "tests/fixtures/retrieval_chunks/semantic_chunks.yaml contains duplicate query id: SRQ-01" in failures
    assert (
        "tests/fixtures/retrieval_chunks/semantic_chunks.yaml SRQ-01 contains duplicate "
        "answer_contract_samples id: duplicate-sample"
    ) in failures


def test_retrieval_chunks_reject_answer_sample_paths_outside_repo_root(tmp_path: Path) -> None:
    query = """  - id: SRQ-01
    query: "sample query"
    needs:
      - hetuvidya
    answer_contracts:
      sample_contract:
        description: Sample contract.
        required_terms:
          - sample
    answer_contract_samples:
      - id: outside-root
        file: ../outside-answer.md
        expected_status: pass
    keywords:
      classical:
        - sample
      modern:
        - sample
    expected_sources:
      - context/sample.md
    expected_chunk_ids:
      - chunk-1
"""
    _write_retrieval_repo(
        tmp_path,
        _retrieval_fixture(_valid_context_chunk(), query),
    )
    failures: list[str] = []
    warnings: list[str] = []

    validate_retrieval_chunks(tmp_path, failures, warnings, strict_yaml=True)

    assert warnings == []
    assert any("answer_contract_samples outside-root file must stay under repo root" in failure for failure in failures)
