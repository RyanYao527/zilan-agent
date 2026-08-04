from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DOC = ROOT / "docs" / "zilan-contract-schema.md"


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
