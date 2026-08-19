from __future__ import annotations

from pathlib import Path

from zilanlib.validation import collation as collation_validation

ROOT = Path(__file__).resolve().parents[1]
ANCHOR_PROBES = ROOT / "tests" / "fixtures" / "collation" / "cbeta_anchor_probes.yaml"
PARALLEL_CANDIDATES = ROOT / "tests" / "fixtures" / "collation" / "high_value_no_self_parallel_candidates.yaml"


def test_manual_review_evidence_reader_rejects_a_directory(tmp_path: Path) -> None:
    evidence_directory = tmp_path / "docs" / "runtime-evidence" / "manual"
    evidence_directory.mkdir(parents=True)

    assert collation_validation._manual_review_evidence_text(
        tmp_path, {"evidence_file": "docs/runtime-evidence/manual"}
    ) is None


def test_collation_validator_accepts_checked_in_anchor_and_parallel_fixtures() -> None:
    failures: list[str] = []
    warnings: list[str] = []

    collation_validation.validate_collation_fixtures(ROOT, failures, warnings, strict_yaml=True)

    assert failures == []
    assert warnings == []


def test_manual_collation_candidate_preserves_limited_non_equivalence_boundary() -> None:
    import yaml

    data = yaml.safe_load(PARALLEL_CANDIDATES.read_text(encoding="utf-8"))
    candidate_set = data["candidate_sets"][0]
    parallel = candidate_set["candidate_parallels"][0]

    assert candidate_set["status"] == "manual_collation_reviewed"
    assert candidate_set["manual_review"]["conclusion"] == "limited_doctrinal_theme_parallel"
    assert candidate_set["manual_review"]["evidence_file"] == (
        "docs/runtime-evidence/2026-08-12-no-self-parallel-manual-collation.md"
    )
    assert parallel["confidence"] == "manual_limited_theme_parallel"
    assert parallel["collation_status"] == "manual_xml_p5_theme_parallel_reviewed"
    assert parallel["equivalence_claim"] is False
    assert parallel["publication_ready"] is False
    assert any("does not prove textual equivalence" in item for item in candidate_set["boundaries"])
    assert any("does not change runtime or platform validation status" in item for item in candidate_set["boundaries"])


def test_second_manual_collation_candidate_is_driven_by_srq04_expected_chunks() -> None:
    import yaml

    anchor_data = yaml.safe_load(ANCHOR_PROBES.read_text(encoding="utf-8"))
    probe_ids = {probe["probe_id"] for probe in anchor_data["anchor_probes"]}
    assert "cbeta-anchor:T01n0001:line-881" in probe_ids
    assert "cbeta-anchor:T01n0001:line-1829" in probe_ids

    data = yaml.safe_load(PARALLEL_CANDIDATES.read_text(encoding="utf-8"))
    candidate_sets = {item["set_id"]: item for item in data["candidate_sets"]}
    candidate_set = candidate_sets["long-agama-no-self-verse-and-aggregates"]
    parallel = candidate_set["candidate_parallels"][0]

    assert candidate_set["status"] == "manual_collation_reviewed"
    assert candidate_set["source_anchor_probe"] == "cbeta-anchor:T01n0001:line-881"
    assert candidate_set["source_chunk_id"] == "agama:T01n0001:juan-1:line-881"
    assert candidate_set["manual_review"]["evidence_file"] == (
        "docs/runtime-evidence/2026-08-12-long-agama-no-self-verse-manual-collation.md"
    )
    assert parallel["anchor_probe"] == "cbeta-anchor:T01n0001:line-1829"
    assert parallel["chunk_id"] == "agama:T01n0001:juan-3:line-1829"
    assert parallel["confidence"] == "manual_limited_theme_parallel"
    assert parallel["collation_status"] == "manual_xml_p5_theme_parallel_reviewed"
    assert parallel["equivalence_claim"] is False
    assert parallel["publication_ready"] is False
    assert "SRQ-04" in parallel["qualified_conclusion"]
    assert any("does not prove textual equivalence" in item for item in candidate_set["boundaries"])
    assert any("does not change runtime or platform validation status" in item for item in candidate_set["boundaries"])


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


def test_collation_validator_rejects_anchor_located_status_as_manual_collation(tmp_path: Path) -> None:
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
  - probe_id: cbeta-anchor:T01n0001:line-3997
    work_id: T01n0001
    source_file: context/agama/T0099-za-agama.md
    xml_file: context/agama/_source/T02n0099.xml
    line_range: {start: 1, end: 1}
    expected_start: {pb: 0002a, lb: 0002a03}
    expected_end: {pb: 0002a, lb: 0002a04}
""",
        encoding="utf-8",
    )
    evidence = tmp_path / "docs" / "runtime-evidence" / "manual.md"
    evidence.parent.mkdir(parents=True, exist_ok=True)
    evidence.write_text("# Manual note\n", encoding="utf-8")
    (fixtures / "high_value_no_self_parallel_candidates.yaml").write_text(
        """version: 1
source: test
candidate_sets:
  - set_id: no-self-five-aggregates
    theme: five_aggregates_no_self
    status: manual_collation_reviewed
    source_anchor_probe: cbeta-anchor:T02n0099:line-1
    source_chunk_id: agama:T02n0099:juan-1:line-1
    manual_review:
      date: "2026-08-12"
      evidence_file: docs/runtime-evidence/manual.md
      conclusion: limited_doctrinal_theme_parallel
      reviewer: local_manual_xml_p5_review
    candidate_parallels:
      - anchor_probe: cbeta-anchor:T01n0001:line-3997
        chunk_id: agama:T01n0001:juan-10:line-3997
        relation: doctrinal_theme_parallel
        confidence: manual_limited_theme_parallel
        collation_status: anchor_located_collation_pending
        equivalence_claim: false
        source_dependence_claim: false
        publication_ready: false
        qualified_conclusion: Anchor located only; this should not count as manual collation.
        rationale: Broken negative fixture.
    boundaries:
      - Manual review does not prove textual equivalence.
      - Manual review does not prove publication-level equivalence.
      - Manual review does not change runtime or platform validation status.
""",
        encoding="utf-8",
    )

    failures: list[str] = []
    warnings: list[str] = []

    collation_validation.validate_collation_fixtures(tmp_path, failures, warnings, strict_yaml=True)

    assert warnings == []
    assert any("anchor-located status cannot be used as manual collation" in failure for failure in failures)
    assert any(
        "manual_review.evidence_file must identify the source anchor and chunk" in failure
        for failure in failures
    )


def test_collation_validator_rejects_manual_review_without_source_dependence_boundary(tmp_path: Path) -> None:
    fixtures = tmp_path / "tests" / "fixtures" / "collation"
    fixtures.mkdir(parents=True)
    markdown = tmp_path / "context" / "agama" / "T0099-za-agama.md"
    markdown.parent.mkdir(parents=True, exist_ok=True)
    markdown.write_text("sample passage\n", encoding="utf-8")
    xml = tmp_path / "context" / "agama" / "_source" / "T02n0099.xml"
    xml.parent.mkdir(parents=True, exist_ok=True)
    xml.write_text(
        """<TEI xmlns="http://www.tei-c.org/ns/1.0" xml:id="T02n0099">
  <text><body><pb n="0002a" xml:id="T02.0099.0002a" ed="T"/>
  <lb n="0002a03" ed="T"/>sample <lb n="0002a04" ed="T"/>passage</body></text>
</TEI>
""",
        encoding="utf-8",
    )
    retrieval_fixtures = tmp_path / "tests" / "fixtures" / "retrieval_chunks"
    retrieval_fixtures.mkdir(parents=True)
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
  - probe_id: cbeta-anchor:T01n0001:line-3997
    work_id: T01n0001
    source_file: context/agama/T0099-za-agama.md
    xml_file: context/agama/_source/T02n0099.xml
    line_range: {start: 1, end: 1}
    expected_start: {pb: 0002a, lb: 0002a03}
    expected_end: {pb: 0002a, lb: 0002a04}
""",
        encoding="utf-8",
    )
    evidence = tmp_path / "docs" / "runtime-evidence" / "manual.md"
    evidence.parent.mkdir(parents=True)
    evidence.write_text(
        "cbeta-anchor:T02n0099:line-1 agama:T02n0099:juan-1:line-1 "
        "cbeta-anchor:T01n0001:line-3997 agama:T01n0001:juan-10:line-3997\n",
        encoding="utf-8",
    )
    (fixtures / "high_value_no_self_parallel_candidates.yaml").write_text(
        """version: 1
source: test
candidate_sets:
  - set_id: no-self-five-aggregates
    theme: five_aggregates_no_self
    status: manual_collation_reviewed
    source_anchor_probe: cbeta-anchor:T02n0099:line-1
    source_chunk_id: agama:T02n0099:juan-1:line-1
    manual_review:
      date: "2026-08-12"
      evidence_file: docs/runtime-evidence/manual.md
      conclusion: limited_doctrinal_theme_parallel
      reviewer: local_manual_xml_p5_review
    candidate_parallels:
      - anchor_probe: cbeta-anchor:T01n0001:line-3997
        chunk_id: agama:T01n0001:juan-10:line-3997
        relation: doctrinal_theme_parallel
        confidence: manual_limited_theme_parallel
        collation_status: manual_xml_p5_theme_parallel_reviewed
        equivalence_claim: false
        publication_ready: false
        qualified_conclusion: Limited theme relation only.
        rationale: Manual review.
    boundaries:
      - Manual review does not prove textual equivalence.
      - Manual review does not prove publication-level equivalence.
      - Manual review does not change runtime or platform validation status.
""",
        encoding="utf-8",
    )

    failures: list[str] = []
    warnings: list[str] = []

    collation_validation.validate_collation_fixtures(tmp_path, failures, warnings, strict_yaml=True)

    assert warnings == []
    assert any("source_dependence_claim must be false" in failure for failure in failures)
