import json
import subprocess
import sys
from pathlib import Path

from semantic_retrieval_dry_run import DEFAULT_FIXTURE, FixtureError
from semantic_role_coverage import build_role_coverage

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "semantic_role_coverage.py"


def test_role_coverage_reports_covered_and_missing_needs() -> None:
    result = build_role_coverage(DEFAULT_FIXTURE, query_id="SRQ-01")

    assert result["mode"] == "semantic-role-coverage"
    assert result["coverage_status"] == "partial"
    assert result["covered_needs"] == {
        "agama_evidence": [
            "agama:T02n0099:juan-1:line-147",
            "agama:T01n0001:juan-1:line-881",
            "agama:T01n0001:juan-3:line-1829",
        ],
        "hetuvidya": [
            "context:hetuvidya:trairupya",
            "reasoning:ZR-01:hetuvidya",
        ],
    }
    assert result["missing_needs"] == [
        "collected_topics",
        "madhyamaka_prasanga",
        "practice_boundary",
    ]
    assert result["extra_roles"] == []
    assert "Fixture-defined role coverage review only" in result["limitations"][0]
    assert "## Missing Needs" in result["review_text"]


def test_role_coverage_respects_chunk_limit_before_review() -> None:
    result = build_role_coverage(DEFAULT_FIXTURE, query_id="SRQ-01", limit=1)

    assert result["covered_needs"] == {
        "agama_evidence": ["agama:T02n0099:juan-1:line-147"],
    }
    assert result["missing_needs"] == [
        "collected_topics",
        "hetuvidya",
        "madhyamaka_prasanga",
        "practice_boundary",
    ]


def test_role_coverage_unknown_query_id_is_reported() -> None:
    try:
        build_role_coverage(DEFAULT_FIXTURE, query_id="SRQ-99")
    except FixtureError as exc:
        assert "Unknown query id: SRQ-99" in str(exc)
    else:
        raise AssertionError("unknown query id should fail")


def test_role_coverage_cli_json_output_is_machine_readable() -> None:
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--query-id", "SRQ-01", "--json"],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=True,
    )
    data = json.loads(result.stdout)

    assert data["mode"] == "semantic-role-coverage"
    assert data["query_id"] == "SRQ-01"
    assert data["coverage_status"] == "partial"
    assert data["missing_needs"] == ["collected_topics", "madhyamaka_prasanga", "practice_boundary"]
