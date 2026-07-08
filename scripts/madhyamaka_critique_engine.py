from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from reasoning_validator_output import build_validator_output

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CASES = ROOT / "tests" / "reasoning_cases.yaml"
VALIDATOR = "madhyamaka_critique_engine"
CONTRACT_FAMILY = "madhyamaka_prasanga"
MODE = "madhyamaka-critique-engine-v0"
OUTPUT_SCHEMA = "madhyamaka-critique-engine-output-v0"
LIMITATIONS = (
    "Prototype reads structured tests/reasoning_cases.yaml fixtures only.",
    "No natural-language dialectic parsing, provider calls, prompt changes, or ultimate-claim grading.",
)

STEP_DEFINITIONS = {
    "opponent_premise": {
        "role": "input_premise",
        "description": "The premise accepted for the sake of prasaṅga analysis.",
    },
    "accepted_commitments": {
        "role": "internal_commitments",
        "description": "Commitments used to derive consequences from the opponent premise.",
    },
    "contradiction": {
        "role": "derived_contradiction",
        "description": "Contradictions or untenable consequences exposed by the prasaṅga.",
    },
    "no_independent_thesis": {
        "role": "prasanga_boundary",
        "description": "Boundary that the critique does not establish an independent thesis.",
    },
}


class MadhyamakaCritiqueEngineError(ValueError):
    """Raised when the structured Madhyamaka fixture cannot be critiqued."""


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise MadhyamakaCritiqueEngineError(f"Reasoning cases not found: {_display_path(path)}")

    try:
        import yaml  # type: ignore[import-not-found]
    except ModuleNotFoundError as exc:
        raise MadhyamakaCritiqueEngineError("PyYAML is required to read reasoning cases.") from exc

    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001 - keep parser failures visible in CLI output.
        raise MadhyamakaCritiqueEngineError(
            f"Failed to parse reasoning cases {_display_path(path)}: {exc}"
        ) from exc

    if not isinstance(data, dict):
        raise MadhyamakaCritiqueEngineError(f"Reasoning cases must be a mapping: {_display_path(path)}")
    return data


def _case_list(data: dict[str, Any]) -> list[dict[str, Any]]:
    cases = data.get("cases")
    if not isinstance(cases, list) or not cases:
        raise MadhyamakaCritiqueEngineError("Reasoning cases must contain a non-empty cases list.")
    if not all(isinstance(item, dict) for item in cases):
        raise MadhyamakaCritiqueEngineError("Every reasoning case must be a mapping.")
    return cases


def _select_cases(cases: list[dict[str, Any]], case_id: str | None) -> list[dict[str, Any]]:
    if case_id is None:
        return [case for case in cases if "madhyamaka_prasanga" in case.get("contracts", [])]

    for case in cases:
        if case.get("id") == case_id:
            return [case]
    raise MadhyamakaCritiqueEngineError(f"Unknown reasoning case id: {case_id}")


def _string_list(value: Any, field: str, case_id: str) -> list[str]:
    if not isinstance(value, list) or not all(isinstance(item, str) and item for item in value):
        raise MadhyamakaCritiqueEngineError(f"{case_id} {field} must be a non-empty string list.")
    return list(value)


def _term_items(terms: list[str], role: str) -> list[dict[str, str]]:
    return [{"text": term, "role": role} for term in terms]


def _critique_steps(
    opponent_premise: str,
    accepted_commitments: list[str],
    contradiction: list[str],
    *,
    no_independent_thesis: bool,
) -> list[dict[str, Any]]:
    return [
        {
            "id": "opponent_premise",
            "role": STEP_DEFINITIONS["opponent_premise"]["role"],
            "description": STEP_DEFINITIONS["opponent_premise"]["description"],
            "content": opponent_premise,
            "status": "present",
        },
        {
            "id": "accepted_commitments",
            "role": STEP_DEFINITIONS["accepted_commitments"]["role"],
            "description": STEP_DEFINITIONS["accepted_commitments"]["description"],
            "content": accepted_commitments,
            "status": "present",
        },
        {
            "id": "contradiction",
            "role": STEP_DEFINITIONS["contradiction"]["role"],
            "description": STEP_DEFINITIONS["contradiction"]["description"],
            "content": contradiction,
            "status": "present",
        },
        {
            "id": "no_independent_thesis",
            "role": STEP_DEFINITIONS["no_independent_thesis"]["role"],
            "description": STEP_DEFINITIONS["no_independent_thesis"]["description"],
            "content": no_independent_thesis,
            "status": "required" if no_independent_thesis else "missing",
        },
    ]


def _diagnostics(no_independent_thesis: bool, boundary_required: bool) -> list[dict[str, Any]]:
    diagnostics: list[dict[str, Any]] = []
    if no_independent_thesis:
        diagnostics.append(
            {
                "code": "no_independent_thesis_required",
                "severity": "info",
                "message": "The fixture requires prasaṅga boundary language rather than an independent thesis.",
            }
        )
    else:
        diagnostics.append(
            {
                "code": "independent_thesis_boundary_missing",
                "severity": "warning",
                "message": "The fixture does not mark the no-independent-thesis boundary.",
            }
        )
    if boundary_required:
        diagnostics.append(
            {
                "code": "boundary_statement_required",
                "severity": "info",
                "message": "The fixture requires explicit boundary language.",
            }
        )
    return diagnostics


def _critique_case(case: dict[str, Any]) -> dict[str, Any]:
    case_id = case.get("id")
    expected = case.get("expected")
    if not isinstance(case_id, str) or not case_id:
        raise MadhyamakaCritiqueEngineError("Every selected reasoning case must have a non-empty id.")
    if not isinstance(expected, dict):
        raise MadhyamakaCritiqueEngineError(f"{case_id} expected must be a mapping.")

    madhyamaka = expected.get("madhyamaka_prasanga")
    if not isinstance(madhyamaka, dict):
        raise MadhyamakaCritiqueEngineError(f"{case_id} expected.madhyamaka_prasanga must be a mapping.")

    opponent_premise = madhyamaka.get("opponent_premise")
    if not isinstance(opponent_premise, str) or not opponent_premise:
        raise MadhyamakaCritiqueEngineError(
            f"{case_id} expected.madhyamaka_prasanga.opponent_premise must be a string."
        )

    accepted_commitments = _string_list(
        madhyamaka.get("accepted_commitments"),
        "expected.madhyamaka_prasanga.accepted_commitments",
        case_id,
    )
    contradiction = _string_list(
        madhyamaka.get("contradiction"),
        "expected.madhyamaka_prasanga.contradiction",
        case_id,
    )
    no_independent_thesis = bool(madhyamaka.get("no_independent_thesis", False))
    boundary_required = bool(expected.get("boundary_statement", False))

    return {
        "case_id": case_id,
        "title": case.get("title", ""),
        "prompt": case.get("prompt", ""),
        "source_regression_cases": case.get("source_regression_cases", []),
        "reference_files": case.get("reference_files", []),
        "boundary_statement_required": boundary_required,
        "structure": expected.get("structure", []),
        "madhyamaka_prasanga": {
            "opponent_premise": opponent_premise,
            "accepted_commitments": _term_items(accepted_commitments, "accepted_commitment"),
            "contradictions": _term_items(contradiction, "contradiction"),
            "no_independent_thesis": {
                "required": no_independent_thesis,
                "status": "required" if no_independent_thesis else "missing",
            },
            "critique_steps": _critique_steps(
                opponent_premise,
                accepted_commitments,
                contradiction,
                no_independent_thesis=no_independent_thesis,
            ),
        },
        "diagnostics": _diagnostics(no_independent_thesis, boundary_required),
    }


def build_madhyamaka_critique(
    cases_path: Path = DEFAULT_CASES,
    *,
    case_id: str | None = None,
) -> dict[str, Any]:
    """Return structured Madhyamaka prasaṅga critiques from checked-in reasoning cases."""

    data = _load_yaml(cases_path)
    selected = _select_cases(_case_list(data), case_id)
    if case_id is not None and "madhyamaka_prasanga" not in selected[0].get("contracts", []):
        raise MadhyamakaCritiqueEngineError(f"{case_id} is not a Madhyamaka prasaṅga reasoning case.")

    critiques = [_critique_case(case) for case in selected]

    return build_validator_output(
        validator=VALIDATOR,
        contract_family=CONTRACT_FAMILY,
        mode=MODE,
        output_schema=OUTPUT_SCHEMA,
        source=_display_path(cases_path),
        case_id=case_id,
        payload_key="critiques",
        payload=critiques,
        limitations=LIMITATIONS,
    )


def _render_text(result: dict[str, Any]) -> str:
    lines = [
        f"mode: {result['mode']}",
        f"source: {result['source']}",
    ]
    for item in result["critiques"]:
        madhyamaka = item["madhyamaka_prasanga"]
        commitments = "; ".join(term["text"] for term in madhyamaka["accepted_commitments"])
        contradictions = "; ".join(term["text"] for term in madhyamaka["contradictions"])
        lines.extend(
            [
                "",
                f"{item['case_id']}: {item['title']}",
                f"  prompt: {item['prompt']}",
                f"  opponent_premise: {madhyamaka['opponent_premise']}",
                f"  accepted_commitments: {commitments}",
                f"  contradictions: {contradictions}",
                f"  no_independent_thesis: {madhyamaka['no_independent_thesis']['status']}",
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
        description="Build structured Madhyamaka prasaṅga critiques from tests/reasoning_cases.yaml."
    )
    parser.add_argument("--cases", type=Path, default=DEFAULT_CASES, help="Reasoning cases YAML path.")
    parser.add_argument("--case-id", help="Reasoning case id, such as ZR-09.")
    parser.add_argument("--json", action="store_true", dest="json_output", help="Emit machine-readable JSON.")
    args = parser.parse_args()

    try:
        result = build_madhyamaka_critique(args.cases, case_id=args.case_id)
    except MadhyamakaCritiqueEngineError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    if args.json_output:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(_render_text(result), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
