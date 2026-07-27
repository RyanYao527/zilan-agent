from __future__ import annotations

from pathlib import Path

from zilanlib.yaml_io import load_yaml_for_validation

README_FILES = ("README.md", "README.zh.md", "README.en.md")
PLATFORM_VALIDATION_DOC = "docs/platform-validation.md"
RUNTIME_VALIDATION_LOG_DOC = "docs/runtime-validation-log.md"
MAINTENANCE_ROADMAP_DOC = "docs/maintenance-roadmap.md"
INSTALLATION_DOC = "docs/installation.md"
VALIDATION_EVIDENCE_DOC = "docs/validation-evidence.md"
PROVIDER_ROUTES_DOC = "docs/provider-routes.md"
CHANGELOG_DOC = "CHANGELOG.md"
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


def validate_platform_metadata(
    root: Path,
    failures: list[str],
    warnings: list[str],
    strict_yaml: bool,
) -> dict[str, object]:
    data = load_yaml_for_validation(root, "agents/openai.yaml", failures, warnings, strict_yaml)
    if data is None:
        return {}

    validation = get_validation_mapping(data, failures)
    if not validation:
        return {}

    check_agent_validation_entries(validation, failures)
    check_platform_validation_doc(root, validation, failures)
    return validation


def get_validation_mapping(data: object, failures: list[str]) -> dict[str, object]:
    if not isinstance(data, dict):
        failures.append("agents/openai.yaml must be a mapping.")
        return {}

    validation = data.get("validation")
    if not isinstance(validation, dict):
        failures.append("agents/openai.yaml missing validation mapping.")
        return {}
    return validation


def check_agent_validation_entries(validation: dict[str, object], failures: list[str]) -> None:
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


def parse_markdown_table_rows(text: str) -> dict[str, list[str]]:
    rows: dict[str, list[str]] = {}
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|") or set(stripped.replace("|", "").strip()) <= {"-", ":"}:
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if len(cells) >= 2:
            rows[cells[0]] = cells
    return rows


def check_platform_validation_doc(root: Path, validation: dict[str, object], failures: list[str]) -> None:
    doc_text = (root / PLATFORM_VALIDATION_DOC).read_text(encoding="utf-8")
    rows = parse_markdown_table_rows(doc_text)

    for status in ALLOWED_VALIDATION_STATUSES:
        if f"| `{status}` |" not in doc_text:
            failures.append(f"{PLATFORM_VALIDATION_DOC} missing status definition: {status}")

    for provider, label in PLATFORM_VALIDATION_LABELS.items():
        entry = validation.get(provider)
        if not isinstance(entry, dict):
            continue

        entry_status = entry.get("status")
        if not isinstance(entry_status, str):
            continue

        row = rows.get(label)
        if row is None:
            failures.append(f"{PLATFORM_VALIDATION_DOC} missing platform row: {label}")
            continue
        if len(row) < 3:
            failures.append(f"{PLATFORM_VALIDATION_DOC} platform row is incomplete: {label}")
            continue
        if row[1] != f"`{entry_status}`":
            failures.append(
                f"{PLATFORM_VALIDATION_DOC} status mismatch for {label}: "
                f"expected `{entry_status}` from agents/openai.yaml, got {row[1]}."
            )

        date = entry.get("date")
        if entry_status == "tested" and isinstance(date, str) and row[2] != date:
            failures.append(
                f"{PLATFORM_VALIDATION_DOC} validation date mismatch for {label}: "
                f"expected {date} from agents/openai.yaml, got {row[2]}."
            )


def check_readme_platform_validation_links(root: Path, failures: list[str]) -> None:
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