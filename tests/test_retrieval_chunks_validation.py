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
    (context / "agama-sample.md").write_text("（一）Sample Section\nline one\nline two\n", encoding="utf-8")
    (context / "agama-unsectioned.md").write_text("line one\nline two\n", encoding="utf-8")

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


def _valid_agama_chunk(*, extra_metadata: str = '      section_label: "（一）Sample Section"\n') -> str:
    return f"""  - chunk_id: agama:sample
    chunk_type: agama_passage
    source_file: context/agama-sample.md
    start_line: 2
    end_line: 2
    citation: "Sample (T02n0099) 卷 1 （一）Sample Section, context/agama-sample.md:2"
    passage_citation: "Sample (T02n0099) 卷 1 （一）Sample Section, context/agama-sample.md:2"
    text: "line one"
    metadata:
      collection: "Sample"
      cbeta_id: T02n0099
      juan: "卷 1"
      section_marker: "（一）"
      section_title: "Sample Section"
{extra_metadata}      topics:
        - sample
      reasoning_roles:
        - agama_evidence
      matched_lines:
        - 2
      source_hash: "sha256:d9e83a19744a1a2a0408d877dbda4265b1a356913361f4403b5647df33e59d04"
      line_text_hash: "sha256:d9e83a19744a1a2a0408d877dbda4265b1a356913361f4403b5647df33e59d04"
      provenance:
        source_script: scripts/search_agama.py
        source_file: context/agama-sample.md
        line_range:
          start: 2
          end: 2
        matched_lines:
          - 2
        hash_algorithm: sha256
        line_text_hash: "sha256:d9e83a19744a1a2a0408d877dbda4265b1a356913361f4403b5647df33e59d04"
        source_hash_scope: legacy_alias_for_line_text_hash
        line_text_hash_scope: trimmed_non_empty_lines_joined_with_lf
"""


def _valid_unsectioned_agama_chunk(*, extra_metadata: str = "      section_label_status: source_unavailable\n") -> str:
    return f"""  - chunk_id: agama:unsectioned
    chunk_type: agama_passage
    source_file: context/agama-unsectioned.md
    start_line: 1
    end_line: 1
    citation: "Sample (T02n0099) 卷 1, context/agama-unsectioned.md:1"
    passage_citation: "Sample (T02n0099) 卷 1, context/agama-unsectioned.md:1"
    text: "line one"
    metadata:
      collection: "Sample"
      cbeta_id: T02n0099
      juan: "卷 1"
      section_marker:
      section_title:
      section_label:
{extra_metadata}      topics:
        - sample
      reasoning_roles:
        - agama_evidence
      matched_lines:
        - 1
      source_hash: "sha256:d9e83a19744a1a2a0408d877dbda4265b1a356913361f4403b5647df33e59d04"
      line_text_hash: "sha256:d9e83a19744a1a2a0408d877dbda4265b1a356913361f4403b5647df33e59d04"
      provenance:
        source_script: scripts/search_agama.py
        source_file: context/agama-unsectioned.md
        line_range:
          start: 1
          end: 1
        matched_lines:
          - 1
        hash_algorithm: sha256
        line_text_hash: "sha256:d9e83a19744a1a2a0408d877dbda4265b1a356913361f4403b5647df33e59d04"
        source_hash_scope: legacy_alias_for_line_text_hash
        line_text_hash_scope: trimmed_non_empty_lines_joined_with_lf
"""


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


def test_retrieval_chunks_require_agama_section_label_metadata(tmp_path: Path) -> None:
    _write_retrieval_repo(
        tmp_path,
        _retrieval_fixture(_valid_agama_chunk(extra_metadata=""), _valid_query(chunk_id="agama:sample")),
    )
    failures: list[str] = []
    warnings: list[str] = []

    validate_retrieval_chunks(tmp_path, failures, warnings, strict_yaml=True)

    assert warnings == []
    assert (
        "tests/fixtures/retrieval_chunks/semantic_chunks.yaml agama:sample "
        "metadata.section_label must match section_marker and section_title."
    ) in failures


def test_retrieval_chunks_report_agama_section_label_drift(tmp_path: Path) -> None:
    _write_retrieval_repo(
        tmp_path,
        _retrieval_fixture(
            _valid_agama_chunk(extra_metadata='      section_label: "Fixture Drift"\n'),
            _valid_query(chunk_id="agama:sample"),
        ),
    )
    failures: list[str] = []
    warnings: list[str] = []

    validate_retrieval_chunks(tmp_path, failures, warnings, strict_yaml=True)

    assert warnings == []
    assert (
        "tests/fixtures/retrieval_chunks/semantic_chunks.yaml agama:sample "
        "metadata.section_label must match section_marker and section_title."
    ) in failures


def test_retrieval_chunks_allow_source_unavailable_section_label_status(tmp_path: Path) -> None:
    _write_retrieval_repo(
        tmp_path,
        _retrieval_fixture(_valid_unsectioned_agama_chunk(), _valid_query(chunk_id="agama:unsectioned")),
    )
    failures: list[str] = []
    warnings: list[str] = []

    validate_retrieval_chunks(tmp_path, failures, warnings, strict_yaml=True)

    assert warnings == []
    assert failures == []


def test_retrieval_chunks_require_source_unavailable_status_when_source_has_no_section(tmp_path: Path) -> None:
    _write_retrieval_repo(
        tmp_path,
        _retrieval_fixture(
            _valid_unsectioned_agama_chunk(extra_metadata=""),
            _valid_query(chunk_id="agama:unsectioned"),
        ),
    )
    failures: list[str] = []
    warnings: list[str] = []

    validate_retrieval_chunks(tmp_path, failures, warnings, strict_yaml=True)

    assert warnings == []
    assert (
        "tests/fixtures/retrieval_chunks/semantic_chunks.yaml agama:unsectioned "
        "metadata.section_label_status must be source_unavailable when source has no section label."
    ) in failures


def test_retrieval_chunks_require_agama_citations_to_include_section_label(tmp_path: Path) -> None:
    chunk = _valid_agama_chunk().replace(" （一）Sample Section", "")
    _write_retrieval_repo(
        tmp_path,
        _retrieval_fixture(chunk, _valid_query(chunk_id="agama:sample")),
    )
    failures: list[str] = []
    warnings: list[str] = []

    validate_retrieval_chunks(tmp_path, failures, warnings, strict_yaml=True)

    assert warnings == []
    assert (
        "tests/fixtures/retrieval_chunks/semantic_chunks.yaml agama:sample "
        "citation must include metadata.section_label."
    ) in failures
    assert (
        "tests/fixtures/retrieval_chunks/semantic_chunks.yaml agama:sample "
        "passage_citation must include metadata.section_label."
    ) in failures
