from __future__ import annotations

import argparse
import hashlib
import re
import subprocess
import sys
from pathlib import Path

from search_agama import DEFAULT_FALSE_POSITIVE_PHRASES, search_agama

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = (
    "README.md",
    "README.zh.md",
    "README.en.md",
    "SKILL.md",
    "SKILL-en.md",
    "CHANGELOG.md",
    "CODEX_REGRESSION_TESTS.md",
    "AGENT_UPGRADE_PORTABLE.md",
    "docs/platform-validation.md",
    "docs/runtime-validation-log.md",
    "docs/runtime-evidence/README.md",
    "docs/runtime-evidence/evidence-template.md",
    "docs/runtime-evidence/2026-06-15-clean-install-smoke.md",
    "docs/runtime-evidence/2026-06-15-mock-claude-install-smoke.md",
    "docs/runtime-evidence/2026-06-15-codex-v245-runtime-rerun.md",
    "docs/runtime-evidence/2026-06-16-claude-code-utf8-rerun.md",
    "docs/maintenance-roadmap.md",
    "docs/installation.md",
    "docs/validation-evidence.md",
    "docs/provider-routes.md",
    "docs/openai-api-harness.md",
    "LICENSE",
    "CONTRIBUTING.md",
    "CONTRIBUTING-en.md",
    "agents/openai.yaml",
    "agents/zilan-claude-code.md",
    "agents/zilan-codex.md",
    "scripts/build_agama_context.py",
    "scripts/search_agama.py",
    "scripts/openai_api_harness.py",
    "scripts/mock_install_smoke.py",
    "tests/regression_cases.yaml",
)

REQUIRED_CONTEXT_FILES = (
    "context/摄类学工具箱.md",
    "context/因明推理引擎.md",
    "context/心类学认知分析.md",
    "context/中观应成精要.md",
    "context/南传观禅指南.md",
    "context/模因机器视角下的佛教结集与传播.md",
    "context/agama/agama-index.md",
    "context/agama/T0001-chang-agama.md",
    "context/agama/T0026-zhong-agama.md",
    "context/agama/T0099-za-agama.md",
    "context/agama/T0125-ekottarika-agama.md",
    "context/agama/_source/T01n0001.xml",
    "context/agama/_source/T01n0026.xml",
    "context/agama/_source/T02n0099.xml",
    "context/agama/_source/T02n0125.xml",
)

GENERATED_AGAMA_FILES = (
    "context/agama/agama-index.md",
    "context/agama/T0001-chang-agama.md",
    "context/agama/T0026-zhong-agama.md",
    "context/agama/T0099-za-agama.md",
    "context/agama/T0125-ekottarika-agama.md",
)

REGRESSION_CASES = ("ZC-01", "ZC-02", "ZC-03", "ZC-04", "ZC-05", "ZC-06")
REGRESSION_CASES_PATH = "tests/regression_cases.yaml"
README_FILES = ("README.md", "README.zh.md", "README.en.md")
PUBLIC_STYLE_BOUNDARY_FILES = (
    "SKILL.md",
    "SKILL-en.md",
    "README.zh.md",
    "README.en.md",
    "agents/zilan-codex.md",
    "agents/zilan-claude-code.md",
    "CODEX_REGRESSION_TESTS.md",
    "tests/regression_cases.yaml",
    "context/摄类学工具箱.md",
    "context/心类学认知分析.md",
    "context/中观应成精要.md",
    "context/南传观禅指南.md",
)
HIGH_RISK_PUBLIC_FRAGMENTS = (
    "认知带宽受限",
    "育儿耐心溃败",
    "育儿溃败",
    "两性得失计较",
    "两性计较",
    "三大长间隙",
    "职场否定",
    "灵性经验切片",
    "深度沉迷",
    "AI佛乐",
    "AI 佛乐",
    "感觉老婆",
    "11月孩子",
    "11 个月孩子",
    "被领导质疑",
    "带娃",
)
PLATFORM_VALIDATION_DOC = "docs/platform-validation.md"
RUNTIME_VALIDATION_LOG_DOC = "docs/runtime-validation-log.md"
RUNTIME_EVIDENCE_INDEX_DOC = "docs/runtime-evidence/README.md"
RUNTIME_EVIDENCE_TEMPLATE_DOC = "docs/runtime-evidence/evidence-template.md"
RUNTIME_EVIDENCE_CLEAN_INSTALL_DOC = "docs/runtime-evidence/2026-06-15-clean-install-smoke.md"
RUNTIME_EVIDENCE_MOCK_INSTALL_DOC = "docs/runtime-evidence/2026-06-15-mock-claude-install-smoke.md"
MAINTENANCE_ROADMAP_DOC = "docs/maintenance-roadmap.md"
INSTALLATION_DOC = "docs/installation.md"
VALIDATION_EVIDENCE_DOC = "docs/validation-evidence.md"
PROVIDER_ROUTES_DOC = "docs/provider-routes.md"
CHANGELOG_DOC = "CHANGELOG.md"
PORTABLE_UPGRADE_DOC = "AGENT_UPGRADE_PORTABLE.md"
VERSION_SOURCES = {
    "pyproject.toml": r'(?m)^version = "([^"]+)"$',
    "README.zh.md": r"\*\*版本\*\*：v([0-9]+\.[0-9]+\.[0-9]+)",
    "README.en.md": r"\*\*Version\*\*: v([0-9]+\.[0-9]+\.[0-9]+)",
    "CHANGELOG.md": r"(?m)^## \[([0-9]+\.[0-9]+\.[0-9]+)\] - ",
    "AGENT_UPGRADE_PORTABLE.md": r"Current project baseline: zilan-agent v([0-9]+\.[0-9]+\.[0-9]+)",
}
ALLOWED_VALIDATION_STATUSES = (
    "tested",
    "definition-versioned",
    "harness-ready",
    "metadata-only",
    "config-only",
    "blocked",
)
PLATFORM_VALIDATION_LABELS = {
    "codex": "Codex",
    "claude_code": "Claude Code",
    "openai_api": "OpenAI API",
    "volcengine_openai_compatible": "Volcengine OpenAI-Compatible",
    "deepseek": "DeepSeek",
    "glm": "GLM",
    "qwen": "Qwen",
}
AGENT_PROMPT_REQUIRED_FRAGMENTS = {
    "agents/zilan-codex.md": (
        "runtime: codex-sub-agent",
        "首轮任务执行优先级",
        "激活与任务合并规则",
        "禁止只输出身份问候",
        "Codex 阿含检索规范",
        "引用阿含经时必须注明",
        "边界与限制",
        "search_agama.py --terms",
        "search_agama.py --json",
        "citation",
        "passage_citation",
        "T02n0099",
        "context/agama/T0099-za-agama.md:",
    ),
    "agents/zilan-claude-code.md": (
        "输出硬约束",
        "首轮任务执行优先级",
        "激活与任务合并规则",
        "非交互运行护栏",
        "禁止只输出身份问候",
        "引用阿含经时必须注明",
        "search_agama.py",
        "search_agama.py --json",
        "citation",
        "passage_citation",
        "T02n0099",
        "context/agama/T0099-za-agama.md:",
    ),
}


def _hash_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _check_paths(root: Path, failures: list[str]) -> None:
    for rel_path in REQUIRED_FILES + REQUIRED_CONTEXT_FILES:
        if not (root / rel_path).exists():
            failures.append(f"Missing required path: {rel_path}")


def _extract_version(root: Path, rel_path: str, pattern: str, failures: list[str]) -> str | None:
    text = (root / rel_path).read_text(encoding="utf-8")
    match = re.search(pattern, text)
    if not match:
        failures.append(f"{rel_path} missing project version pattern.")
        return None
    return match.group(1)


def _check_version_consistency(root: Path, failures: list[str]) -> None:
    versions: dict[str, str] = {}
    for rel_path, pattern in VERSION_SOURCES.items():
        version = _extract_version(root, rel_path, pattern, failures)
        if version is not None:
            versions[rel_path] = version

    if len(set(versions.values())) > 1:
        details = ", ".join(f"{rel_path}={version}" for rel_path, version in sorted(versions.items()))
        failures.append(f"Project version mismatch: {details}")


def _check_regression_matrix(root: Path, failures: list[str]) -> None:
    text = (root / "CODEX_REGRESSION_TESTS.md").read_text(encoding="utf-8")
    for case in REGRESSION_CASES:
        if case not in text:
            failures.append(f"Missing regression case in CODEX_REGRESSION_TESTS.md: {case}")


def _load_yaml(root: Path, rel_path: str, failures: list[str], warnings: list[str], strict_yaml: bool) -> object | None:
    yaml_path = root / rel_path
    try:
        import yaml  # type: ignore[import-not-found]
    except ModuleNotFoundError:
        message = f"PyYAML is not installed; skipped {rel_path} parse check."
        if strict_yaml:
            failures.append(message)
        else:
            warnings.append(message)
        return None

    try:
        return yaml.safe_load(yaml_path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001 - surface parser details to maintainers.
        failures.append(f"Failed to parse {rel_path}: {exc}")
        return None


def _check_regression_cases_yaml(root: Path, failures: list[str], warnings: list[str], strict_yaml: bool) -> None:
    data = _load_yaml(root, REGRESSION_CASES_PATH, failures, warnings, strict_yaml)
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


def _check_agent_prompts(root: Path, failures: list[str]) -> None:
    for rel_path, required_fragments in AGENT_PROMPT_REQUIRED_FRAGMENTS.items():
        text = (root / rel_path).read_text(encoding="utf-8")
        for fragment in required_fragments:
            if fragment not in text:
                failures.append(f"{rel_path} missing required fragment: {fragment}")


def _get_validation_mapping(data: object, failures: list[str]) -> dict[str, object]:
    if not isinstance(data, dict):
        failures.append("agents/openai.yaml must be a mapping.")
        return {}

    validation = data.get("validation")
    if not isinstance(validation, dict):
        failures.append("agents/openai.yaml missing validation mapping.")
        return {}
    return validation


def _check_agent_validation_entries(validation: dict[str, object], failures: list[str]) -> None:
    expected_keys = set(PLATFORM_VALIDATION_LABELS)
    actual_keys = set(validation)
    for provider in sorted(expected_keys - actual_keys):
        failures.append(f"agents/openai.yaml missing validation entry: {provider}")
    for provider in sorted(actual_keys - expected_keys):
        failures.append(f"agents/openai.yaml has undocumented validation entry: {provider}")

    for provider in PLATFORM_VALIDATION_LABELS:
        entry = validation.get(provider)
        if not isinstance(entry, dict):
            failures.append(f"agents/openai.yaml validation.{provider} must be a mapping.")
            continue

        status = entry.get("status")
        if status not in ALLOWED_VALIDATION_STATUSES:
            failures.append(
                f"agents/openai.yaml validation.{provider}.status must be one of "
                f"{', '.join(ALLOWED_VALIDATION_STATUSES)}."
            )
        if not isinstance(entry.get("scope"), str) or not entry["scope"]:
            failures.append(f"agents/openai.yaml validation.{provider}.scope must be a non-empty string.")
        if status == "tested" and (not isinstance(entry.get("date"), str) or not entry["date"]):
            failures.append(f"agents/openai.yaml validation.{provider}.date is required when status is tested.")


def _parse_markdown_table_rows(text: str) -> dict[str, list[str]]:
    rows: dict[str, list[str]] = {}
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|") or set(stripped.replace("|", "").strip()) <= {"-", ":"}:
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if len(cells) >= 2:
            rows[cells[0]] = cells
    return rows


def _check_platform_validation_doc(root: Path, validation: dict[str, object], failures: list[str]) -> None:
    doc_text = (root / PLATFORM_VALIDATION_DOC).read_text(encoding="utf-8")
    rows = _parse_markdown_table_rows(doc_text)

    for status in ALLOWED_VALIDATION_STATUSES:
        if f"| `{status}` |" not in doc_text:
            failures.append(f"{PLATFORM_VALIDATION_DOC} missing status definition: {status}")

    for provider, label in PLATFORM_VALIDATION_LABELS.items():
        entry = validation.get(provider)
        if not isinstance(entry, dict):
            continue

        status = entry.get("status")
        if not isinstance(status, str):
            continue

        row = rows.get(label)
        if row is None:
            failures.append(f"{PLATFORM_VALIDATION_DOC} missing platform row: {label}")
            continue
        if len(row) < 3:
            failures.append(f"{PLATFORM_VALIDATION_DOC} platform row is incomplete: {label}")
            continue
        if row[1] != f"`{status}`":
            failures.append(
                f"{PLATFORM_VALIDATION_DOC} status mismatch for {label}: "
                f"expected `{status}` from agents/openai.yaml, got {row[1]}."
            )

        date = entry.get("date")
        if status == "tested" and isinstance(date, str) and row[2] != date:
            failures.append(
                f"{PLATFORM_VALIDATION_DOC} validation date mismatch for {label}: "
                f"expected {date} from agents/openai.yaml, got {row[2]}."
            )


def _check_readme_platform_validation_links(root: Path, failures: list[str]) -> None:
    for rel_path in README_FILES:
        text = (root / rel_path).read_text(encoding="utf-8")
        if PLATFORM_VALIDATION_DOC not in text:
            failures.append(f"{rel_path} should link to {PLATFORM_VALIDATION_DOC}.")
        if RUNTIME_VALIDATION_LOG_DOC not in text:
            failures.append(f"{rel_path} should link to {RUNTIME_VALIDATION_LOG_DOC}.")
        if "docs/runtime-evidence/" not in text:
            failures.append(f"{rel_path} should link to docs/runtime-evidence/.")
        if MAINTENANCE_ROADMAP_DOC not in text:
            failures.append(f"{rel_path} should link to {MAINTENANCE_ROADMAP_DOC}.")
        if INSTALLATION_DOC not in text:
            failures.append(f"{rel_path} should link to {INSTALLATION_DOC}.")
        if VALIDATION_EVIDENCE_DOC not in text:
            failures.append(f"{rel_path} should link to {VALIDATION_EVIDENCE_DOC}.")
        if PROVIDER_ROUTES_DOC not in text:
            failures.append(f"{rel_path} should link to {PROVIDER_ROUTES_DOC}.")
        if CHANGELOG_DOC not in text:
            failures.append(f"{rel_path} should link to {CHANGELOG_DOC}.")
        if "agents/openai.yaml" not in text:
            failures.append(f"{rel_path} should mention agents/openai.yaml as platform metadata.")


def _check_public_style_boundaries(root: Path, failures: list[str]) -> None:
    for rel_path in PUBLIC_STYLE_BOUNDARY_FILES:
        text = (root / rel_path).read_text(encoding="utf-8")
        for fragment in HIGH_RISK_PUBLIC_FRAGMENTS:
            if fragment in text:
                failures.append(
                    f"{rel_path} contains private/autobiographical public fragment: {fragment}"
                )


def _check_runtime_validation_log(root: Path, failures: list[str]) -> None:
    text = (root / RUNTIME_VALIDATION_LOG_DOC).read_text(encoding="utf-8")
    required_fragments = (
        "2026-06-10",
        "Codex",
        "CODEX_REGRESSION_TESTS.md",
        "docs/platform-validation.md",
        "Transcript status",
    )
    for fragment in required_fragments:
        if fragment not in text:
            failures.append(f"{RUNTIME_VALIDATION_LOG_DOC} missing required fragment: {fragment}")
    for case in REGRESSION_CASES:
        if case not in text:
            failures.append(f"{RUNTIME_VALIDATION_LOG_DOC} missing regression case: {case}")
    if RUNTIME_EVIDENCE_CLEAN_INSTALL_DOC not in text:
        failures.append(f"{RUNTIME_VALIDATION_LOG_DOC} should link to {RUNTIME_EVIDENCE_CLEAN_INSTALL_DOC}.")
    if RUNTIME_EVIDENCE_MOCK_INSTALL_DOC not in text:
        failures.append(f"{RUNTIME_VALIDATION_LOG_DOC} should link to {RUNTIME_EVIDENCE_MOCK_INSTALL_DOC}.")


def _check_runtime_evidence_docs(root: Path, failures: list[str]) -> None:
    index_text = (root / RUNTIME_EVIDENCE_INDEX_DOC).read_text(encoding="utf-8")
    clean_install_text = (root / RUNTIME_EVIDENCE_CLEAN_INSTALL_DOC).read_text(encoding="utf-8")
    mock_install_text = (root / RUNTIME_EVIDENCE_MOCK_INSTALL_DOC).read_text(encoding="utf-8")
    template_text = (root / RUNTIME_EVIDENCE_TEMPLATE_DOC).read_text(encoding="utf-8")

    for fragment in (
        "Runtime Evidence Excerpts",
        "Do not use this directory for",
        "docs/validation-evidence.md",
    ):
        if fragment not in index_text:
            failures.append(f"{RUNTIME_EVIDENCE_INDEX_DOC} missing required fragment: {fragment}")

    for fragment in (
        "2026-06-15 Clean Install Smoke Evidence",
        "zilan-agent validation passed.",
        "mode: dry-run",
        "Found 5 matches",
        "No secrets",
    ):
        if fragment not in clean_install_text:
            failures.append(f"{RUNTIME_EVIDENCE_CLEAN_INSTALL_DOC} missing required fragment: {fragment}")

    for fragment in (
        "2026-06-15 Mock Claude Install Smoke Evidence",
        "mode: mock-claude-install",
        "skill:scripts/search_agama.py: pass",
        "agent:matches-source: pass",
        "Found 1 matches",
    ):
        if fragment not in mock_install_text:
            failures.append(f"{RUNTIME_EVIDENCE_MOCK_INSTALL_DOC} missing required fragment: {fragment}")

    for fragment in ("Redaction note", "Output Excerpts", "Limitations"):
        if fragment not in template_text:
            failures.append(f"{RUNTIME_EVIDENCE_TEMPLATE_DOC} missing required fragment: {fragment}")


def _check_portable_upgrade_doc(root: Path, failures: list[str]) -> None:
    text = (root / PORTABLE_UPGRADE_DOC).read_text(encoding="utf-8")
    required_fragments = (
        "Skill To Agent Migration Record",
        "Current Architecture",
        "docs/installation.md",
        "docs/platform-validation.md",
        "docs/provider-routes.md",
        "DeepSeek Compatibility Caveat",
        "Do not infer platform support from this file alone",
    )
    for fragment in required_fragments:
        if fragment not in text:
            failures.append(f"{PORTABLE_UPGRADE_DOC} missing required fragment: {fragment}")


def _check_yaml(root: Path, failures: list[str], warnings: list[str], strict_yaml: bool) -> None:
    data = _load_yaml(root, "agents/openai.yaml", failures, warnings, strict_yaml)
    if data is None:
        return

    validation = _get_validation_mapping(data, failures)
    if not validation:
        return

    _check_agent_validation_entries(validation, failures)
    _check_platform_validation_doc(root, validation, failures)
    codex_validation = validation.get("codex")
    if not isinstance(codex_validation, dict) or codex_validation.get("status") != "tested":
        failures.append("agents/openai.yaml should mark validation.codex.status as tested.")


def _check_agama_search(root: Path, failures: list[str]) -> None:
    matches = search_agama("無我|非我|緣起", root=root, limit=30)
    if not matches:
        failures.append("Agama smoke search returned no matches.")
        return
    if any("_source" in match.file for match in matches):
        failures.append("Agama smoke search should not return _source XML matches.")

    false_positive_check = search_agama("無我|非我", root=root, limit=0)
    if any(
        any(phrase in match.text for phrase in DEFAULT_FALSE_POSITIVE_PHRASES)
        for match in false_positive_check
    ):
        failures.append("Agama search did not filter known false positives.")


def _run_build_agama(root: Path) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        [sys.executable, str(root / "scripts" / "build_agama_context.py")],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )
    return result


def _check_generated_agama(root: Path, failures: list[str]) -> None:
    result = _run_build_agama(root)
    if result.returncode != 0:
        failures.append(
            "build_agama_context.py failed:\n"
            f"stdout:\n{result.stdout}\n"
            f"stderr:\n{result.stderr}"
        )
        return
    after_first_run = {rel_path: _hash_file(root / rel_path) for rel_path in GENERATED_AGAMA_FILES}

    result = _run_build_agama(root)
    if result.returncode != 0:
        failures.append(
            "Second build_agama_context.py run failed:\n"
            f"stdout:\n{result.stdout}\n"
            f"stderr:\n{result.stderr}"
        )
        return
    after_second_run = {rel_path: _hash_file(root / rel_path) for rel_path in GENERATED_AGAMA_FILES}

    changed = [
        rel_path
        for rel_path in GENERATED_AGAMA_FILES
        if after_first_run[rel_path] != after_second_run[rel_path]
    ]
    if changed:
        failures.append("Agama Markdown generation is not idempotent: " + ", ".join(changed))
        return

    diff_result = subprocess.run(
        ["git", "diff", "--quiet", "--", *GENERATED_AGAMA_FILES],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )
    if diff_result.returncode != 0:
        failures.append(
            "Generated Agama Markdown differs from committed content. "
            "Run scripts/build_agama_context.py and review the diff."
        )


def run_checks(
    root: Path = ROOT,
    *,
    check_generated: bool = False,
    strict_yaml: bool = False,
) -> tuple[list[str], list[str]]:
    failures: list[str] = []
    warnings: list[str] = []
    root = root.resolve()

    _check_paths(root, failures)
    _check_version_consistency(root, failures)
    _check_regression_matrix(root, failures)
    _check_regression_cases_yaml(root, failures, warnings, strict_yaml)
    _check_agent_prompts(root, failures)
    _check_readme_platform_validation_links(root, failures)
    _check_public_style_boundaries(root, failures)
    _check_runtime_validation_log(root, failures)
    _check_runtime_evidence_docs(root, failures)
    _check_portable_upgrade_doc(root, failures)
    _check_yaml(root, failures, warnings, strict_yaml)
    _check_agama_search(root, failures)
    if check_generated:
        _check_generated_agama(root, failures)
    return failures, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate zilan-agent repository invariants.")
    parser.add_argument("--root", type=Path, default=ROOT, help="Repository root.")
    parser.add_argument(
        "--check-generated",
        action="store_true",
        help="Rebuild Agama Markdown and fail if generated files change.",
    )
    parser.add_argument(
        "--strict-yaml",
        action="store_true",
        help="Fail when PyYAML is unavailable instead of warning.",
    )
    args = parser.parse_args()

    failures, warnings = run_checks(
        args.root,
        check_generated=args.check_generated,
        strict_yaml=args.strict_yaml,
    )
    for warning in warnings:
        print(f"WARN: {warning}")
    if failures:
        print("zilan-agent validation failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("zilan-agent validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
