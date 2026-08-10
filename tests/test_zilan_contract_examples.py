from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "docs" / "examples" / "zilan-contract"


def test_medical_disclaimer_examples_are_executable() -> None:
    pass_result = subprocess.run(
        [
            sys.executable,
            "-m",
            "zilan_contract.cli",
            "check",
            "--contract-file",
            str(EXAMPLES / "medical-disclaimer.yaml"),
            "--answer-file",
            str(EXAMPLES / "medical-disclaimer-pass.md"),
            "--json",
        ],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=True,
    )
    assert '"overall_status": "pass"' in pass_result.stdout

    fail_result = subprocess.run(
        [
            sys.executable,
            "-m",
            "zilan_contract.cli",
            "check",
            "--contract-file",
            str(EXAMPLES / "medical-disclaimer.yaml"),
            "--answer-file",
            str(EXAMPLES / "medical-disclaimer-fail.md"),
            "--json",
        ],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=False,
    )
    assert fail_result.returncode == 1
    assert '"overall_status": "fail"' in fail_result.stdout
