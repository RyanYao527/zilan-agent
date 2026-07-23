from __future__ import annotations

import re
from pathlib import Path

from zilanlib.text_checks import check_required_fragments
from zilanlib.yaml_io import load_yaml_for_validation

REGRESSION_CASES = ("ZC-01", "ZC-02", "ZC-03", "ZC-04", "ZC-05", "ZC-06")
RUNTIME_VALIDATION_LOG_DOC = "docs/runtime-validation-log.md"
RUNTIME_EVIDENCE_INDEX_DOC = "docs/runtime-evidence/README.md"
RUNTIME_EVIDENCE_NAV_INDEX_DOC = "docs/runtime-evidence/index.md"
RUNTIME_EVIDENCE_TEMPLATE_DOC = "docs/runtime-evidence/evidence-template.md"
RUNTIME_EVIDENCE_CLEAN_INSTALL_DOC = "docs/runtime-evidence/2026-06-15-clean-install-smoke.md"
RUNTIME_EVIDENCE_MOCK_INSTALL_DOC = "docs/runtime-evidence/2026-06-15-mock-claude-install-smoke.md"
_RUNTIME_EVIDENCE_FILE_REF_RE = re.compile(r"`([^`]+(?:\.md|\.yaml))`")


def validate_runtime_evidence(root: Path, failures: list[str]) -> None:
    check_runtime_validation_log(root, failures)
    check_runtime_evidence_docs(root, failures)


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