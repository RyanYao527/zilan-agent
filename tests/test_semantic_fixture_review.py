import json
import subprocess
import sys
from pathlib import Path

from semantic_fixture_candidates import build_candidate_set
from semantic_fixture_review import ReviewError, build_review

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "semantic_fixture_review.py"


def _write_fixture(path: Path, chunks: list[dict]) -> None:
    import yaml

    path.write_text(
        yaml.safe_dump(
            {
                "version": 1,
                "source": "test",
                "purpose": "test",
                "chunks": chunks,
                "queries": [],
            },
            allow_unicode=True,
            sort_keys=False,
        ),
        encoding="utf-8",
    )


def test_review_separates_existing_and_new_candidates(tmp_path: Path) -> None:
    candidates = build_candidate_set(root=ROOT, terms="\u975e\u6211", limit=2)["chunks"]
    fixture_path = tmp_path / "semantic_chunks.yaml"
    _write_fixture(fixture_path, [candidates[0]])

    result = build_review(root=ROOT, fixture_path=fixture_path, terms="\u975e\u6211", limit=2)

    assert result["mode"] == "semantic-fixture-review"
    assert result["summary"]["candidate_chunks"] == 2
    assert result["summary"]["already_present"] == 1
    assert result["summary"]["new_candidates"] == 1
    assert result["already_present"][0]["chunk_id"] == candidates[0]["chunk_id"]
    assert result["new_candidates"][0]["chunk_id"] == candidates[1]["chunk_id"]


def test_review_detects_range_match_with_different_chunk_id(tmp_path: Path) -> None:
    candidate = build_candidate_set(root=ROOT, terms="\u975e\u6211", limit=1)["chunks"][0]
    fixture_chunk = dict(candidate)
    fixture_chunk["chunk_id"] = "agama:custom-id"
    fixture_path = tmp_path / "semantic_chunks.yaml"
    _write_fixture(fixture_path, [fixture_chunk])

    result = build_review(root=ROOT, fixture_path=fixture_path, terms="\u975e\u6211", limit=1)

    assert result["summary"]["already_present"] == 0
    assert result["summary"]["range_matches"] == 1
    assert result["range_matches"][0]["chunk_id"] == candidate["chunk_id"]


def test_review_missing_fixture_is_reported(tmp_path: Path) -> None:
    try:
        build_review(root=ROOT, fixture_path=tmp_path / "missing.yaml", terms="\u975e\u6211", limit=1)
    except ReviewError as exc:
        assert "Fixture not found" in str(exc)
    else:
        raise AssertionError("missing fixture should fail")


def test_review_cli_json_output_is_machine_readable() -> None:
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--terms", "\u975e\u6211", "--limit", "1", "--json"],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=True,
    )
    data = json.loads(result.stdout)

    assert data["mode"] == "semantic-fixture-review"
    assert "summary" in data
    assert "new_candidates" in data
    assert data["limitations"]
