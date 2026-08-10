from __future__ import annotations

from pathlib import Path

from zilanlib.validation.reasoning_cases import validate_reasoning_cases


def _write_reasoning_case_repo(tmp_path: Path, body: str) -> None:
    docs = tmp_path / "docs" / "architecture"
    docs.mkdir(parents=True)
    (docs / "reasoning-contract.md").write_text("# Reasoning Contract\n", encoding="utf-8")

    context = tmp_path / "context"
    context.mkdir()
    (context / "reasoning-reference.md").write_text("# Reasoning Reference\n", encoding="utf-8")

    tests = tmp_path / "tests"
    tests.mkdir()
    (tests / "reasoning_cases.yaml").write_text(body, encoding="utf-8")


def _valid_hetuvidya_case(case_id: str, title: str) -> str:
    return f"""  - id: {case_id}
    title: {title}
    prompt: "Classify this argument."
    contracts:
      - hetuvidya
    reference_files:
      - context/reasoning-reference.md
    expected:
      boundary_statement: true
      structure:
        - claim
      hetuvidya:
        subject: sound
        predicate: impermanent
        reason: produced
        result: positive_reason
        checks:
          paksa_dharmata: pass
          sapaksa_sattva: pass
          vipaksa_asattva: pass
"""


def _reasoning_fixture(cases: str) -> str:
    return f"""version: 1
source: docs/architecture/reasoning-contract.md
purpose: Test reasoning fixtures.
cases:
{cases}"""


def test_reasoning_cases_accept_minimal_valid_hetuvidya_case(tmp_path: Path) -> None:
    _write_reasoning_case_repo(
        tmp_path,
        _reasoning_fixture(_valid_hetuvidya_case("ZR-01", "Valid hetuvidya case")),
    )
    failures: list[str] = []
    warnings: list[str] = []

    validate_reasoning_cases(tmp_path, failures, warnings, strict_yaml=True)

    assert warnings == []
    assert failures == []


def test_reasoning_cases_report_duplicate_case_ids(tmp_path: Path) -> None:
    _write_reasoning_case_repo(
        tmp_path,
        _reasoning_fixture(
            _valid_hetuvidya_case("ZR-01", "First valid case")
            + _valid_hetuvidya_case("ZR-01", "Duplicate valid case")
        ),
    )
    failures: list[str] = []
    warnings: list[str] = []

    validate_reasoning_cases(tmp_path, failures, warnings, strict_yaml=True)

    assert warnings == []
    assert failures == ["tests/reasoning_cases.yaml contains duplicate case id: ZR-01"]


def test_reasoning_cases_report_top_level_metadata_errors(tmp_path: Path) -> None:
    _write_reasoning_case_repo(
        tmp_path,
        """version: 2
source: docs/architecture/missing.md
purpose: ""
cases: []
""",
    )
    failures: list[str] = []
    warnings: list[str] = []

    validate_reasoning_cases(tmp_path, failures, warnings, strict_yaml=True)

    assert warnings == []
    assert failures == [
        "tests/reasoning_cases.yaml version must be 1.",
        "tests/reasoning_cases.yaml source must reference an existing local file.",
        "tests/reasoning_cases.yaml purpose must be a non-empty string.",
        "tests/reasoning_cases.yaml must contain a non-empty cases list.",
    ]


def test_reasoning_cases_report_invalid_contract_and_case_shape_errors(tmp_path: Path) -> None:
    case = """  - id: ZR-01
    title: ""
    prompt: ""
    source_regression_cases:
      - ZC-99
    contracts:
      - unknown_contract
    reference_files:
      - context/missing-reference.md
    expected:
      boundary_statement: "yes"
      structure: []
"""
    _write_reasoning_case_repo(tmp_path, _reasoning_fixture(case))
    failures: list[str] = []
    warnings: list[str] = []

    validate_reasoning_cases(tmp_path, failures, warnings, strict_yaml=True)

    assert warnings == []
    assert "tests/reasoning_cases.yaml ZR-01 missing string field: title" in failures
    assert "tests/reasoning_cases.yaml ZR-01 missing string field: prompt" in failures
    assert "tests/reasoning_cases.yaml ZR-01 source_regression_cases must reference known ZC cases." in failures
    assert "tests/reasoning_cases.yaml ZR-01 has invalid contracts: ['unknown_contract']" in failures
    assert "tests/reasoning_cases.yaml ZR-01 references missing path: context/missing-reference.md" in failures
    assert "tests/reasoning_cases.yaml ZR-01 expected.boundary_statement must be boolean." in failures
    assert "tests/reasoning_cases.yaml ZR-01 expected.structure must be a list." in failures


def test_reasoning_cases_report_non_hetuvidya_contract_shape_errors(tmp_path: Path) -> None:
    case = """  - id: ZR-01
    title: Multi-family malformed case
    prompt: "Review multiple malformed families."
    contracts:
      - collected_topics
      - cognitive_analysis
      - madhyamaka_prasanga
      - agama_evidence
    reference_files:
      - context/reasoning-reference.md
    expected:
      boundary_statement: true
      structure:
        - claim
      collected_topics:
        concepts: []
        relation_checks: {}
        error_type: ""
      cognitive_analysis:
        chain:
          - wrong
        afflictions: []
        corrective_factors: []
      madhyamaka_prasanga:
        opponent_premise: ""
        accepted_commitments: []
        contradiction: []
        no_independent_thesis: false
      agama_evidence:
        citation_required: "yes"
        collation_boundary: "no"
        search_scope: ""
"""
    _write_reasoning_case_repo(tmp_path, _reasoning_fixture(case))
    failures: list[str] = []
    warnings: list[str] = []

    validate_reasoning_cases(tmp_path, failures, warnings, strict_yaml=True)

    assert warnings == []
    expected_fragments = [
        "expected.collected_topics.concepts must be a list.",
        "expected.collected_topics.relation_checks must be a mapping.",
        "expected.collected_topics.error_type must be a string.",
        "expected.cognitive_analysis.chain must be",
        "expected.cognitive_analysis.afflictions must be a list.",
        "expected.cognitive_analysis.corrective_factors must be a list.",
        "expected.madhyamaka_prasanga.opponent_premise must be a string.",
        "expected.madhyamaka_prasanga.accepted_commitments must be a list.",
        "expected.madhyamaka_prasanga.contradiction must be a list.",
        "expected.madhyamaka_prasanga.no_independent_thesis must be true.",
        "expected.agama_evidence.citation_required must be boolean.",
        "expected.agama_evidence.collation_boundary must be boolean.",
        "expected.agama_evidence.search_scope must be a string.",
    ]
    for fragment in expected_fragments:
        assert any(fragment in failure for failure in failures)
