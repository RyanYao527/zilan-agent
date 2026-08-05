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
        errors="replace",
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
        errors="replace",
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    return json.loads(result.stdout)



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

def _run_installed_cli_check(
    target: Path,
    tmp_path: Path,
    folder_name: str,
    contract_text: str,
    answer_text: str = "This is not therapy.",
) -> subprocess.CompletedProcess[str]:
    outside_cwd = tmp_path / folder_name
    outside_cwd.mkdir()
    contract_file = outside_cwd / "contracts.yaml"
    contract_file.write_text(contract_text, encoding="utf-8")
    answer_file = outside_cwd / "answer.md"
    answer_file.write_text(answer_text, encoding="utf-8")
    env = os.environ.copy()
    env["PYTHONPATH"] = str(target)
    env.pop("PYTHONHOME", None)

    return subprocess.run(
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
        cwd=outside_cwd,
        env=env,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
    )
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
            def local_evidence_boundary(result):
                review = result.raw["validators"]["agama_evidence"]["evidence_reviews"][0]
                local_evidence = review["agama_evidence"]["local_evidence"]
                return {
                    "status": local_evidence["status"],
                    "source_root": local_evidence["source_root"],
                    "diagnostic_codes": sorted(item["code"] for item in review["diagnostics"]),
                }

            sample_boundary = local_evidence_boundary(sample_result)
            inline_boundary = local_evidence_boundary(inline_result)
            print(json.dumps({
                "sample_status": sample_result.overall_status,
                "sample_review_status": sample_result.answer_review_status,
                "sample_file": sample_result.raw["answer_contract_review"]["answer_source"]["file"],
                "sample_local_evidence_status": sample_boundary["status"],
                "sample_local_evidence_source_root": sample_boundary["source_root"],
                "sample_local_evidence_diagnostics": sample_boundary["diagnostic_codes"],
                "inline_status": inline_result.overall_status,
                "inline_review_status": inline_result.answer_review_status,
                "inline_local_evidence_status": inline_boundary["status"],
                "inline_local_evidence_source_root": inline_boundary["source_root"],
                "inline_local_evidence_diagnostics": inline_boundary["diagnostic_codes"],
            }, ensure_ascii=False))
            """
        ),
    )

    assert data == {
        "sample_status": "pass",
        "sample_review_status": "pass",
        "sample_file": "tests/fixtures/answers/srq04-agama-citation-boundary-pass.md",
        "sample_local_evidence_status": "not_applicable",
        "sample_local_evidence_source_root": None,
        "sample_local_evidence_diagnostics": [
            "boundary_statement_required",
            "citation_anchor_required",
            "collation_boundary_required",
            "local_evidence_anchors_not_available",
            "representative_search_scope",
        ],
        "inline_status": "pass",
        "inline_review_status": "pass",
        "inline_local_evidence_status": "not_applicable",
        "inline_local_evidence_source_root": None,
        "inline_local_evidence_diagnostics": [
            "boundary_statement_required",
            "citation_anchor_required",
            "collation_boundary_required",
            "local_evidence_anchors_not_available",
            "representative_search_scope",
        ],
    }


def test_installed_package_exposes_third_party_notices(tmp_path: Path) -> None:
    target = _install_package_to_target(tmp_path)
    data = _run_installed_package(
        target,
        tmp_path,
        textwrap.dedent(
            """
            import importlib.metadata as metadata
            import json

            dist = metadata.distribution("zilan-agent")
            files = [str(path).replace("\\\\", "/") for path in (dist.files or [])]
            notice_files = [path for path in files if path.endswith("THIRD_PARTY_NOTICES.md")]
            notice_texts = [dist.locate_file(path).read_text(encoding="utf-8") for path in notice_files]
            print(json.dumps({
                "notice_files": notice_files,
                "mentions_zilan_contract_fixtures": any("zilan_contract/fixtures" in text for text in notice_texts),
                "mentions_cbeta_license": any("CC BY-NC-SA 4.0" in text for text in notice_texts),
            }, ensure_ascii=False))
            """
        ),
    )

    assert data["notice_files"]
    assert data["mentions_zilan_contract_fixtures"] is True
    assert data["mentions_cbeta_license"] is True


def test_installed_package_exposes_answer_contract_runner(tmp_path: Path) -> None:
    target = _install_package_to_target(tmp_path)
    data = _run_installed_package(
        target,
        tmp_path,
        textwrap.dedent(
            """
            import json

            from zilan_contract import AnswerContractRunner

            contracts = {
                "support_boundary": {
                    "required_terms": ["not therapy", "professional support"],
                    "forbidden_terms": ["guaranteed cure"],
                }
            }
            result = AnswerContractRunner().check(
                answer_text="This is not therapy; consider professional support.",
                contracts=contracts,
            )
            print(json.dumps(result.to_summary(), ensure_ascii=False))
            """
        ),
    )

    assert data["overall_status"] == "pass"
    assert data["issue_count"] == 0


def test_installed_package_exposes_zilan_contract_console_script(tmp_path: Path) -> None:
    target = _install_package_to_target(tmp_path)
    outside_cwd = tmp_path / "outside-console-script"
    outside_cwd.mkdir()
    contract_file = outside_cwd / "contracts.yaml"
    contract_file.write_text(
        textwrap.dedent(
            """
            contracts:
              support_boundary:
                required_terms:
                  - not therapy
                forbidden_terms:
                  - guaranteed cure
            """
        ),
        encoding="utf-8",
    )
    answer_file = outside_cwd / "answer.md"
    answer_file.write_text("This is not therapy.", encoding="utf-8")
    script = _find_installed_console_script(target, "zilan-contract")
    env = os.environ.copy()
    env["PYTHONPATH"] = str(target)
    env.pop("PYTHONHOME", None)

    result = subprocess.run(
        [
            str(script),
            "check",
            "--contract-file",
            str(contract_file),
            "--answer-file",
            str(answer_file),
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

    assert result.returncode == 0, result.stdout + result.stderr
    data = json.loads(result.stdout)
    assert data["overall_status"] == "pass"
    assert data["issue_count"] == 0

def test_installed_package_cli_json_reports_issue_details(tmp_path: Path) -> None:
    target = _install_package_to_target(tmp_path)
    outside_cwd = tmp_path / "outside-cli"
    outside_cwd.mkdir()
    contract_file = outside_cwd / "contracts.yaml"
    contract_file.write_text(
        textwrap.dedent(
            """
            contracts:
              support_boundary:
                required_terms:
                  - not therapy
                forbidden_terms:
                  - guaranteed cure
            """
        ),
        encoding="utf-8",
    )
    answer_file = outside_cwd / "answer.md"
    answer_file.write_text(
        "This is not therapy, but it is not a guaranteed cure.",
        encoding="utf-8",
    )
    env = os.environ.copy()
    env["PYTHONPATH"] = str(target)
    env.pop("PYTHONHOME", None)

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
        cwd=outside_cwd,
        env=env,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
    )

    assert result.returncode == 1, result.stdout + result.stderr
    data = json.loads(result.stdout)
    assert data["overall_status"] == "fail"
    assert data["issues"] == [
        {
            "source": "answer_contract",
            "contract_id": "support_boundary",
            "kind": "present_forbidden_term",
            "label": "guaranteed cure",
            "detail": "Present forbidden term: guaranteed cure",
        }
    ]


def test_installed_package_cli_rejects_malformed_contract_schema(tmp_path: Path) -> None:
    target = _install_package_to_target(tmp_path)
    outside_cwd = tmp_path / "outside-bad-schema"
    outside_cwd.mkdir()
    contract_file = outside_cwd / "contracts.yaml"
    contract_file.write_text(
        textwrap.dedent(
            """
            contracts:
              support_boundary:
                required_terms: not therapy
            """
        ),
        encoding="utf-8",
    )
    answer_file = outside_cwd / "answer.md"
    answer_file.write_text("This is not therapy.", encoding="utf-8")
    env = os.environ.copy()
    env["PYTHONPATH"] = str(target)
    env.pop("PYTHONHOME", None)

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
        cwd=outside_cwd,
        env=env,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
    )

    assert result.returncode == 2, result.stdout + result.stderr
    assert "support_boundary" in result.stderr
    assert "required_terms" in result.stderr



def test_installed_package_cli_rejects_malformed_yaml(tmp_path: Path) -> None:
    target = _install_package_to_target(tmp_path)
    result = _run_installed_cli_check(
        target=target,
        tmp_path=tmp_path,
        folder_name="outside-invalid-yaml",
        contract_text="contracts:\n  support_boundary:\n    required_terms: [not therapy\n",
    )

    assert result.returncode == 2, result.stdout + result.stderr
    assert result.stdout == ""
    assert "Contract file contains invalid YAML" in result.stderr


def test_installed_package_cli_rejects_missing_contracts_mapping(tmp_path: Path) -> None:
    target = _install_package_to_target(tmp_path)
    result = _run_installed_cli_check(
        target=target,
        tmp_path=tmp_path,
        folder_name="outside-missing-contracts",
        contract_text=textwrap.dedent(
            """
            support_boundary:
              required_terms:
                - not therapy
            """
        ),
    )

    assert result.returncode == 2, result.stdout + result.stderr
    assert result.stdout == ""
    assert "Contract file must contain a top-level contracts mapping." in result.stderr
def test_installed_zilanlib_direct_runner_uses_package_local_evidence_boundary(tmp_path: Path) -> None:
    target = _install_package_to_target(tmp_path)
    data = _run_installed_package(
        target,
        tmp_path,
        textwrap.dedent(
            """
            import json
            from pathlib import Path

            from zilan_contract import get_cases_path, get_fixture_path
            from zilanlib.reasoning.contract_runner import build_reasoning_contract_run

            answer_text = Path(
                get_fixture_path("answers/srq04-agama-citation-boundary-pass.md")
            ).read_text(encoding="utf-8")
            result = build_reasoning_contract_run(
                fixture_path=get_fixture_path(),
                cases_path=get_cases_path(),
                query_id="SRQ-04",
                answer_text=answer_text,
            )
            review = result["validators"]["agama_evidence"]["evidence_reviews"][0]
            local_evidence = review["agama_evidence"]["local_evidence"]
            print(json.dumps({
                "overall_status": result["overall_status"],
                "answer_review_status": result["answer_review_status"],
                "local_evidence_status": local_evidence["status"],
                "local_evidence_source_root": local_evidence["source_root"],
                "diagnostic_codes": sorted(item["code"] for item in review["diagnostics"]),
            }, ensure_ascii=False))
            """
        ),
    )

    assert data == {
        "overall_status": "pass",
        "answer_review_status": "pass",
        "local_evidence_status": "not_applicable",
        "local_evidence_source_root": None,
        "diagnostic_codes": [
            "boundary_statement_required",
            "citation_anchor_required",
            "collation_boundary_required",
            "local_evidence_anchors_not_available",
            "representative_search_scope",
        ],
    }


def test_installed_contract_runner_all_answer_contract_pass_samples_load_from_package(tmp_path: Path) -> None:
    target = _install_package_to_target(tmp_path)
    data = _run_installed_package(
        target,
        tmp_path,
        textwrap.dedent(
            """
            import json
            from pathlib import Path

            from zilan_contract import ContractRunner, get_fixture_path

            all_pass_samples = [
                "srq01-practice-boundary-pass",
                "srq02-hetuvidya-error-pass",
                "srq03-madhyamaka-prasanga-pass",
                "srq04-agama-citation-boundary-pass",
                "srq05-hetuvidya-non-pervasive-pass",
                "srq06-hetuvidya-indeterminate-pass",
                "srq07-collected-topics-total-part-pass",
                "srq08-madhyamaka-nihilism-boundary-pass",
                "srq09-cognitive-practice-boundary-pass",
                "srq10-cognitive-caregiving-boundary-pass",
                "srq11-collected-topics-definition-scope-pass",
            ]
            answer_contract_samples = {
                "SRQ-02": "srq02-hetuvidya-error-pass",
                "SRQ-03": "srq03-madhyamaka-prasanga-pass",
                "SRQ-04": "srq04-agama-citation-boundary-pass",
                "SRQ-05": "srq05-hetuvidya-non-pervasive-pass",
                "SRQ-06": "srq06-hetuvidya-indeterminate-pass",
                "SRQ-07": "srq07-collected-topics-total-part-pass",
                "SRQ-08": "srq08-madhyamaka-nihilism-boundary-pass",
                "SRQ-09": "srq09-cognitive-practice-boundary-pass",
                "SRQ-10": "srq10-cognitive-caregiving-boundary-pass",
                "SRQ-11": "srq11-collected-topics-definition-scope-pass",
            }
            bundled_files = {
                sample_id: Path(get_fixture_path(f"answers/{sample_id}.md")).is_file()
                for sample_id in all_pass_samples
            }
            runner = ContractRunner()
            statuses = {
                sample_id: runner.check(query_id=query_id, sample_id=sample_id).answer_review_status
                for query_id, sample_id in answer_contract_samples.items()
            }
            print(json.dumps({
                "bundled_files": bundled_files,
                "statuses": statuses,
            }, ensure_ascii=False, sort_keys=True))
            """
        ),
    )

    assert set(data["bundled_files"]) == {
        "srq01-practice-boundary-pass",
        "srq02-hetuvidya-error-pass",
        "srq03-madhyamaka-prasanga-pass",
        "srq04-agama-citation-boundary-pass",
        "srq05-hetuvidya-non-pervasive-pass",
        "srq06-hetuvidya-indeterminate-pass",
        "srq07-collected-topics-total-part-pass",
        "srq08-madhyamaka-nihilism-boundary-pass",
        "srq09-cognitive-practice-boundary-pass",
        "srq10-cognitive-caregiving-boundary-pass",
        "srq11-collected-topics-definition-scope-pass",
    }
    assert set(data["bundled_files"].values()) == {True}
    assert set(data["statuses"].values()) == {"pass"}
