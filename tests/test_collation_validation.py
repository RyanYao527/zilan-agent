from __future__ import annotations

from pathlib import Path

from zilanlib.validation import collation as collation_validation

ROOT = Path(__file__).resolve().parents[1]


def _write_minimal_collation_tree(
    root: Path,
    candidate_fixture: str,
    *,
    include_candidate_probe: bool = True,
    evidence_files: dict[str, str] | None = None,
) -> None:
    fixtures = root / "tests" / "fixtures" / "collation"
    fixtures.mkdir(parents=True)
    markdown = root / "context" / "agama" / "T0099-za-agama.md"
    markdown.parent.mkdir(parents=True, exist_ok=True)
    markdown.write_text("source passage\n", encoding="utf-8")
    xml = root / "context" / "agama" / "_source" / "T02n0099.xml"
    xml.parent.mkdir(parents=True, exist_ok=True)
    xml.write_text(
        """<TEI xmlns="http://www.tei-c.org/ns/1.0" xml:id="T02n0099">
  <text>
    <body>
      <pb n="0002a" xml:id="T02.0099.0002a" ed="T"/>
      <lb n="0002a03" ed="T"/>source <lb n="0002a04" ed="T"/>passage
    </body>
  </text>
</TEI>
""",
        encoding="utf-8",
    )
    retrieval_fixtures = root / "tests" / "fixtures" / "retrieval_chunks"
    retrieval_fixtures.mkdir(parents=True, exist_ok=True)
    (retrieval_fixtures / "semantic_chunks.yaml").write_text(
        """version: 1
chunks:
  - chunk_id: agama:T02n0099:juan-1:line-1
  - chunk_id: agama:T01n0001:juan-10:line-1
""",
        encoding="utf-8",
    )
    anchor_probe_fixture = """version: 1
source: test
anchor_probes:
  - probe_id: cbeta-anchor:T02n0099:line-1
    work_id: T02n0099
    source_file: context/agama/T0099-za-agama.md
    xml_file: context/agama/_source/T02n0099.xml
    line_range: {start: 1, end: 1}
    expected_start: {pb: 0002a, lb: 0002a03}
    expected_end: {pb: 0002a, lb: 0002a04}
"""
    if include_candidate_probe:
        candidate_markdown = root / "context" / "agama" / "T0001-chang-agama.md"
        candidate_markdown.write_text("candidate passage\n", encoding="utf-8")
        candidate_xml = root / "context" / "agama" / "_source" / "T01n0001.xml"
        candidate_xml.write_text(
            """<TEI xmlns="http://www.tei-c.org/ns/1.0" xml:id="T01n0001">
  <text>
    <body>
      <pb n="0061c" xml:id="T01.0001.0061c" ed="T"/>
      <lb n="0061c06" ed="T"/>candidate <lb n="0061c07" ed="T"/>passage
    </body>
  </text>
</TEI>
""",
            encoding="utf-8",
        )
        anchor_probe_fixture += """  - probe_id: cbeta-anchor:T01n0001:line-1
    work_id: T01n0001
    source_file: context/agama/T0001-chang-agama.md
    xml_file: context/agama/_source/T01n0001.xml
    line_range: {start: 1, end: 1}
    expected_start: {pb: 0061c, lb: 0061c06}
    expected_end: {pb: 0061c, lb: 0061c07}
"""
    (fixtures / "cbeta_anchor_probes.yaml").write_text(anchor_probe_fixture, encoding="utf-8")
    (fixtures / "high_value_no_self_parallel_candidates.yaml").write_text(candidate_fixture, encoding="utf-8")
    for relative_path, content in (evidence_files or {}).items():
        evidence_path = root / relative_path
        evidence_path.parent.mkdir(parents=True, exist_ok=True)
        evidence_path.write_text(content, encoding="utf-8")


def test_collation_validator_accepts_checked_in_anchor_and_parallel_fixtures() -> None:
    failures: list[str] = []
    warnings: list[str] = []

    collation_validation.validate_collation_fixtures(ROOT, failures, warnings, strict_yaml=True)

    assert failures == []
    assert warnings == []


def test_collation_validator_rejects_unknown_parallel_anchor_probe(tmp_path: Path) -> None:
    _write_minimal_collation_tree(
        tmp_path,
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
        chunk_id: agama:T01n0001:juan-10:line-1
        relation: doctrinal_theme_parallel
        confidence: review_candidate
        collation_status: pending_manual_collation
        rationale: Candidate only.
    boundaries:
      - Candidate map only; does not prove publication-level equivalence.
""",
        include_candidate_probe=False,
    )

    failures: list[str] = []
    warnings: list[str] = []

    collation_validation.validate_collation_fixtures(tmp_path, failures, warnings, strict_yaml=True)

    assert warnings == []
    assert failures == [
        "tests/fixtures/collation/high_value_no_self_parallel_candidates.yaml "
        "no-self-five-aggregates candidate cbeta-anchor:T01n0001:missing must reference a known anchor probe."
    ]


def test_collation_validator_requires_existing_manual_collation_evidence(tmp_path: Path) -> None:
    _write_minimal_collation_tree(
        tmp_path,
        """version: 1
source: test
candidate_sets:
  - set_id: no-self-five-aggregates
    theme: five_aggregates_no_self
    status: manual_theme_collation_recorded
    manual_collation_evidence: docs/runtime-evidence/missing-manual-collation.md
    source_anchor_probe: cbeta-anchor:T02n0099:line-1
    source_chunk_id: agama:T02n0099:juan-1:line-1
    candidate_parallels:
      - anchor_probe: cbeta-anchor:T01n0001:line-1
        chunk_id: agama:T01n0001:juan-10:line-1
        relation: doctrinal_theme_parallel
        confidence: review_candidate
        collation_status: manual_theme_collation_recorded
        manual_collation_evidence: docs/runtime-evidence/missing-manual-collation.md
        rationale: Manual theme-level collation was recorded.
    boundaries:
      - Manual evidence records a doctrinal-theme parallel only; it does not prove publication-level equivalence.
""",
    )

    failures: list[str] = []
    warnings: list[str] = []

    collation_validation.validate_collation_fixtures(tmp_path, failures, warnings, strict_yaml=True)

    assert warnings == []
    assert failures == [
        "tests/fixtures/collation/high_value_no_self_parallel_candidates.yaml "
        "no-self-five-aggregates manual_collation_evidence must reference an existing "
        "docs/runtime-evidence Markdown file.",
        "tests/fixtures/collation/high_value_no_self_parallel_candidates.yaml "
        "no-self-five-aggregates candidate cbeta-anchor:T01n0001:line-1 manual_collation_evidence "
        "must reference an existing docs/runtime-evidence Markdown file.",
    ]


def test_collation_validator_requires_manual_evidence_to_mention_candidate_anchor(tmp_path: Path) -> None:
    evidence_path = "docs/runtime-evidence/manual-collation.md"
    _write_minimal_collation_tree(
        tmp_path,
        f"""version: 1
source: test
candidate_sets:
  - set_id: no-self-five-aggregates
    theme: five_aggregates_no_self
    status: manual_theme_collation_recorded
    manual_collation_evidence: {evidence_path}
    source_anchor_probe: cbeta-anchor:T02n0099:line-1
    source_chunk_id: agama:T02n0099:juan-1:line-1
    candidate_parallels:
      - anchor_probe: cbeta-anchor:T01n0001:line-1
        chunk_id: agama:T01n0001:juan-10:line-1
        relation: doctrinal_theme_parallel
        confidence: review_candidate
        collation_status: manual_theme_collation_recorded
        manual_collation_evidence: {evidence_path}
        rationale: Manual theme-level collation was recorded.
    boundaries:
      - Manual evidence records a doctrinal-theme parallel only; it does not prove publication-level equivalence.
""",
        evidence_files={
            evidence_path: "no-self-five-aggregates\ncbeta-anchor:T02n0099:line-1\n",
        },
    )

    failures: list[str] = []
    warnings: list[str] = []

    collation_validation.validate_collation_fixtures(tmp_path, failures, warnings, strict_yaml=True)

    assert warnings == []
    assert failures == [
        "tests/fixtures/collation/high_value_no_self_parallel_candidates.yaml "
        "no-self-five-aggregates candidate cbeta-anchor:T01n0001:line-1 manual_collation_evidence "
        "must mention: cbeta-anchor:T01n0001:line-1."
    ]
