from __future__ import annotations

import json
import os
import subprocess
import sys
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _install_package_to_target(tmp_path: Path) -> Path:
    target = tmp_path / "site"
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "pip",
            "install",
            "--no-deps",
            "--target",
            str(target),
            str(ROOT),
        ],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    return target


def _run_installed_package(target: Path, tmp_path: Path, code: str) -> dict[str, object]:
    outside_cwd = tmp_path / "outside"
    outside_cwd.mkdir()
    env = os.environ.copy()
    env["PYTHONPATH"] = str(target)
    env.pop("PYTHONHOME", None)
    result = subprocess.run(
        [sys.executable, "-c", code],
        cwd=outside_cwd,
        env=env,
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    return json.loads(result.stdout)


def test_installed_contract_runner_quickstart_sample_and_inline_answer_work(tmp_path: Path) -> None:
    target = _install_package_to_target(tmp_path)
    data = _run_installed_package(
        target,
        tmp_path,
        textwrap.dedent(
            """
            import json
            from pathlib import Path

            from zilan_contract import ContractRunner, get_fixture_path

            runner = ContractRunner()
            sample_result = runner.check(
                query_id="SRQ-04",
                sample_id="srq04-agama-citation-boundary-pass",
            )
            answer_text = Path(
                get_fixture_path("answers/srq04-agama-citation-boundary-pass.md")
            ).read_text(encoding="utf-8")
            inline_result = runner.check(
                query_id="SRQ-04",
                answer_text=answer_text,
            )
            print(json.dumps({
                "sample_status": sample_result.overall_status,
                "sample_review_status": sample_result.answer_review_status,
                "sample_file": sample_result.raw["answer_contract_review"]["answer_source"]["file"],
                "inline_status": inline_result.overall_status,
                "inline_review_status": inline_result.answer_review_status,
            }, ensure_ascii=False))
            """
        ),
    )

    assert data == {
        "sample_status": "pass",
        "sample_review_status": "pass",
        "sample_file": "tests/fixtures/answers/srq04-agama-citation-boundary-pass.md",
        "inline_status": "pass",
        "inline_review_status": "pass",
    }
