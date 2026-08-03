from __future__ import annotations

from pathlib import Path

from zilanlib.text_checks import check_required_fragments

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
MAINTENANCE_ROADMAP_DOC = "docs/maintenance-roadmap.md"
INSTALLATION_DOC = "docs/installation.md"
VALIDATION_EVIDENCE_DOC = "docs/validation-evidence.md"
PROVIDER_ROUTES_DOC = "docs/provider-routes.md"
CHANGELOG_DOC = "CHANGELOG.md"
THIRD_PARTY_NOTICES_DOC = "THIRD_PARTY_NOTICES.md"
PORTABLE_UPGRADE_DOC = "AGENT_UPGRADE_PORTABLE.md"


def validate_public_docs(root: Path, failures: list[str]) -> None:
    check_readme_platform_validation_links(root, failures)
    check_third_party_notices(root, failures)
    check_skill_script_inventory(root, failures)
    check_public_style_boundaries(root, failures)
    check_portable_upgrade_doc(root, failures)


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


def check_third_party_notices(root: Path, failures: list[str]) -> None:
    notice_text = (root / THIRD_PARTY_NOTICES_DOC).read_text(encoding="utf-8")
    required_notice_fragments = (
        "CBETA XML-P5",
        "https://github.com/cbeta-org/xml-p5",
        "https://www.cbeta.org/copyright.php",
        "context/agama/_source/",
        "context/agama/T0099-za-agama.md",
        "not relicensed under the MIT License",
    )
    check_required_fragments(notice_text, required_notice_fragments, failures, rel_path=THIRD_PARTY_NOTICES_DOC)

    license_text = (root / "LICENSE").read_text(encoding="utf-8")
    check_required_fragments(
        license_text,
        ("Repository License Scope", "CBETA-derived", THIRD_PARTY_NOTICES_DOC),
        failures,
        rel_path="LICENSE",
        message="missing third-party scope fragment",
    )

    for rel_path in README_FILES:
        text = (root / rel_path).read_text(encoding="utf-8")
        if THIRD_PARTY_NOTICES_DOC not in text:
            failures.append(f"{rel_path} should link to {THIRD_PARTY_NOTICES_DOC}.")
        if "CBETA" not in text:
            failures.append(f"{rel_path} should mention CBETA for Agama third-party material.")


def check_skill_script_inventory(root: Path, failures: list[str]) -> None:
    script_paths = sorted(path.relative_to(root).as_posix() for path in (root / "scripts").rglob("*.py"))
    for rel_path in ("SKILL.md", "SKILL-en.md"):
        text = (root / rel_path).read_text(encoding="utf-8")
        for script_path in script_paths:
            script_name = Path(script_path).name
            if script_path not in text and script_name not in text:
                failures.append(f"{rel_path} missing script inventory entry: {script_path}")


def check_public_style_boundaries(root: Path, failures: list[str]) -> None:
    for rel_path in PUBLIC_STYLE_BOUNDARY_FILES:
        text = (root / rel_path).read_text(encoding="utf-8")
        for fragment in HIGH_RISK_PUBLIC_FRAGMENTS:
            if fragment in text:
                failures.append(f"{rel_path} contains private/autobiographical public fragment: {fragment}")


def check_portable_upgrade_doc(root: Path, failures: list[str]) -> None:
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
    check_required_fragments(text, required_fragments, failures, rel_path=PORTABLE_UPGRADE_DOC)


_check_readme_platform_validation_links = check_readme_platform_validation_links
_check_third_party_notices = check_third_party_notices
_check_skill_script_inventory = check_skill_script_inventory
_check_public_style_boundaries = check_public_style_boundaries
_check_portable_upgrade_doc = check_portable_upgrade_doc
_check_public_docs = validate_public_docs
