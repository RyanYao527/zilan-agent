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


def test_reasoning_cases_accept_minimal_valid_hetuvidya_case(tmp_path: Path) -> None:
    _write_reasoning_case_repo(
        tmp_path,
        f"""version: 1
source: docs/architecture/reasoning-contract.md
purpose: Test reasoning fixtures.
cases:
{_valid_hetuvidya_case("ZR-01", "Valid hetuvidya case")}""",
    )
    failures: list[str] = []
    warnings: list[str] = []

    validate_reasoning_cases(tmp_path, failures, warnings, strict_yaml=True)

    assert warnings == []
    assert failures == []


def test_reasoning_cases_report_duplicate_case_ids(tmp_path: Path) -> None:
    _write_reasoning_case_repo(
        tmp_path,
        f"""version: 1
source: docs/architecture/reasoning-contract.md
purpose: Test reasoning fixtures.
cases:
{_valid_hetuvidya_case("ZR-01", "First valid case")}{_valid_hetuvidya_case("ZR-01", "Duplicate valid case")}""",
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
