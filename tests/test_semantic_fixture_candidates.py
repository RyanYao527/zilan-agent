import json
import subprocess
import sys
from pathlib import Path

from zilanlib.agama.candidates import CandidateError, build_candidate_set

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "semantic_fixture_candidates.py"


def test_candidate_builder_preserves_agama_citation_fields() -> None:
    result = build_candidate_set(root=ROOT, terms="\u975e\u6211", limit=2)

    assert result["mode"] == "agama-fixture-candidates"
    assert result["source_script"] == "scripts/search_agama.py"
    assert result["chunks"]
    for chunk in result["chunks"]:
        assert chunk["chunk_type"] == "agama_passage"
        assert chunk["source_file"].startswith("context/agama/")
        assert f"{chunk['source_file']}:{chunk['start_line']}" in chunk["passage_citation"]
        assert chunk["source_file"] in chunk["citation"]
        assert chunk["text"]
        assert chunk["metadata"]["reasoning_roles"] == ["agama_evidence"]
        assert chunk["metadata"]["matched_lines"]
        assert chunk["metadata"]["source_hash"].startswith("sha256:")
        assert chunk["metadata"]["line_text_hash"] == chunk["metadata"]["source_hash"]
        provenance = chunk["metadata"]["provenance"]
        assert provenance["source_script"] == "scripts/search_agama.py"
        assert provenance["source_file"] == chunk["source_file"]
        assert provenance["line_range"] == {"start": chunk["start_line"], "end": chunk["end_line"]}
        assert provenance["matched_lines"] == chunk["metadata"]["matched_lines"]
        assert provenance["hash_algorithm"] == "sha256"
        assert provenance["line_text_hash"] == chunk["metadata"]["line_text_hash"]
        assert provenance["source_hash_scope"] == "legacy_alias_for_line_text_hash"


def test_candidate_builder_deduplicates_passage_chunks() -> None:
    result = build_candidate_set(root=ROOT, terms="\u7121\u5e38|\u975e\u6211", limit=5)
    keys = {
        (chunk["source_file"], chunk["start_line"], chunk["end_line"])
        for chunk in result["chunks"]
    }

    assert len(keys) == len(result["chunks"])
    for chunk in result["chunks"]:
        assert chunk["metadata"]["provenance"]["matched_lines"] == chunk["metadata"]["matched_lines"]


def test_candidate_builder_rejects_negative_limit() -> None:
    try:
        build_candidate_set(root=ROOT, terms="\u975e\u6211", limit=-1)
    except CandidateError as exc:
        assert "--limit must be zero or greater" in str(exc)
    else:
        raise AssertionError("negative limit should fail")


def test_candidate_cli_json_output_is_machine_readable() -> None:
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--terms", "\u975e\u6211", "--limit", "1", "--json"],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=True,
    )
    data = json.loads(result.stdout)

    assert data["mode"] == "agama-fixture-candidates"
    assert len(data["chunks"]) == 1
    assert "citation" in data["chunks"][0]
    assert "passage_citation" in data["chunks"][0]
    assert data["chunks"][0]["metadata"]["line_text_hash"].startswith("sha256:")
    assert data["chunks"][0]["metadata"]["provenance"]["hash_algorithm"] == "sha256"
