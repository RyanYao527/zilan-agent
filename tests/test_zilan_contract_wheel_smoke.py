from __future__ import annotations

import json
import os
import subprocess
import sys
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "docs" / "examples" / "zilan-contract"


def _build_wheel(tmp_path: Path) -> Path:
    wheelhouse = tmp_path / "wheelhouse"
    wheelhouse.mkdir()
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "pip",
            "wheel",
            "--no-deps",
            "--no-build-isolation",
            "--wheel-dir",
            str(wheelhouse),
            str(ROOT),
        ],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    wheels = sorted(wheelhouse.glob("zilan_agent-*.whl"))
    assert len(wheels) == 1
    return wheels[0]


def _install_wheel_to_target(tmp_path: Path) -> Path:
    wheel = _build_wheel(tmp_path)
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
            str(wheel),
        ],
        cwd=tmp_path,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    return target


def _installed_env(target: Path) -> dict[str, str]:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(target)
    env.pop("PYTHONHOME", None)
    return env


def _find_installed_console_script(target: Path, script_name: str) -> Path:
    candidates = [
        target / "Scripts" / f"{script_name}.exe",
        target / "Scripts" / f"{script_name}.cmd",
        target / "Scripts" / script_name,
        target / "bin" / script_name,
        target / "bin" / f"{script_name}.exe",
    ]
    for candidate in candidates:
        if candidate.is_file():
            return candidate

    matches = sorted(path for path in target.rglob(f"{script_name}*") if path.is_file())
    assert matches, f"Installed console script not found under {target}"
    return matches[0]


def test_wheel_install_exposes_public_api_module_cli_console_script_and_examples(tmp_path: Path) -> None:
    target = _install_wheel_to_target(tmp_path)
    outside_cwd = tmp_path / "outside-source-tree"
    outside_cwd.mkdir()
    env = _installed_env(target)

    api_result = subprocess.run(
        [
            sys.executable,
            "-c",
            textwrap.dedent(
                """
                import json

                from zilan_contract import AnswerContractRunner, ContractRunner, HetuvidyaValidator, get_fixture_path

                contract_runner = ContractRunner()
                sample_result = contract_runner.check(
                    query_id="SRQ-04",
                    sample_id="srq04-agama-citation-boundary-pass",
                )
                answer_result = AnswerContractRunner().check(
                    answer_text="This is not legal advice. Consult an attorney.",
                    contracts={
                        "legal_boundary": {
                            "required_terms": ["not legal advice"],
                            "forbidden_terms": ["guaranteed outcome"],
                            "required_slots": [
                                {"label": "care_path", "terms": ["attorney", "qualified professional"]},
                            ],
                        },
                    },
                )
                hetuvidya_result = HetuvidyaValidator().validate(case_id="ZR-01")
                print(json.dumps({
                    "contract_runner_status": sample_result.overall_status,
                    "answer_contract_status": answer_result.overall_status,
                    "answer_contract_issue_count": len(answer_result.issues()),
                    "hetuvidya_status": hetuvidya_result["status"],
                    "bundled_answer_exists": get_fixture_path(
                        "answers/srq04-agama-citation-boundary-pass.md"
                    ).is_file(),
                }, ensure_ascii=False, sort_keys=True))
                """
            ),
        ],
        cwd=outside_cwd,
        env=env,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
    )
    assert api_result.returncode == 0, api_result.stdout + api_result.stderr
    api_data = json.loads(api_result.stdout)
    assert api_data == {
        "answer_contract_issue_count": 0,
        "answer_contract_status": "pass",
        "bundled_answer_exists": True,
        "contract_runner_status": "pass",
        "hetuvidya_status": "run",
    }

    module_result = subprocess.run(
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
        cwd=outside_cwd,
        env=env,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
    )
    assert module_result.returncode == 0, module_result.stdout + module_result.stderr
    module_data = json.loads(module_result.stdout)
    assert module_data["overall_status"] == "pass"
    assert module_data["issue_count"] == 0

    console_script = _find_installed_console_script(target, "zilan-contract")
    console_result = subprocess.run(
        [
            str(console_script),
            "check",
            "--contract-file",
            str(EXAMPLES / "medical-disclaimer.yaml"),
            "--answer-file",
            str(EXAMPLES / "medical-disclaimer-fail.md"),
            "--json",
        ],
        cwd=outside_cwd,
        env=env,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
    )
    assert console_result.returncode == 1, console_result.stdout + console_result.stderr
    console_data = json.loads(console_result.stdout)
    assert console_data["overall_status"] == "fail"
    assert console_data["issue_count"] > 0
    assert {issue["kind"] for issue in console_data["issues"]} >= {
        "missing_required_term",
        "present_forbidden_term",
    }