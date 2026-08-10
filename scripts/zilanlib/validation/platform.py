from __future__ import annotations

from pathlib import Path

from zilanlib.validation import public_docs as public_docs_validation
from zilanlib.yaml_io import load_yaml_for_validation

README_FILES = public_docs_validation.README_FILES
PLATFORM_VALIDATION_DOC = "docs/platform-validation.md"
RUNTIME_VALIDATION_LOG_DOC = public_docs_validation.RUNTIME_VALIDATION_LOG_DOC
MAINTENANCE_ROADMAP_DOC = public_docs_validation.MAINTENANCE_ROADMAP_DOC
INSTALLATION_DOC = public_docs_validation.INSTALLATION_DOC
VALIDATION_EVIDENCE_DOC = public_docs_validation.VALIDATION_EVIDENCE_DOC
PROVIDER_ROUTES_DOC = public_docs_validation.PROVIDER_ROUTES_DOC
CHANGELOG_DOC = public_docs_validation.CHANGELOG_DOC
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


def validate_platform_yaml_metadata(
    root: Path,
    failures: list[str],
    warnings: list[str],
    strict_yaml: bool,
) -> None:
    validation = validate_platform_metadata(root, failures, warnings, strict_yaml)
    if not validation:
        return

    codex_validation = validation.get("codex")
    if not isinstance(codex_validation, dict) or codex_validation.get("status") != "tested":
        failures.append("agents/openai.yaml should mark validation.codex.status as tested.")


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


check_readme_platform_validation_links = public_docs_validation.check_readme_platform_validation_links
