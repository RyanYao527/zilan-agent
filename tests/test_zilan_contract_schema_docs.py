from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DOC = ROOT / "docs" / "zilan-contract-schema.md"
QUICKSTART_DOC = ROOT / "docs" / "zilan-contract-quickstart.md"
RELEASE_CHECKLIST_DOC = ROOT / "docs" / "zilan-contract-release-checklist.md"


def test_zilan_contract_schema_reference_documents_public_api_and_semantics() -> None:
    text = SCHEMA_DOC.read_text(encoding="utf-8")

    required_snippets = [
        "CLI file shape",
        "Python API shape",
        "AnswerContractRunner",
        "case-sensitive substring",
        "`missing_required_term`",
        "`present_forbidden_term`",
        "`missing_required_slot`",
        "Contracts must contain at least one contract.",
        "Contract file contains invalid YAML",
        "Contract file must contain a top-level contracts mapping.",
        "does not support regex",
        "severity",
        "exit code `2`",
    ]

    missing = [snippet for snippet in required_snippets if snippet not in text]

    assert missing == []


def test_zilan_contract_productization_docs_define_release_boundary() -> None:
    quickstart_text = QUICKSTART_DOC.read_text(encoding="utf-8")
    checklist_text = RELEASE_CHECKLIST_DOC.read_text(encoding="utf-8")

    required_quickstart_snippets = [
        "60-second domain-neutral contract check",
        "medical-disclaimer.yaml",
        "deterministic output-contract checker",
        "not an LLM judge",
    ]
    required_checklist_snippets = [
        "Release Checklist",
        "python -m pytest tests/test_zilan_contract_installed_smoke.py",
        "installed-package validation",
        "Public API unchanged",
        "Do not claim semantic grading",
        "no provider calls",
    ]

    assert [snippet for snippet in required_quickstart_snippets if snippet not in quickstart_text] == []
    assert [snippet for snippet in required_checklist_snippets if snippet not in checklist_text] == []
