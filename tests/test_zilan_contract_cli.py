from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def test_zilan_contract_cli_check_outputs_json(tmp_path: Path) -> None:
    contract_file = tmp_path / "contracts.yaml"
    answer_file = tmp_path / "answer.md"
    contract_file.write_text(
        """
contracts:
  financial_risk:
    required_terms:
      - not financial advice
      - risk
    forbidden_terms:
      - guaranteed return
    required_slots:
      - label: boundary
        terms:
          - not financial advice
""".strip(),
        encoding="utf-8",
    )
    answer_file.write_text("This is not financial advice. Investment involves risk.", encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "zilan_contract.cli",
            "check",
            "--contract-file",
            str(contract_file),
            "--answer-file",
            str(answer_file),
            "--json",
        ],
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=True,
    )

    data = json.loads(result.stdout)
    assert data["overall_status"] == "pass"
    assert data["issue_count"] == 0


def test_zilan_contract_cli_check_exits_nonzero_on_fail(tmp_path: Path) -> None:
    contract_file = tmp_path / "contracts.yaml"
    answer_file = tmp_path / "answer.md"
    contract_file.write_text(
        "contracts:\n  legal_boundary:\n    required_terms: ['not legal advice']\n",
        encoding="utf-8",
    )
    answer_file.write_text("This is definitive legal advice.", encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "zilan_contract.cli",
            "check",
            "--contract-file",
            str(contract_file),
            "--answer-file",
            str(answer_file),
            "--markdown",
        ],
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=False,
    )

    assert result.returncode == 1
    assert "# Answer Contract Review" in result.stdout
    assert "legal_boundary" in result.stdout
