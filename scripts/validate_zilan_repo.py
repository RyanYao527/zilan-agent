from __future__ import annotations

import argparse
import hashlib
import re
import subprocess
import sys
from pathlib import Path

from zilanlib.agama.search import DEFAULT_FALSE_POSITIVE_PHRASES, search_agama

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
    "docs/runtime-evidence/2026-06-16-volcengine-openai-compatible-zc-01-zc-03-live.md",
    "docs/runtime-evidence/2026-06-16-volcengine-openai-compatible-zc-02-live.md",
    "docs/maintenance-roadmap.md",
    "docs/installation.md",
    "docs/validation-evidence.md",
    "docs/provider-routes.md",
    "docs/openai-api-harness.md",
    "docs/architecture/reasoning-contract.md",
    "docs/architecture/reasoning-contract-review.md",
    "docs/architecture/semantic-retrieval-interface.md",
    "LICENSE",
    "THIRD_PARTY_NOTICES.md",
    "CONTRIBUTING.md",
    "CONTRIBUTING-en.md",
    "agents/openai.yaml",
    "agents/zilan-claude-code.md",
    "agents/zilan-codex.md",
    "scripts/agama_evidence_checker.py",
    "scripts/build_agama_context.py",
    "scripts/cognitive_analysis_mapper.py",
    "scripts/collected_topics_analyzer.py",
    "scripts/hetuvidya_validator.py",
    "scripts/madhyamaka_critique_engine.py",
    "scripts/mock_install_smoke.py",
    "scripts/openai_api_harness.py",
    "scripts/reasoning_contract_runner.py",
    "scripts/reasoning_validator_output.py",
    "scripts/search_agama.py",
    "scripts/semantic_answer_boundary_review.py",
    "scripts/semantic_answer_contract_review.py",
    "scripts/semantic_context_bundle.py",
    "scripts/semantic_fixture_candidates.py",
    "scripts/semantic_fixture_review.py",
    "scripts/semantic_retrieval_dry_run.py",
    "scripts/semantic_role_coverage.py",
    "scripts/validate_zilan_repo.py",
    "scripts/zilanlib/__init__.py",
    "scripts/zilanlib/agama/__init__.py",
    "scripts/zilanlib/agama/candidates.py",
    "scripts/zilanlib/agama/fixture_review.py",
    "scripts/zilanlib/agama/search.py",
    "scripts/zilanlib/semantic/__init__.py",
    "scripts/zilanlib/semantic/answer_boundary_review.py",
    "scripts/zilanlib/semantic/answer_contract_review.py",
    "scripts/zilanlib/semantic/context_bundle.py",
    "scripts/zilanlib/semantic/role_coverage.py",
    "scripts/zilanlib/yaml_io.py",
    "tests/regression_cases.yaml",
    "tests/reasoning_cases.yaml",
    "tests/fixtures/retrieval_chunks/semantic_chunks.yaml",
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
REASONING_CASES_PATH = "tests/reasoning_cases.yaml"
RETRIEVAL_CHUNKS_PATH = "tests/fixtures/retrieval_chunks/semantic_chunks.yaml"
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
THIRD_PARTY_NOTICES_DOC = "THIRD_PARTY_NOTICES.md"
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
ALLOWED_REASONING_CONTRACTS = (
    "agama_evidence",
    "cognitive_analysis",
    "collected_topics",
    "hetuvidya",
    "madhyamaka_prasanga",
)
ALLOWED_HETUVIDYA_RESULTS = (
    "positive_reason",
    "reason_unestablished",
    "non_pervasive",
    "inconclusive_or_contradictory",
    "boundary_only",
)
ALLOWED_REASONING_CHECK_STATUSES = ("pass", "fail", "boundary", "not_applicable")
ALLOWED_RETRIEVAL_CHUNK_TYPES = ("agama_passage", "argument_unit", "context_topic", "reasoning_case")
ALLOWED_RETRIEVAL_NEEDS = (*ALLOWED_REASONING_CONTRACTS, "practice_boundary")
ALLOWED_RETRIEVAL_NON_CHUNK_NEEDS = ("practice_boundary",)
ALLOWED_ANSWER_SAMPLE_STATUSES = ("pass", "fail")
RETRIEVAL_HASH_ALGORITHM = "sha256"
RETRIEVAL_SOURCE_SCRIPT = "scripts/search_agama.py"
RETRIEVAL_SOURCE_HASH_SCOPE = "legacy_alias_for_line_text_hash"
RETRIEVAL_LINE_TEXT_HASH_SCOPE = "trimmed_non_empty_lines_joined_with_lf"
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
        "不要把文件写入作为主要交付方式",
        "Codex 阿含检索规范",
        "引用阿含经时必须注明",
        "阿含证据输出契约",
        "检索范围",
        "代表性",
        "待校勘",
        "context/agama/",
        "雜阿含經",
        "摄类学总别边界输出契约",
        "总与别",
        "局部别法",
        "整体总法",
        "总别混淆",
        "不周遍",
        "心类学与观禅实修边界输出契约",
        "颠倒知",
        "犹豫识",
        "比量",
        "无瞋",
        "行舍",
        "名色分别",
        "缘摄受",
        "三相印证",
        "非心理治疗",
        "善知识指导",
        "中观应成输出契约",
        "对方承许",
        "自性有",
        "归谬",
        "缘起",
        "矛盾",
        "不立自宗",
        "只破自性有",
        "断灭",
        "二谛",
        "不是虚无主义",
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
        "不要用 `Write` 作为主要交付方式",
        "引用阿含经时必须注明",
        "阿含证据输出契约",
        "检索范围",
        "代表性",
        "待校勘",
        "context/agama/",
        "雜阿含經",
        "摄类学总别边界输出契约",
        "总与别",
        "局部别法",
        "整体总法",
        "总别混淆",
        "不周遍",
        "心类学与观禅实修边界输出契约",
        "颠倒知",
        "犹豫识",
        "比量",
        "无瞋",
        "行舍",
        "名色分别",
        "缘摄受",
        "三相印证",
        "非心理治疗",
        "善知识指导",
        "中观应成输出契约",
        "对方承许",
        "自性有",
        "归谬",
        "缘起",
        "矛盾",
        "不立自宗",
        "只破自性有",
        "断灭",
        "二谛",
        "不是虚无主义",
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


def _is_non_empty_string_list(value: object) -> bool:
    return isinstance(value, list) and bool(value) and all(isinstance(item, str) and item for item in value)


def _is_non_empty_int_list(value: object) -> bool:
    return isinstance(value, list) and bool(value) and all(
        isinstance(item, int) and not isinstance(item, bool) for item in value
    )


def _retrieval_line_text_hash(source_lines: list[str], start_line: int, end_line: int) -> str:
    text = "\n".join(line.strip() for line in source_lines[start_line - 1 : end_line] if line.strip())
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    return f"{RETRIEVAL_HASH_ALGORITHM}:{digest}"


def _check_agama_passage_provenance(
    *,
    chunk_id: str,
    metadata: dict[str, object],
    source_file: str,
    start_line: int,
    end_line: int,
    source_lines: list[str],
    failures: list[str],
) -> None:
    expected_hash = _retrieval_line_text_hash(source_lines, start_line, end_line)
    source_hash = metadata.get("source_hash")
    line_text_hash = metadata.get("line_text_hash")

    if source_hash != expected_hash:
        failures.append(f"{RETRIEVAL_CHUNKS_PATH} {chunk_id} metadata.source_hash must match source range hash.")
    if line_text_hash != expected_hash:
        failures.append(f"{RETRIEVAL_CHUNKS_PATH} {chunk_id} metadata.line_text_hash must match source range hash.")
    if source_hash != line_text_hash:
        failures.append(f"{RETRIEVAL_CHUNKS_PATH} {chunk_id} metadata.source_hash must equal line_text_hash.")

    matched_lines = metadata.get("matched_lines")
    matched_lines_valid = _is_non_empty_int_list(matched_lines)
    if not matched_lines_valid:
        failures.append(f"{RETRIEVAL_CHUNKS_PATH} {chunk_id} metadata.matched_lines must be a line-number list.")
    else:
        out_of_range = [line for line in matched_lines if line < start_line or line > end_line]
        if out_of_range:
            failures.append(
                f"{RETRIEVAL_CHUNKS_PATH} {chunk_id} metadata.matched_lines must fall within the line range."
            )

    provenance = metadata.get("provenance")
    if not isinstance(provenance, dict):
        failures.append(f"{RETRIEVAL_CHUNKS_PATH} {chunk_id} metadata.provenance must be a mapping.")
        return

    if provenance.get("source_script") != RETRIEVAL_SOURCE_SCRIPT:
        failures.append(
            f"{RETRIEVAL_CHUNKS_PATH} {chunk_id} metadata.provenance.source_script must be "
            f"{RETRIEVAL_SOURCE_SCRIPT}."
        )
    if provenance.get("source_file") != source_file:
        failures.append(f"{RETRIEVAL_CHUNKS_PATH} {chunk_id} metadata.provenance.source_file must match source_file.")
    if provenance.get("line_range") != {"start": start_line, "end": end_line}:
        failures.append(f"{RETRIEVAL_CHUNKS_PATH} {chunk_id} metadata.provenance.line_range must match line range.")
    if matched_lines_valid and provenance.get("matched_lines") != matched_lines:
        failures.append(
            f"{RETRIEVAL_CHUNKS_PATH} {chunk_id} metadata.provenance.matched_lines must match metadata.matched_lines."
        )
    if provenance.get("hash_algorithm") != RETRIEVAL_HASH_ALGORITHM:
        failures.append(
            f"{RETRIEVAL_CHUNKS_PATH} {chunk_id} metadata.provenance.hash_algorithm must be "
            f"{RETRIEVAL_HASH_ALGORITHM}."
        )
    if provenance.get("line_text_hash") != expected_hash:
        failures.append(
            f"{RETRIEVAL_CHUNKS_PATH} {chunk_id} metadata.provenance.line_text_hash must match source range hash."
        )
    if provenance.get("source_hash_scope") != RETRIEVAL_SOURCE_HASH_SCOPE:
        failures.append(
            f"{RETRIEVAL_CHUNKS_PATH} {chunk_id} metadata.provenance.source_hash_scope must be "
            f"{RETRIEVAL_SOURCE_HASH_SCOPE}."
        )
    if provenance.get("line_text_hash_scope") != RETRIEVAL_LINE_TEXT_HASH_SCOPE:
        failures.append(
            f"{RETRIEVAL_CHUNKS_PATH} {chunk_id} metadata.provenance.line_text_hash_scope must be "
            f"{RETRIEVAL_LINE_TEXT_HASH_SCOPE}."
        )


def _check_hetuvidya_contract(case_id: str, expected: dict[str, object], failures: list[str]) -> None:
    hetuvidya = expected.get("hetuvidya")
    if not isinstance(hetuvidya, dict):
        failures.append(f"{REASONING_CASES_PATH} {case_id} missing expected.hetuvidya mapping.")
        return

    for field in ("subject", "predicate", "reason"):
        if not isinstance(hetuvidya.get(field), str) or not hetuvidya[field]:
            failures.append(f"{REASONING_CASES_PATH} {case_id} expected.hetuvidya.{field} must be a string.")

    result = hetuvidya.get("result")
    if result not in ALLOWED_HETUVIDYA_RESULTS:
        failures.append(
            f"{REASONING_CASES_PATH} {case_id} expected.hetuvidya.result must be one of "
            f"{', '.join(ALLOWED_HETUVIDYA_RESULTS)}."
        )

    checks = hetuvidya.get("checks")
    if not isinstance(checks, dict):
        failures.append(f"{REASONING_CASES_PATH} {case_id} missing expected.hetuvidya.checks mapping.")
        return

    for field in ("paksa_dharmata", "sapaksa_sattva", "vipaksa_asattva"):
        if checks.get(field) not in ALLOWED_REASONING_CHECK_STATUSES:
            failures.append(
                f"{REASONING_CASES_PATH} {case_id} expected.hetuvidya.checks.{field} must be one of "
                f"{', '.join(ALLOWED_REASONING_CHECK_STATUSES)}."
            )


def _check_collected_topics_contract(case_id: str, expected: dict[str, object], failures: list[str]) -> None:
    collected_topics = expected.get("collected_topics")
    if not isinstance(collected_topics, dict):
        failures.append(f"{REASONING_CASES_PATH} {case_id} missing expected.collected_topics mapping.")
        return

    if not _is_non_empty_string_list(collected_topics.get("concepts")):
        failures.append(f"{REASONING_CASES_PATH} {case_id} expected.collected_topics.concepts must be a list.")
    relation_checks = collected_topics.get("relation_checks")
    if not isinstance(relation_checks, dict) or not relation_checks:
        failures.append(
            f"{REASONING_CASES_PATH} {case_id} expected.collected_topics.relation_checks must be a mapping."
        )
    error_type = collected_topics.get("error_type")
    if error_type is not None and (not isinstance(error_type, str) or not error_type):
        failures.append(f"{REASONING_CASES_PATH} {case_id} expected.collected_topics.error_type must be a string.")


def _check_cognitive_analysis_contract(case_id: str, expected: dict[str, object], failures: list[str]) -> None:
    cognitive_analysis = expected.get("cognitive_analysis")
    if not isinstance(cognitive_analysis, dict):
        failures.append(f"{REASONING_CASES_PATH} {case_id} missing expected.cognitive_analysis mapping.")
        return

    chain = cognitive_analysis.get("chain")
    if chain != ["触", "作意", "受", "想", "思"]:
        failures.append(
            f"{REASONING_CASES_PATH} {case_id} expected.cognitive_analysis.chain must be "
            "['触', '作意', '受', '想', '思']."
        )
    for field in ("afflictions", "corrective_factors"):
        if not _is_non_empty_string_list(cognitive_analysis.get(field)):
            failures.append(
                f"{REASONING_CASES_PATH} {case_id} expected.cognitive_analysis.{field} must be a list."
            )


def _check_madhyamaka_prasanga_contract(case_id: str, expected: dict[str, object], failures: list[str]) -> None:
    madhyamaka_prasanga = expected.get("madhyamaka_prasanga")
    if not isinstance(madhyamaka_prasanga, dict):
        failures.append(f"{REASONING_CASES_PATH} {case_id} missing expected.madhyamaka_prasanga mapping.")
        return

    if not isinstance(madhyamaka_prasanga.get("opponent_premise"), str) or not madhyamaka_prasanga[
        "opponent_premise"
    ]:
        failures.append(
            f"{REASONING_CASES_PATH} {case_id} expected.madhyamaka_prasanga.opponent_premise must be a string."
        )
    for field in ("accepted_commitments", "contradiction"):
        if not _is_non_empty_string_list(madhyamaka_prasanga.get(field)):
            failures.append(
                f"{REASONING_CASES_PATH} {case_id} expected.madhyamaka_prasanga.{field} must be a list."
            )
    if madhyamaka_prasanga.get("no_independent_thesis") is not True:
        failures.append(
            f"{REASONING_CASES_PATH} {case_id} expected.madhyamaka_prasanga.no_independent_thesis must be true."
        )


def _check_agama_evidence_contract(case_id: str, expected: dict[str, object], failures: list[str]) -> None:
    agama_evidence = expected.get("agama_evidence")
    if not isinstance(agama_evidence, dict):
        failures.append(f"{REASONING_CASES_PATH} {case_id} missing expected.agama_evidence mapping.")
        return

    for field in ("citation_required", "collation_boundary"):
        if not isinstance(agama_evidence.get(field), bool):
            failures.append(f"{REASONING_CASES_PATH} {case_id} expected.agama_evidence.{field} must be boolean.")
    if not isinstance(agama_evidence.get("search_scope"), str) or not agama_evidence["search_scope"]:
        failures.append(f"{REASONING_CASES_PATH} {case_id} expected.agama_evidence.search_scope must be a string.")


def _check_retrieval_chunk_metadata(
    case_id: str,
    chunk_type: object,
    metadata: object,
    failures: list[str],
    *,
    source_file: str | None = None,
    start_line: int | None = None,
    end_line: int | None = None,
    source_lines: list[str] | None = None,
) -> None:
    if not isinstance(metadata, dict):
        failures.append(f"{RETRIEVAL_CHUNKS_PATH} {case_id} metadata must be a mapping.")
        return

    if not _is_non_empty_string_list(metadata.get("topics")):
        failures.append(f"{RETRIEVAL_CHUNKS_PATH} {case_id} metadata.topics must be a list.")

    roles = metadata.get("reasoning_roles")
    if not _is_non_empty_string_list(roles):
        failures.append(f"{RETRIEVAL_CHUNKS_PATH} {case_id} metadata.reasoning_roles must be a list.")
    else:
        invalid_roles = [role for role in roles if role not in ALLOWED_REASONING_CONTRACTS]
        if invalid_roles:
            failures.append(f"{RETRIEVAL_CHUNKS_PATH} {case_id} has invalid reasoning roles: {invalid_roles}")

    if chunk_type == "agama_passage":
        for field in ("collection", "cbeta_id", "juan"):
            if not isinstance(metadata.get(field), str) or not metadata[field]:
                failures.append(f"{RETRIEVAL_CHUNKS_PATH} {case_id} metadata.{field} must be a string.")
        cbeta_id = metadata.get("cbeta_id")
        if isinstance(cbeta_id, str) and not re.fullmatch(r"T\d{2}n\d{4}", cbeta_id):
            failures.append(f"{RETRIEVAL_CHUNKS_PATH} {case_id} metadata.cbeta_id is not a CBETA id.")
        if (
            isinstance(source_file, str)
            and isinstance(start_line, int)
            and isinstance(end_line, int)
            and isinstance(source_lines, list)
        ):
            _check_agama_passage_provenance(
                chunk_id=case_id,
                metadata=metadata,
                source_file=source_file,
                start_line=start_line,
                end_line=end_line,
                source_lines=source_lines,
                failures=failures,
            )


def _check_answer_samples(
    root: Path,
    query_id: str,
    samples: object,
    field_name: str,
    failures: list[str],
) -> None:
    if not isinstance(samples, list) or not samples:
        failures.append(f"{RETRIEVAL_CHUNKS_PATH} {query_id} {field_name} must be a non-empty list.")
        return

    seen_sample_ids: set[str] = set()
    for sample in samples:
        if not isinstance(sample, dict):
            failures.append(f"{RETRIEVAL_CHUNKS_PATH} {query_id} contains a non-mapping {field_name} item.")
            continue

        sample_id = sample.get("id")
        if not isinstance(sample_id, str) or not re.fullmatch(r"[a-z0-9][a-z0-9-]*", sample_id):
            failures.append(f"{RETRIEVAL_CHUNKS_PATH} {query_id} {field_name} id must be kebab-case.")
        elif sample_id in seen_sample_ids:
            failures.append(f"{RETRIEVAL_CHUNKS_PATH} {query_id} contains duplicate {field_name} id: {sample_id}")
        else:
            seen_sample_ids.add(sample_id)

        rel_file = sample.get("file")
        if not isinstance(rel_file, str) or not rel_file:
            failures.append(f"{RETRIEVAL_CHUNKS_PATH} {query_id} {field_name} {sample_id} missing file.")
        else:
            sample_path = root / rel_file
            try:
                sample_path.resolve().relative_to(root.resolve())
            except ValueError:
                failures.append(
                    f"{RETRIEVAL_CHUNKS_PATH} {query_id} {field_name} {sample_id} file must stay under repo root."
                )
            if not sample_path.exists() or not sample_path.is_file():
                failures.append(
                    f"{RETRIEVAL_CHUNKS_PATH} {query_id} {field_name} {sample_id} file missing: {rel_file}"
                )
            elif not sample_path.read_text(encoding="utf-8").strip():
                failures.append(
                    f"{RETRIEVAL_CHUNKS_PATH} {query_id} {field_name} {sample_id} file is empty: {rel_file}"
                )

        expected_status = sample.get("expected_status")
        if expected_status not in ALLOWED_ANSWER_SAMPLE_STATUSES:
            failures.append(
                f"{RETRIEVAL_CHUNKS_PATH} {query_id} {field_name} {sample_id} expected_status must be one of "
                f"{', '.join(ALLOWED_ANSWER_SAMPLE_STATUSES)}."
            )


def _check_answer_contracts(query_id: str, contracts: object, field_name: str, failures: list[str]) -> None:
    if not isinstance(contracts, dict) or not contracts:
        failures.append(f"{RETRIEVAL_CHUNKS_PATH} {query_id} {field_name} must be a non-empty mapping.")
        return

    for key, contract in contracts.items():
        if not isinstance(key, str) or not re.fullmatch(r"[a-z0-9][a-z0-9_]*", key):
            failures.append(f"{RETRIEVAL_CHUNKS_PATH} {query_id} {field_name} key must be snake_case.")
            continue
        if not isinstance(contract, dict):
            failures.append(f"{RETRIEVAL_CHUNKS_PATH} {query_id} {field_name}.{key} must be a mapping.")
            continue
        if not isinstance(contract.get("description"), str) or not contract["description"]:
            failures.append(f"{RETRIEVAL_CHUNKS_PATH} {query_id} {field_name}.{key}.description must be a string.")
        if not _is_non_empty_string_list(contract.get("required_terms")):
            failures.append(f"{RETRIEVAL_CHUNKS_PATH} {query_id} {field_name}.{key}.required_terms must be a list.")
        forbidden_terms = contract.get("forbidden_terms", [])
        if forbidden_terms and not _is_non_empty_string_list(forbidden_terms):
            failures.append(
                f"{RETRIEVAL_CHUNKS_PATH} {query_id} {field_name}.{key}.forbidden_terms "
                "must be a list when present."
            )
        required_slots = contract.get("required_slots", [])
        if required_slots:
            if not isinstance(required_slots, list):
                failures.append(
                    f"{RETRIEVAL_CHUNKS_PATH} {query_id} {field_name}.{key}.required_slots "
                    "must be a list when present."
                )
                continue
            for index, slot in enumerate(required_slots):
                if not isinstance(slot, dict):
                    failures.append(
                        f"{RETRIEVAL_CHUNKS_PATH} {query_id} {field_name}.{key}.required_slots[{index}] "
                        "must be a mapping."
                    )
                    continue
                label = slot.get("label")
                if not isinstance(label, str) or not re.fullmatch(r"[a-z0-9][a-z0-9_]*", label):
                    failures.append(
                        f"{RETRIEVAL_CHUNKS_PATH} {query_id} {field_name}.{key}.required_slots[{index}].label "
                        "must be snake_case."
                    )
                if not _is_non_empty_string_list(slot.get("terms")):
                    failures.append(
                        f"{RETRIEVAL_CHUNKS_PATH} {query_id} {field_name}.{key}.required_slots[{index}].terms "
                        "must be a non-empty string list."
                    )


def _check_retrieval_queries(
    root: Path,
    queries: object,
    chunk_ids: set[str],
    failures: list[str],
) -> None:
    if not isinstance(queries, list) or not queries:
        failures.append(f"{RETRIEVAL_CHUNKS_PATH} must contain a non-empty queries list.")
        return

    seen_query_ids: set[str] = set()
    for item in queries:
        if not isinstance(item, dict):
            failures.append(f"{RETRIEVAL_CHUNKS_PATH} contains a non-mapping query.")
            continue

        query_id = item.get("id")
        if not isinstance(query_id, str) or not re.fullmatch(r"SRQ-\d{2}", query_id):
            failures.append(f"{RETRIEVAL_CHUNKS_PATH} contains a query without an SRQ-XX id.")
            continue
        if query_id in seen_query_ids:
            failures.append(f"{RETRIEVAL_CHUNKS_PATH} contains duplicate query id: {query_id}")
        seen_query_ids.add(query_id)

        if not isinstance(item.get("query"), str) or not item["query"]:
            failures.append(f"{RETRIEVAL_CHUNKS_PATH} {query_id} query must be a string.")

        needs = item.get("needs")
        if not _is_non_empty_string_list(needs):
            failures.append(f"{RETRIEVAL_CHUNKS_PATH} {query_id} needs must be a list.")
        else:
            invalid_needs = [need for need in needs if need not in ALLOWED_RETRIEVAL_NEEDS]
            if invalid_needs:
                failures.append(f"{RETRIEVAL_CHUNKS_PATH} {query_id} has invalid needs: {invalid_needs}")

        non_chunk_needs = item.get("non_chunk_needs", [])
        if non_chunk_needs:
            if not _is_non_empty_string_list(non_chunk_needs):
                failures.append(f"{RETRIEVAL_CHUNKS_PATH} {query_id} non_chunk_needs must be a list.")
            else:
                invalid_non_chunk_needs = [
                    need for need in non_chunk_needs if need not in ALLOWED_RETRIEVAL_NON_CHUNK_NEEDS
                ]
                if invalid_non_chunk_needs:
                    failures.append(
                        f"{RETRIEVAL_CHUNKS_PATH} {query_id} has invalid non_chunk_needs: "
                        f"{invalid_non_chunk_needs}"
                    )
                missing_non_chunk_needs = [need for need in non_chunk_needs if need not in needs]
                if missing_non_chunk_needs:
                    failures.append(
                        f"{RETRIEVAL_CHUNKS_PATH} {query_id} non_chunk_needs are not listed in needs: "
                        f"{missing_non_chunk_needs}"
                    )

        answer_boundary_contracts = item.get("answer_boundary_contracts", {})
        if answer_boundary_contracts:
            if not isinstance(answer_boundary_contracts, dict):
                failures.append(f"{RETRIEVAL_CHUNKS_PATH} {query_id} answer_boundary_contracts must be a mapping.")
            elif not non_chunk_needs:
                failures.append(
                    f"{RETRIEVAL_CHUNKS_PATH} {query_id} answer_boundary_contracts requires non_chunk_needs."
                )
            else:
                invalid_contract_keys = [
                    key for key in answer_boundary_contracts if not isinstance(key, str) or key not in non_chunk_needs
                ]
                if invalid_contract_keys:
                    failures.append(
                        f"{RETRIEVAL_CHUNKS_PATH} {query_id} has answer boundary contracts outside "
                        f"non_chunk_needs: {invalid_contract_keys}"
                    )
                for key, contract in answer_boundary_contracts.items():
                    if not isinstance(contract, dict):
                        failures.append(
                            f"{RETRIEVAL_CHUNKS_PATH} {query_id} answer_boundary_contracts.{key} must be a mapping."
                        )
                        continue
                    if not isinstance(contract.get("description"), str) or not contract["description"]:
                        failures.append(
                            f"{RETRIEVAL_CHUNKS_PATH} {query_id} answer_boundary_contracts.{key}.description "
                            "must be a string."
                        )
                    if not _is_non_empty_string_list(contract.get("required_terms")):
                        failures.append(
                            f"{RETRIEVAL_CHUNKS_PATH} {query_id} answer_boundary_contracts.{key}.required_terms "
                            "must be a list."
                        )
                    forbidden_terms = contract.get("forbidden_terms", [])
                    if forbidden_terms and not _is_non_empty_string_list(forbidden_terms):
                        failures.append(
                            f"{RETRIEVAL_CHUNKS_PATH} {query_id} answer_boundary_contracts.{key}.forbidden_terms "
                            "must be a list when present."
                        )

        if "answer_boundary_samples" in item:
            if not answer_boundary_contracts:
                failures.append(
                    f"{RETRIEVAL_CHUNKS_PATH} {query_id} answer_boundary_samples requires "
                    "answer_boundary_contracts."
                )
            _check_answer_samples(
                root,
                query_id,
                item.get("answer_boundary_samples"),
                "answer_boundary_samples",
                failures,
            )

        answer_contracts = item.get("answer_contracts", {})
        if answer_contracts:
            _check_answer_contracts(query_id, answer_contracts, "answer_contracts", failures)

        if "answer_contract_samples" in item:
            if not answer_contracts:
                failures.append(
                    f"{RETRIEVAL_CHUNKS_PATH} {query_id} answer_contract_samples requires answer_contracts."
                )
            _check_answer_samples(
                root,
                query_id,
                item.get("answer_contract_samples"),
                "answer_contract_samples",
                failures,
            )

        keywords = item.get("keywords")
        if not isinstance(keywords, dict):
            failures.append(f"{RETRIEVAL_CHUNKS_PATH} {query_id} keywords must be a mapping.")
        else:
            for field in ("classical", "modern"):
                if not _is_non_empty_string_list(keywords.get(field)):
                    failures.append(f"{RETRIEVAL_CHUNKS_PATH} {query_id} keywords.{field} must be a list.")

        expected_sources = item.get("expected_sources")
        if not _is_non_empty_string_list(expected_sources):
            failures.append(f"{RETRIEVAL_CHUNKS_PATH} {query_id} expected_sources must be a list.")
        else:
            for rel_path in expected_sources:
                normalized = rel_path.rstrip("/")
                if not (root / normalized).exists():
                    failures.append(f"{RETRIEVAL_CHUNKS_PATH} {query_id} source missing: {rel_path}")

        expected_chunk_ids = item.get("expected_chunk_ids")
        if not _is_non_empty_string_list(expected_chunk_ids):
            failures.append(f"{RETRIEVAL_CHUNKS_PATH} {query_id} expected_chunk_ids must be a list.")
        else:
            missing = [chunk_id for chunk_id in expected_chunk_ids if chunk_id not in chunk_ids]
            if missing:
                failures.append(f"{RETRIEVAL_CHUNKS_PATH} {query_id} unknown expected chunks: {missing}")


def _check_retrieval_chunks_yaml(root: Path, failures: list[str], warnings: list[str], strict_yaml: bool) -> None:
    data = _load_yaml(root, RETRIEVAL_CHUNKS_PATH, failures, warnings, strict_yaml)
    if data is None:
        return
    if not isinstance(data, dict):
        failures.append(f"{RETRIEVAL_CHUNKS_PATH} must be a mapping.")
        return
    if data.get("version") != 1:
        failures.append(f"{RETRIEVAL_CHUNKS_PATH} version must be 1.")

    source = data.get("source")
    if not isinstance(source, str) or not (root / source).exists():
        failures.append(f"{RETRIEVAL_CHUNKS_PATH} source must reference an existing local file.")
    if not isinstance(data.get("purpose"), str) or not data["purpose"]:
        failures.append(f"{RETRIEVAL_CHUNKS_PATH} purpose must be a non-empty string.")

    chunks = data.get("chunks")
    if not isinstance(chunks, list) or not chunks:
        failures.append(f"{RETRIEVAL_CHUNKS_PATH} must contain a non-empty chunks list.")
        return

    chunk_ids: set[str] = set()
    for item in chunks:
        if not isinstance(item, dict):
            failures.append(f"{RETRIEVAL_CHUNKS_PATH} contains a non-mapping chunk.")
            continue

        chunk_id = item.get("chunk_id")
        if not isinstance(chunk_id, str) or not chunk_id:
            failures.append(f"{RETRIEVAL_CHUNKS_PATH} contains a chunk without a string id.")
            continue
        if chunk_id in chunk_ids:
            failures.append(f"{RETRIEVAL_CHUNKS_PATH} contains duplicate chunk id: {chunk_id}")
        chunk_ids.add(chunk_id)

        chunk_type = item.get("chunk_type")
        if chunk_type not in ALLOWED_RETRIEVAL_CHUNK_TYPES:
            failures.append(f"{RETRIEVAL_CHUNKS_PATH} {chunk_id} has invalid chunk_type: {chunk_type}")

        source_file = item.get("source_file")
        if not isinstance(source_file, str) or not (root / source_file).exists():
            failures.append(f"{RETRIEVAL_CHUNKS_PATH} {chunk_id} source_file must exist.")
            continue

        start_line = item.get("start_line")
        end_line = item.get("end_line")
        if not isinstance(start_line, int) or not isinstance(end_line, int) or start_line < 1 or end_line < start_line:
            failures.append(f"{RETRIEVAL_CHUNKS_PATH} {chunk_id} line range is invalid.")
            continue

        lines = (root / source_file).read_text(encoding="utf-8").splitlines()
        if end_line > len(lines):
            failures.append(f"{RETRIEVAL_CHUNKS_PATH} {chunk_id} line range exceeds source length.")
            continue

        snippet = item.get("text")
        if not isinstance(snippet, str) or not snippet:
            failures.append(f"{RETRIEVAL_CHUNKS_PATH} {chunk_id} text must be a string.")
        else:
            selected = "\n".join(lines[start_line - 1 : end_line])
            if snippet not in selected:
                failures.append(f"{RETRIEVAL_CHUNKS_PATH} {chunk_id} text is not present in source range.")

        for field in ("citation", "passage_citation"):
            value = item.get(field)
            if not isinstance(value, str) or source_file not in value or f":{start_line}" not in value:
                failures.append(f"{RETRIEVAL_CHUNKS_PATH} {chunk_id} {field} must include the local line anchor.")

        _check_retrieval_chunk_metadata(
            chunk_id,
            chunk_type,
            item.get("metadata"),
            failures,
            source_file=source_file,
            start_line=start_line,
            end_line=end_line,
            source_lines=lines,
        )

    _check_retrieval_queries(root, data.get("queries"), chunk_ids, failures)


def _check_reasoning_cases_yaml(root: Path, failures: list[str], warnings: list[str], strict_yaml: bool) -> None:
    data = _load_yaml(root, REASONING_CASES_PATH, failures, warnings, strict_yaml)
    if data is None:
        return
    if not isinstance(data, dict):
        failures.append(f"{REASONING_CASES_PATH} must be a mapping.")
        return
    if data.get("version") != 1:
        failures.append(f"{REASONING_CASES_PATH} version must be 1.")

    source = data.get("source")
    if not isinstance(source, str) or not (root / source).exists():
        failures.append(f"{REASONING_CASES_PATH} source must reference an existing local file.")
    if not isinstance(data.get("purpose"), str) or not data["purpose"]:
        failures.append(f"{REASONING_CASES_PATH} purpose must be a non-empty string.")

    cases = data.get("cases")
    if not isinstance(cases, list) or not cases:
        failures.append(f"{REASONING_CASES_PATH} must contain a non-empty cases list.")
        return

    seen_ids: set[str] = set()
    for item in cases:
        if not isinstance(item, dict):
            failures.append(f"{REASONING_CASES_PATH} contains a non-mapping case.")
            continue

        case_id = item.get("id")
        if not isinstance(case_id, str) or not re.fullmatch(r"ZR-\d{2}", case_id):
            failures.append(f"{REASONING_CASES_PATH} contains a case without a ZR-XX id.")
            continue
        if case_id in seen_ids:
            failures.append(f"{REASONING_CASES_PATH} contains duplicate case id: {case_id}")
        seen_ids.add(case_id)

        for field in ("title", "prompt"):
            if not isinstance(item.get(field), str) or not item[field]:
                failures.append(f"{REASONING_CASES_PATH} {case_id} missing string field: {field}")

        source_regression_cases = item.get("source_regression_cases", [])
        if not isinstance(source_regression_cases, list) or not all(
            isinstance(case, str) and case in REGRESSION_CASES for case in source_regression_cases
        ):
            failures.append(
                f"{REASONING_CASES_PATH} {case_id} source_regression_cases must reference known ZC cases."
            )

        contracts = item.get("contracts")
        if not isinstance(contracts, list) or not contracts:
            failures.append(f"{REASONING_CASES_PATH} {case_id} contracts must be a non-empty list.")
            continue
        invalid_contracts = [
            contract
            for contract in contracts
            if not isinstance(contract, str) or contract not in ALLOWED_REASONING_CONTRACTS
        ]
        if invalid_contracts:
            failures.append(f"{REASONING_CASES_PATH} {case_id} has invalid contracts: {invalid_contracts}")

        reference_files = item.get("reference_files")
        if not isinstance(reference_files, list) or not reference_files:
            failures.append(f"{REASONING_CASES_PATH} {case_id} reference_files must be a non-empty list.")
        else:
            for rel_path in reference_files:
                if not isinstance(rel_path, str) or not (root / rel_path).exists():
                    failures.append(f"{REASONING_CASES_PATH} {case_id} references missing path: {rel_path}")

        expected = item.get("expected")
        if not isinstance(expected, dict):
            failures.append(f"{REASONING_CASES_PATH} {case_id} missing expected mapping.")
            continue
        if not isinstance(expected.get("boundary_statement"), bool):
            failures.append(f"{REASONING_CASES_PATH} {case_id} expected.boundary_statement must be boolean.")
        if not _is_non_empty_string_list(expected.get("structure")):
            failures.append(f"{REASONING_CASES_PATH} {case_id} expected.structure must be a list.")

        if "hetuvidya" in contracts:
            _check_hetuvidya_contract(case_id, expected, failures)
        if "collected_topics" in contracts:
            _check_collected_topics_contract(case_id, expected, failures)
        if "cognitive_analysis" in contracts:
            _check_cognitive_analysis_contract(case_id, expected, failures)
        if "madhyamaka_prasanga" in contracts:
            _check_madhyamaka_prasanga_contract(case_id, expected, failures)
        if "agama_evidence" in contracts:
            _check_agama_evidence_contract(case_id, expected, failures)


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


def _check_third_party_notices(root: Path, failures: list[str]) -> None:
    notice_text = (root / THIRD_PARTY_NOTICES_DOC).read_text(encoding="utf-8")
    required_notice_fragments = (
        "CBETA XML-P5",
        "https://github.com/cbeta-org/xml-p5",
        "https://www.cbeta.org/copyright.php",
        "context/agama/_source/",
        "context/agama/T0099-za-agama.md",
        "not relicensed under the MIT License",
    )
    for fragment in required_notice_fragments:
        if fragment not in notice_text:
            failures.append(f"{THIRD_PARTY_NOTICES_DOC} missing required fragment: {fragment}")

    license_text = (root / "LICENSE").read_text(encoding="utf-8")
    for fragment in ("Repository License Scope", "CBETA-derived", THIRD_PARTY_NOTICES_DOC):
        if fragment not in license_text:
            failures.append(f"LICENSE missing third-party scope fragment: {fragment}")

    for rel_path in README_FILES:
        text = (root / rel_path).read_text(encoding="utf-8")
        if THIRD_PARTY_NOTICES_DOC not in text:
            failures.append(f"{rel_path} should link to {THIRD_PARTY_NOTICES_DOC}.")
        if "CBETA" not in text:
            failures.append(f"{rel_path} should mention CBETA for Agama third-party material.")

def _check_skill_script_inventory(root: Path, failures: list[str]) -> None:
    script_paths = sorted(path.relative_to(root).as_posix() for path in (root / "scripts").rglob("*.py"))
    for rel_path in ("SKILL.md", "SKILL-en.md"):
        text = (root / rel_path).read_text(encoding="utf-8")
        for script_path in script_paths:
            script_name = Path(script_path).name
            if script_path not in text and script_name not in text:
                failures.append(f"{rel_path} missing script inventory entry: {script_path}")

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
    _check_reasoning_cases_yaml(root, failures, warnings, strict_yaml)
    _check_retrieval_chunks_yaml(root, failures, warnings, strict_yaml)
    _check_agent_prompts(root, failures)
    _check_readme_platform_validation_links(root, failures)
    _check_third_party_notices(root, failures)
    _check_skill_script_inventory(root, failures)
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
