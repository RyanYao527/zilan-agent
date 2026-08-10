from __future__ import annotations

from pathlib import Path

from zilanlib.validation import collation as collation_validation

ROOT = Path(__file__).resolve().parents[1]


def test_collation_validator_accepts_checked_in_anchor_and_parallel_fixtures() -> None:
    failures: list[str] = []
    warnings: list[str] = []

    collation_validation.validate_collation_fixtures(ROOT, failures, warnings, strict_yaml=True)

    assert failures == []
    assert warnings == []


def test_collation_validator_rejects_unknown_parallel_anchor_probe(tmp_path: Path) -> None:
    fixtures = tmp_path / "tests" / "fixtures" / "collation"
    fixtures.mkdir(parents=True)
    markdown = tmp_path / "context" / "agama" / "T0099-za-agama.md"
    markdown.parent.mkdir(parents=True, exist_ok=True)
    markdown.write_text("sample passage\n", encoding="utf-8")
    xml = tmp_path / "context" / "agama" / "_source" / "T02n0099.xml"
    xml.parent.mkdir(parents=True, exist_ok=True)
    xml.write_text(
        """<TEI xmlns="http://www.tei-c.org/ns/1.0" xml:id="T02n0099">
  <text>
    <body>
      <pb n="0002a" xml:id="T02.0099.0002a" ed="T"/>
      <lb n="0002a03" ed="T"/>sample <lb n="0002a04" ed="T"/>passage
    </body>
  </text>
</TEI>
""",
        encoding="utf-8",
    )
    retrieval_fixtures = tmp_path / "tests" / "fixtures" / "retrieval_chunks"
    retrieval_fixtures.mkdir(parents=True, exist_ok=True)
    (retrieval_fixtures / "semantic_chunks.yaml").write_text(
        """version: 1
chunks:
  - chunk_id: agama:T02n0099:juan-1:line-1
  - chunk_id: agama:T01n0001:juan-10:line-3997
""",
        encoding="utf-8",
    )
    (fixtures / "cbeta_anchor_probes.yaml").write_text(
        """version: 1
source: test
anchor_probes:
  - probe_id: cbeta-anchor:T02n0099:line-1
    work_id: T02n0099
    source_file: context/agama/T0099-za-agama.md
    xml_file: context/agama/_source/T02n0099.xml
    line_range: {start: 1, end: 1}
    expected_start: {pb: 0002a, lb: 0002a03}
    expected_end: {pb: 0002a, lb: 0002a04}
""",
        encoding="utf-8",
    )
    (fixtures / "high_value_no_self_parallel_candidates.yaml").write_text(
        """version: 1
source: test
candidate_sets:
  - set_id: no-self-five-aggregates
    theme: five_aggregates_no_self
    status: candidate_map_only
    source_anchor_probe: cbeta-anchor:T02n0099:line-1
    source_chunk_id: agama:T02n0099:juan-1:line-1
    candidate_parallels:
      - anchor_probe: cbeta-anchor:T01n0001:missing
        chunk_id: agama:T01n0001:juan-10:line-3997
        relation: doctrinal_theme_parallel
        confidence: review_candidate
        collation_status: pending_manual_collation
        rationale: Candidate only.
    boundaries:
      - Candidate map only; does not prove publication-level equivalence.
""",
        encoding="utf-8",
    )

    failures: list[str] = []
    warnings: list[str] = []

    collation_validation.validate_collation_fixtures(tmp_path, failures, warnings, strict_yaml=True)

    assert warnings == []
    assert failures == [
        "tests/fixtures/collation/high_value_no_self_parallel_candidates.yaml "
        "no-self-five-aggregates candidate cbeta-anchor:T01n0001:missing must reference a known anchor probe."
    ]
