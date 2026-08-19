from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from zilanlib.text_checks import check_required_fragments
from zilanlib.yaml_io import load_yaml_for_validation

REGRESSION_CASES = ("ZC-01", "ZC-02", "ZC-03", "ZC-04", "ZC-05", "ZC-06")
RUNTIME_VALIDATION_LOG_DOC = "docs/runtime-validation-log.md"
RUNTIME_EVIDENCE_INDEX_DOC = "docs/runtime-evidence/README.md"
RUNTIME_EVIDENCE_NAV_INDEX_DOC = "docs/runtime-evidence/index.md"
RUNTIME_EVIDENCE_MANIFEST_DOC = "docs/runtime-evidence/evidence_manifest.yaml"
RUNTIME_EVIDENCE_TEMPLATE_DOC = "docs/runtime-evidence/evidence-template.md"
RUNTIME_EVIDENCE_CLEAN_INSTALL_DOC = "docs/runtime-evidence/2026-06-15-clean-install-smoke.md"
RUNTIME_EVIDENCE_MOCK_INSTALL_DOC = "docs/runtime-evidence/2026-06-15-mock-claude-install-smoke.md"
_RUNTIME_EVIDENCE_FILE_REF_RE = re.compile(r"`([^`]+(?:\.md|\.yaml))`")
_CASE_ID_RE = re.compile(r"^(?:SRQ|ZC|ZR)-\d{2}$")
_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
ALLOWED_EVIDENCE_CLASSES = {
    "standalone_answer_excerpt",
    "batch_manifest",
    "batch_report",
    "summary_only",
    "provider_smoke",
    "manual_collation",
}
NON_ANSWER_FILE_SAFE_EVIDENCE_CLASSES = {
    "batch_manifest",
    "batch_report",
    "manual_collation",
    "provider_smoke",
    "summary_only",
}
ALLOWED_REVIEW_STATUSES = {
    "fail",
    "fail_expected",
    "manual_review_required",
    "not_reviewed",
    "partial",
    "pass",
    "runtime_pending",
}


def validate_runtime_evidence(root: Path, failures: list[str]) -> None:
    check_runtime_validation_log(root, failures)
    check_runtime_evidence_docs(root, failures)
    validate_runtime_evidence_manifest(root, failures)


def check_runtime_validation_log(root: Path, failures: list[str]) -> None:
    text = (root / RUNTIME_VALIDATION_LOG_DOC).read_text(encoding="utf-8")
    required_fragments = (
        "2026-06-10",
        "Codex",
        "CODEX_REGRESSION_TESTS.md",
        "docs/platform-validation.md",
        "Transcript status",
    )
    check_required_fragments(text, required_fragments, failures, rel_path=RUNTIME_VALIDATION_LOG_DOC)
    for case in REGRESSION_CASES:
        if case not in text:
            failures.append(f"{RUNTIME_VALIDATION_LOG_DOC} missing regression case: {case}")
    if RUNTIME_EVIDENCE_CLEAN_INSTALL_DOC not in text:
        failures.append(f"{RUNTIME_VALIDATION_LOG_DOC} should link to {RUNTIME_EVIDENCE_CLEAN_INSTALL_DOC}.")
    if RUNTIME_EVIDENCE_MOCK_INSTALL_DOC not in text:
        failures.append(f"{RUNTIME_VALIDATION_LOG_DOC} should link to {RUNTIME_EVIDENCE_MOCK_INSTALL_DOC}.")


def runtime_evidence_rel_path_from_ref(ref: str) -> str | None:
    normalized = ref.replace("\\", "/")
    if "<" in normalized or ">" in normalized:
        return None
    if normalized.startswith("docs/runtime-evidence/"):
        return normalized
    if "/" not in normalized and (normalized.endswith(".md") or normalized.endswith(".yaml")):
        return f"docs/runtime-evidence/{normalized}"
    return None


def runtime_evidence_refs_from_text(text: str) -> set[str]:
    refs: set[str] = set()
    for match in _RUNTIME_EVIDENCE_FILE_REF_RE.finditer(text):
        rel_path = runtime_evidence_rel_path_from_ref(match.group(1))
        if rel_path is not None:
            refs.add(rel_path)
    return refs


def markdown_section(text: str, heading: str) -> str:
    section_lines: list[str] = []
    in_section = False
    for line in text.splitlines():
        if line.startswith("## "):
            if in_section:
                break
            in_section = line[3:].strip() == heading
            continue
        if in_section:
            section_lines.append(line)
    return "\n".join(section_lines)


def runtime_evidence_summary_only_refs(index_text: str) -> set[str]:
    summary_section = markdown_section(index_text, "Summary-Only Runtime Evidence")
    return runtime_evidence_refs_from_text(summary_section)


def check_runtime_evidence_index_references(root: Path, index_text: str, failures: list[str]) -> None:
    for rel_path in sorted(runtime_evidence_refs_from_text(index_text)):
        if not (root / rel_path).exists():
            failures.append(
                f"{RUNTIME_EVIDENCE_NAV_INDEX_DOC} references missing runtime evidence file: {Path(rel_path).name}"
            )


def check_runtime_evidence_batch_manifests(
    root: Path,
    failures: list[str],
    *,
    summary_only_refs: set[str],
) -> None:
    evidence_dir = root / "docs" / "runtime-evidence"
    for batch_path in sorted(evidence_dir.glob("*batch.yaml")):
        rel_path = batch_path.relative_to(root).as_posix()
        warnings: list[str] = []
        data = load_yaml_for_validation(root, rel_path, failures, warnings, strict_yaml=True)
        if data is None:
            continue
        if not isinstance(data, dict):
            failures.append(f"{rel_path} must be a YAML mapping.")
            continue
        reviews = data.get("reviews")
        if not isinstance(reviews, list):
            failures.append(f"{rel_path} reviews must be a list.")
            continue
        for index, review in enumerate(reviews):
            if not isinstance(review, dict):
                failures.append(f"{rel_path} reviews[{index}] must be a mapping.")
                continue
            review_id = review.get("id")
            if not isinstance(review_id, str) or not review_id:
                review_id = f"reviews[{index}]"
            answer_file = review.get("answer_file")
            if not isinstance(answer_file, str) or not answer_file:
                continue
            normalized_answer_file = answer_file.replace("\\", "/")
            if not (root / normalized_answer_file).exists():
                failures.append(f"{rel_path} review {review_id} answer_file missing: {normalized_answer_file}")
            if normalized_answer_file in summary_only_refs:
                failures.append(
                    f"{rel_path} review {review_id} uses summary-only evidence as answer_file: "
                    f"{normalized_answer_file}"
                )


def _entry_label(entry: dict[str, Any], index: int) -> str:
    entry_id = entry.get("id")
    if isinstance(entry_id, str) and entry_id:
        return f"entry {entry_id}"
    return f"entries[{index}]"


def _require_string(
    value: object,
    *,
    field: str,
    label: str,
    failures: list[str],
) -> str | None:
    if not isinstance(value, str) or not value:
        failures.append(f"{RUNTIME_EVIDENCE_MANIFEST_DOC} {label}.{field} must be a non-empty string.")
        return None
    return value


def _require_bool(
    value: object,
    *,
    field: str,
    label: str,
    failures: list[str],
) -> bool | None:
    if not isinstance(value, bool):
        failures.append(f"{RUNTIME_EVIDENCE_MANIFEST_DOC} {label}.{field} must be true or false.")
        return None
    return value


def _require_string_list(
    value: object,
    *,
    field: str,
    label: str,
    failures: list[str],
) -> list[str]:
    if not isinstance(value, list) or not value or not all(isinstance(item, str) and item for item in value):
        failures.append(f"{RUNTIME_EVIDENCE_MANIFEST_DOC} {label}.{field} must be a non-empty string list.")
        return []
    return list(value)


def _check_case_ids(
    values: list[str],
    *,
    field: str,
    label: str,
    failures: list[str],
) -> None:
    for value in values:
        if not _CASE_ID_RE.match(value):
            failures.append(f"{RUNTIME_EVIDENCE_MANIFEST_DOC} {label}.{field} must use SRQ-*, ZC-*, or ZR-* ids.")


def _check_optional_manifest_file_ref(
    root: Path,
    value: object,
    *,
    field: str,
    label: str,
    failures: list[str],
) -> None:
    if value is None:
        return
    if not isinstance(value, str) or not value:
        failures.append(f"{RUNTIME_EVIDENCE_MANIFEST_DOC} {label}.{field} must be a non-empty string when present.")
        return
    normalized = value.replace("\\", "/")
    if normalized.startswith("docs/runtime-evidence/") and not (root / normalized).exists():
        failures.append(f"{RUNTIME_EVIDENCE_MANIFEST_DOC} {label}.{field} file missing: {normalized}")


def _check_manifest_review(
    root: Path,
    review: object,
    *,
    entry_label: str,
    review_index: int,
    failures: list[str],
) -> None:
    review_label = f"{entry_label} reviews[{review_index}]"
    if not isinstance(review, dict):
        failures.append(f"{RUNTIME_EVIDENCE_MANIFEST_DOC} {review_label} must be a mapping.")
        return

    query_id = _require_string(review.get("query_id"), field="query_id", label=review_label, failures=failures)
    if query_id is not None and not _CASE_ID_RE.match(query_id):
        failures.append(
            f"{RUNTIME_EVIDENCE_MANIFEST_DOC} {review_label}.query_id must start with SRQ-, ZC-, or ZR-."
        )

    status = _require_string(review.get("status"), field="status", label=review_label, failures=failures)
    if status is not None and status not in ALLOWED_REVIEW_STATUSES:
        allowed = ", ".join(sorted(ALLOWED_REVIEW_STATUSES))
        failures.append(f"{RUNTIME_EVIDENCE_MANIFEST_DOC} {review_label}.status must be one of: {allowed}.")

    _check_optional_manifest_file_ref(
        root,
        review.get("source_file"),
        field="source_file",
        label=review_label,
        failures=failures,
    )
    _check_optional_manifest_file_ref(root, review.get("batch"), field="batch", label=review_label, failures=failures)
    notes = review.get("notes")
    if notes is not None and not isinstance(notes, str):
        failures.append(f"{RUNTIME_EVIDENCE_MANIFEST_DOC} {review_label}.notes must be a string when present.")


def _check_manifest_entry(root: Path, entry: object, *, index: int, failures: list[str]) -> None:
    if not isinstance(entry, dict):
        failures.append(f"{RUNTIME_EVIDENCE_MANIFEST_DOC} entries[{index}] must be a mapping.")
        return

    entry_label = _entry_label(entry, index)
    _require_string(entry.get("id"), field="id", label=entry_label, failures=failures)
    file_ref = _require_string(entry.get("file"), field="file", label=entry_label, failures=failures)
    if file_ref is not None:
        normalized_file = file_ref.replace("\\", "/")
        if not (root / normalized_file).exists():
            failures.append(f"{RUNTIME_EVIDENCE_MANIFEST_DOC} {entry_label} file missing: {normalized_file}")

    date_value = _require_string(entry.get("date"), field="date", label=entry_label, failures=failures)
    if date_value is not None and not _DATE_RE.match(date_value):
        failures.append(f"{RUNTIME_EVIDENCE_MANIFEST_DOC} {entry_label}.date must use YYYY-MM-DD.")

    evidence_class = _require_string(
        entry.get("evidence_class"),
        field="evidence_class",
        label=entry_label,
        failures=failures,
    )
    if evidence_class is not None and evidence_class not in ALLOWED_EVIDENCE_CLASSES:
        allowed = ", ".join(sorted(ALLOWED_EVIDENCE_CLASSES))
        failures.append(f"{RUNTIME_EVIDENCE_MANIFEST_DOC} {entry_label}.evidence_class must be one of: {allowed}.")

    related_cases = _require_string_list(
        entry.get("related_cases"),
        field="related_cases",
        label=entry_label,
        failures=failures,
    )
    _check_case_ids(related_cases, field="related_cases", label=entry_label, failures=failures)

    answer_file_safe = _require_bool(
        entry.get("answer_file_safe"),
        field="answer_file_safe",
        label=entry_label,
        failures=failures,
    )
    if (
        evidence_class in NON_ANSWER_FILE_SAFE_EVIDENCE_CLASSES
        and answer_file_safe is True
    ):
        failures.append(
            f"{RUNTIME_EVIDENCE_MANIFEST_DOC} {entry_label} evidence_class {evidence_class} "
            "must not set answer_file_safe: true."
        )

    platform_status_change = _require_bool(
        entry.get("platform_status_change"),
        field="platform_status_change",
        label=entry_label,
        failures=failures,
    )
    if platform_status_change is True:
        failures.append(f"{RUNTIME_EVIDENCE_MANIFEST_DOC} {entry_label} platform_status_change must be false.")

    reviews = entry.get("reviews")
    if not isinstance(reviews, list) or not reviews:
        failures.append(f"{RUNTIME_EVIDENCE_MANIFEST_DOC} {entry_label}.reviews must be a non-empty list.")
        return
    for review_index, review in enumerate(reviews):
        _check_manifest_review(root, review, entry_label=entry_label, review_index=review_index, failures=failures)


def validate_runtime_evidence_manifest(root: Path, failures: list[str]) -> None:
    manifest_path = root / RUNTIME_EVIDENCE_MANIFEST_DOC
    if not manifest_path.exists():
        failures.append(f"{RUNTIME_EVIDENCE_MANIFEST_DOC} missing required runtime evidence manifest.")
        return

    warnings: list[str] = []
    data = load_yaml_for_validation(root, RUNTIME_EVIDENCE_MANIFEST_DOC, failures, warnings, strict_yaml=True)
    if data is None:
        return
    if not isinstance(data, dict):
        failures.append(f"{RUNTIME_EVIDENCE_MANIFEST_DOC} must be a YAML mapping.")
        return
    if data.get("version") != 1:
        failures.append(f"{RUNTIME_EVIDENCE_MANIFEST_DOC} version must be 1.")

    entries = data.get("entries")
    if not isinstance(entries, list) or not entries:
        failures.append(f"{RUNTIME_EVIDENCE_MANIFEST_DOC} entries must be a non-empty list.")
        return
    for index, entry in enumerate(entries):
        _check_manifest_entry(root, entry, index=index, failures=failures)


def check_runtime_evidence_docs(root: Path, failures: list[str]) -> None:
    index_text = (root / RUNTIME_EVIDENCE_INDEX_DOC).read_text(encoding="utf-8")
    nav_index_path = root / RUNTIME_EVIDENCE_NAV_INDEX_DOC
    if nav_index_path.exists():
        nav_index_text = nav_index_path.read_text(encoding="utf-8")
    else:
        failures.append(f"{RUNTIME_EVIDENCE_NAV_INDEX_DOC} missing required runtime evidence index.")
        nav_index_text = ""
    clean_install_text = (root / RUNTIME_EVIDENCE_CLEAN_INSTALL_DOC).read_text(encoding="utf-8")
    mock_install_text = (root / RUNTIME_EVIDENCE_MOCK_INSTALL_DOC).read_text(encoding="utf-8")
    template_text = (root / RUNTIME_EVIDENCE_TEMPLATE_DOC).read_text(encoding="utf-8")

    check_required_fragments(
        index_text,
        (
            "Runtime Evidence Excerpts",
            "Do not use this directory for",
            "standalone answer excerpt",
            "summary-only evidence must not be used as answer_file input",
            "docs/validation-evidence.md",
        ),
        failures,
        rel_path=RUNTIME_EVIDENCE_INDEX_DOC,
    )

    check_required_fragments(
        nav_index_text,
        (
            "Runtime Evidence Index",
            "Evidence Classes",
            "Summary-Only Runtime Evidence",
            "Review Commands",
        ),
        failures,
        rel_path=RUNTIME_EVIDENCE_NAV_INDEX_DOC,
    )
    check_runtime_evidence_index_references(root, nav_index_text, failures)
    check_runtime_evidence_batch_manifests(
        root,
        failures,
        summary_only_refs=runtime_evidence_summary_only_refs(nav_index_text),
    )
    check_required_fragments(
        clean_install_text,
        (
            "2026-06-15 Clean Install Smoke Evidence",
            "zilan-agent validation passed.",
            "mode: dry-run",
            "Found 5 matches",
            "No secrets",
        ),
        failures,
        rel_path=RUNTIME_EVIDENCE_CLEAN_INSTALL_DOC,
    )

    check_required_fragments(
        mock_install_text,
        (
            "2026-06-15 Mock Claude Install Smoke Evidence",
            "mode: mock-claude-install",
            "skill:scripts/search_agama.py: pass",
            "agent:matches-source: pass",
            "Found 1 matches",
        ),
        failures,
        rel_path=RUNTIME_EVIDENCE_MOCK_INSTALL_DOC,
    )

    check_required_fragments(
        template_text,
        ("Redaction note", "Output Excerpts", "Standalone Answer Excerpts", "Limitations"),
        failures,
        rel_path=RUNTIME_EVIDENCE_TEMPLATE_DOC,
    )
