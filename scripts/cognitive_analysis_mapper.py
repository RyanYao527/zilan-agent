from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CASES = ROOT / "tests" / "reasoning_cases.yaml"
MODE = "cognitive-analysis-mapper-v0"
OUTPUT_SCHEMA = "cognitive-analysis-mapper-output-v0"
LIMITATIONS = (
    "Prototype reads structured tests/reasoning_cases.yaml fixtures only.",
    "No natural-language parsing, provider calls, prompt changes, clinical advice, or doctrinal grading.",
)

CANONICAL_CHAIN = ["触", "作意", "受", "想", "思"]

CHAIN_STEP_DEFINITIONS = {
    "触": {
        "id": "contact",
        "role": "input_contact",
        "description": "Root, object, and consciousness come into contact.",
    },
    "作意": {
        "id": "attention",
        "role": "attention_orientation",
        "description": "Attention turns toward the selected object.",
    },
    "受": {
        "id": "feeling",
        "role": "feeling_tone",
        "description": "The experience is marked as pleasant, unpleasant, or neutral.",
    },
    "想": {
        "id": "perception",
        "role": "classification_labeling",
        "description": "The mind labels, classifies, and narrates the object.",
    },
    "思": {
        "id": "volition",
        "role": "volitional_response",
        "description": "Volition inclines the mind toward speech, action, reaction, or restraint.",
    },
}


class CognitiveAnalysisMapperError(ValueError):
    """Raised when the structured cognitive-analysis fixture cannot be mapped."""


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise CognitiveAnalysisMapperError(f"Reasoning cases not found: {_display_path(path)}")

    try:
        import yaml  # type: ignore[import-not-found]
    except ModuleNotFoundError as exc:
        raise CognitiveAnalysisMapperError("PyYAML is required to read reasoning cases.") from exc

    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001 - keep parser failures visible in CLI output.
        raise CognitiveAnalysisMapperError(
            f"Failed to parse reasoning cases {_display_path(path)}: {exc}"
        ) from exc

    if not isinstance(data, dict):
        raise CognitiveAnalysisMapperError(f"Reasoning cases must be a mapping: {_display_path(path)}")
    return data


def _case_list(data: dict[str, Any]) -> list[dict[str, Any]]:
    cases = data.get("cases")
    if not isinstance(cases, list) or not cases:
        raise CognitiveAnalysisMapperError("Reasoning cases must contain a non-empty cases list.")
    if not all(isinstance(item, dict) for item in cases):
        raise CognitiveAnalysisMapperError("Every reasoning case must be a mapping.")
    return cases


def _select_cases(cases: list[dict[str, Any]], case_id: str | None) -> list[dict[str, Any]]:
    if case_id is None:
        return [case for case in cases if "cognitive_analysis" in case.get("contracts", [])]

    for case in cases:
        if case.get("id") == case_id:
            return [case]
    raise CognitiveAnalysisMapperError(f"Unknown reasoning case id: {case_id}")


def _string_list(value: Any, field: str, case_id: str) -> list[str]:
    if not isinstance(value, list) or not all(isinstance(item, str) and item for item in value):
        raise CognitiveAnalysisMapperError(f"{case_id} {field} must be a non-empty string list.")
    return list(value)


def _chain_step(term: str) -> dict[str, Any]:
    definition = CHAIN_STEP_DEFINITIONS.get(term)
    if definition is None:
        return {
            "term": term,
            "id": "unknown",
            "role": "unknown",
            "description": "No canonical five-universal definition is registered for this term.",
            "status": "unknown",
        }
    return {
        "term": term,
        "id": definition["id"],
        "role": definition["role"],
        "description": definition["description"],
        "status": "mapped",
    }


def _term_items(terms: list[str], category: str) -> list[dict[str, str]]:
    return [{"term": term, "category": category} for term in terms]


def _diagnostics(chain: list[str], boundary_required: bool) -> list[dict[str, Any]]:
    diagnostics: list[dict[str, Any]] = []
    if chain != CANONICAL_CHAIN:
        diagnostics.append(
            {
                "code": "non_canonical_chain",
                "severity": "warning",
                "message": "The cognitive chain does not match the canonical five-universal sequence.",
            }
        )
    if boundary_required:
        diagnostics.append(
            {
                "code": "practice_boundary_required",
                "severity": "info",
                "message": "The fixture requires explicit practice-boundary language.",
            }
        )
    return diagnostics


def _map_case(case: dict[str, Any]) -> dict[str, Any]:
    case_id = case.get("id")
    expected = case.get("expected")
    if not isinstance(case_id, str) or not case_id:
        raise CognitiveAnalysisMapperError("Every selected reasoning case must have a non-empty id.")
    if not isinstance(expected, dict):
        raise CognitiveAnalysisMapperError(f"{case_id} expected must be a mapping.")

    cognitive_analysis = expected.get("cognitive_analysis")
    if not isinstance(cognitive_analysis, dict):
        raise CognitiveAnalysisMapperError(f"{case_id} expected.cognitive_analysis must be a mapping.")

    chain = _string_list(cognitive_analysis.get("chain"), "expected.cognitive_analysis.chain", case_id)
    afflictions = _string_list(
        cognitive_analysis.get("afflictions"),
        "expected.cognitive_analysis.afflictions",
        case_id,
    )
    corrective_factors = _string_list(
        cognitive_analysis.get("corrective_factors"),
        "expected.cognitive_analysis.corrective_factors",
        case_id,
    )
    boundary_required = bool(expected.get("boundary_statement", False))

    return {
        "case_id": case_id,
        "title": case.get("title", ""),
        "prompt": case.get("prompt", ""),
        "source_regression_cases": case.get("source_regression_cases", []),
        "reference_files": case.get("reference_files", []),
        "boundary_statement_required": boundary_required,
        "structure": expected.get("structure", []),
        "cognitive_analysis": {
            "chain": chain,
            "chain_steps": [_chain_step(term) for term in chain],
            "afflictions": _term_items(afflictions, "affliction"),
            "corrective_factors": _term_items(corrective_factors, "corrective_factor"),
            "practice_boundary": {
                "required": boundary_required,
                "status": "required" if boundary_required else "not_required",
            },
        },
        "diagnostics": _diagnostics(chain, boundary_required),
    }


def build_cognitive_analysis_mapping(
    cases_path: Path = DEFAULT_CASES,
    *,
    case_id: str | None = None,
) -> dict[str, Any]:
    """Return structured cognitive-analysis mappings from checked-in reasoning cases."""

    data = _load_yaml(cases_path)
    selected = _select_cases(_case_list(data), case_id)
    if case_id is not None and "cognitive_analysis" not in selected[0].get("contracts", []):
        raise CognitiveAnalysisMapperError(f"{case_id} is not a cognitive-analysis reasoning case.")

    mappings = [_map_case(case) for case in selected]

    return {
        "mode": MODE,
        "output_schema": OUTPUT_SCHEMA,
        "source": _display_path(cases_path),
        "case_id": case_id,
        "count": len(mappings),
        "mappings": mappings,
        "limitations": list(LIMITATIONS),
    }


def _render_text(result: dict[str, Any]) -> str:
    lines = [
        f"mode: {result['mode']}",
        f"source: {result['source']}",
    ]
    for item in result["mappings"]:
        cognitive = item["cognitive_analysis"]
        chain = " -> ".join(cognitive["chain"])
        afflictions = ", ".join(term["term"] for term in cognitive["afflictions"])
        corrective = ", ".join(term["term"] for term in cognitive["corrective_factors"])
        lines.extend(
            [
                "",
                f"{item['case_id']}: {item['title']}",
                f"  prompt: {item['prompt']}",
                f"  chain: {chain}",
                f"  afflictions: {afflictions}",
                f"  corrective_factors: {corrective}",
                f"  practice_boundary: {cognitive['practice_boundary']['status']}",
            ]
        )
        if item["diagnostics"]:
            lines.append("  diagnostics:")
            for diagnostic in item["diagnostics"]:
                lines.append(f"  - {diagnostic['code']}: {diagnostic['message']}")
    lines.extend(["", "limitations:"])
    for item in result["limitations"]:
        lines.append(f"- {item}")
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        description="Map structured cognitive-analysis reasoning cases from tests/reasoning_cases.yaml."
    )
    parser.add_argument("--cases", type=Path, default=DEFAULT_CASES, help="Reasoning cases YAML path.")
    parser.add_argument("--case-id", help="Reasoning case id, such as ZR-10.")
    parser.add_argument("--json", action="store_true", dest="json_output", help="Emit machine-readable JSON.")
    args = parser.parse_args()

    try:
        result = build_cognitive_analysis_mapping(args.cases, case_id=args.case_id)
    except CognitiveAnalysisMapperError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    if args.json_output:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(_render_text(result), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())