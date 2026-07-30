from __future__ import annotations

from pathlib import Path

from zilanlib.validation.runtime_evidence import REGRESSION_CASES
from zilanlib.yaml_io import load_yaml_for_validation

REGRESSION_CASES_PATH = "tests/regression_cases.yaml"


def validate_regression_cases(root: Path, failures: list[str], warnings: list[str], strict_yaml: bool) -> None:
    data = load_yaml_for_validation(root, REGRESSION_CASES_PATH, failures, warnings, strict_yaml)
    if data is None:
        return
    if not isinstance(data, dict):
        failures.append(f"{REGRESSION_CASES_PATH} must be a mapping.")
        return

    cases = data.get("cases")
    if not isinstance(cases, list):
        failures.append(f"{REGRESSION_CASES_PATH} must contain a cases list.")
        return

    seen_ids: set[str] = set()
    for item in cases:
        if not isinstance(item, dict):
            failures.append(f"{REGRESSION_CASES_PATH} contains a non-mapping case.")
            continue

        case_id = item.get("id")
        if not isinstance(case_id, str) or not case_id:
            failures.append(f"{REGRESSION_CASES_PATH} contains a case without a string id.")
            continue
        if case_id in seen_ids:
            failures.append(f"{REGRESSION_CASES_PATH} contains duplicate case id: {case_id}")
        seen_ids.add(case_id)

        for field in ("mode", "category", "prompt"):
            if not isinstance(item.get(field), str) or not item[field]:
                failures.append(f"{REGRESSION_CASES_PATH} {case_id} missing string field: {field}")

        requires = item.get("requires")
        if not isinstance(requires, dict):
            failures.append(f"{REGRESSION_CASES_PATH} {case_id} missing requires mapping.")
        else:
            for field in ("subagent", "agama_search", "file_output"):
                if not isinstance(requires.get(field), bool):
                    failures.append(f"{REGRESSION_CASES_PATH} {case_id} requires.{field} must be boolean.")

        expected = item.get("expected")
        if not isinstance(expected, dict):
            failures.append(f"{REGRESSION_CASES_PATH} {case_id} missing expected mapping.")
            continue

        reference_files = expected.get("reference_files")
        if not isinstance(reference_files, list) or not reference_files:
            failures.append(f"{REGRESSION_CASES_PATH} {case_id} expected.reference_files must be a non-empty list.")
        else:
            for rel_path in reference_files:
                if not isinstance(rel_path, str) or not (root / rel_path).exists():
                    failures.append(f"{REGRESSION_CASES_PATH} {case_id} references missing path: {rel_path}")

        keywords = expected.get("keywords")
        if not isinstance(keywords, list) or not all(isinstance(keyword, str) and keyword for keyword in keywords):
            failures.append(f"{REGRESSION_CASES_PATH} {case_id} expected.keywords must be a non-empty string list.")
        if not isinstance(expected.get("boundary_statement"), bool):
            failures.append(f"{REGRESSION_CASES_PATH} {case_id} expected.boundary_statement must be boolean.")

    expected_ids = set(REGRESSION_CASES)
    if seen_ids != expected_ids:
        failures.append(
            f"{REGRESSION_CASES_PATH} case ids do not match CODEX matrix: "
            f"expected {sorted(expected_ids)}, got {sorted(seen_ids)}"
        )


_check_regression_cases_yaml = validate_regression_cases
