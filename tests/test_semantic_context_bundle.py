import json
import subprocess
import sys
from pathlib import Path

from semantic_context_bundle import build_context_bundle
from semantic_retrieval_dry_run import DEFAULT_FIXTURE, FixtureError

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "semantic_context_bundle.py"


def test_context_bundle_preserves_fixture_order_and_citations() -> None:
    result = build_context_bundle(DEFAULT_FIXTURE, query_id="SRQ-01")

    assert result["mode"] == "semantic-context-bundle"
    assert result["chunk_ids"] == [
        "agama:T02n0099:juan-1:line-147",
        "agama:T01n0001:juan-1:line-881",
        "agama:T01n0001:juan-3:line-1829",
        "context:hetuvidya:trairupya",
        "reasoning:ZR-01:hetuvidya",
        "context:collected-topics:prasanga-runtime",
        "context:madhyamaka:prasanga-method",
    ]
    assert [chunk["chunk_id"] for chunk in result["chunks"]] == result["chunk_ids"]
    assert result["non_chunk_needs"] == ["practice_boundary"]
    assert "Non-chunk needs: practice_boundary" in result["bundle_text"]
    assert all(chunk["citation"] for chunk in result["chunks"])
    assert all(chunk["source_file"] for chunk in result["chunks"])
    assert result["bundle_text"].index("agama:T02n0099:juan-1:line-147") < result["bundle_text"].index(
        "context:hetuvidya:trairupya"
    )
    assert "Fixture-defined context bundle only" in result["limitations"][0]


def test_context_bundle_can_limit_chunks() -> None:
    result = build_context_bundle(DEFAULT_FIXTURE, query_id="SRQ-01", limit=2)

    assert result["chunk_ids"] == [
        "agama:T02n0099:juan-1:line-147",
        "agama:T01n0001:juan-1:line-881",
    ]
    assert len(result["chunks"]) == 2
    assert "agama:T01n0001:juan-3:line-1829" not in result["bundle_text"]


def test_context_bundle_unknown_query_id_is_reported() -> None:
    try:
        build_context_bundle(DEFAULT_FIXTURE, query_id="SRQ-99")
    except FixtureError as exc:
        assert "Unknown query id: SRQ-99" in str(exc)
    else:
        raise AssertionError("unknown query id should fail")


def test_context_bundle_cli_json_output_is_machine_readable() -> None:
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--query-id", "SRQ-01", "--json"],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=True,
    )
    data = json.loads(result.stdout)

    assert data["mode"] == "semantic-context-bundle"
    assert data["query_id"] == "SRQ-01"
    assert len(data["chunks"]) == 7
    assert "# Semantic Retrieval Context Bundle" in data["bundle_text"]
