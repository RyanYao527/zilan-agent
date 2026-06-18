import json
import subprocess
import sys
from pathlib import Path

from semantic_retrieval_dry_run import DEFAULT_FIXTURE, FixtureError, build_dry_run

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "semantic_retrieval_dry_run.py"


def test_dry_run_returns_expected_chunks_for_query_fixture() -> None:
    result = build_dry_run(DEFAULT_FIXTURE, query_id="SRQ-01")

    assert result["mode"] == "fixture-dry-run"
    assert result["query_id"] == "SRQ-01"
    assert result["expected_chunk_ids"] == [
        "agama:T02n0099:juan-1:line-147",
        "agama:T01n0001:juan-1:line-881",
        "agama:T01n0001:juan-3:line-1829",
        "context:hetuvidya:trairupya",
        "reasoning:ZR-01:hetuvidya",
        "context:collected-topics:prasanga-runtime",
        "context:madhyamaka:prasanga-method",
    ]
    assert [chunk["chunk_id"] for chunk in result["chunks"]] == result["expected_chunk_ids"]
    assert result["non_chunk_needs"] == ["practice_boundary"]
    assert result["answer_boundary_contracts"]["practice_boundary"]["required_terms"] == ["边界", "不等于修证"]
    assert all("source_file" in chunk for chunk in result["chunks"])
    assert all("citation" in chunk for chunk in result["chunks"])
    assert any("no embeddings" in item for item in result["limitations"])


def test_dry_run_can_limit_expected_chunks() -> None:
    result = build_dry_run(DEFAULT_FIXTURE, query_id="SRQ-01", limit=1)

    assert result["expected_chunk_ids"] == ["agama:T02n0099:juan-1:line-147"]
    assert len(result["chunks"]) == 1


def test_dry_run_unknown_query_id_is_reported() -> None:
    try:
        build_dry_run(DEFAULT_FIXTURE, query_id="SRQ-99")
    except FixtureError as exc:
        assert "Unknown query id: SRQ-99" in str(exc)
    else:
        raise AssertionError("unknown query id should fail")


def test_dry_run_rejects_unknown_chunk_references(tmp_path: Path) -> None:
    fixture = tmp_path / "semantic_chunks.yaml"
    fixture.write_text(
        """version: 1
source: test
purpose: test
chunks:
  - chunk_id: chunk-1
    chunk_type: context_topic
    source_file: context/sample.md
    start_line: 1
    end_line: 1
    citation: "context/sample.md:1"
    passage_citation: "context/sample.md:1"
    text: sample
    metadata:
      topics:
        - sample
      reasoning_roles:
        - hetuvidya
queries:
  - id: SRQ-01
    query: sample
    expected_chunk_ids:
      - missing-chunk
""",
        encoding="utf-8",
    )

    try:
        build_dry_run(fixture, query_id="SRQ-01")
    except FixtureError as exc:
        assert "references unknown chunks" in str(exc)
    else:
        raise AssertionError("unknown chunk references should fail")


def test_dry_run_cli_json_output_is_machine_readable() -> None:
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--query-id", "SRQ-01", "--json"],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=True,
    )
    data = json.loads(result.stdout)

    assert data["mode"] == "fixture-dry-run"
    assert data["query_id"] == "SRQ-01"
    assert len(data["chunks"]) == 7
