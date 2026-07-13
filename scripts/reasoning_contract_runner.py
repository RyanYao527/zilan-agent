from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import agama_evidence_checker
import cognitive_analysis_mapper
import collected_topics_analyzer
import hetuvidya_validator
import madhyamaka_critique_engine
from zilanlib.reasoning.contract_runner import build_reasoning_contract_run
from zilanlib.semantic.retrieval_dry_run import DEFAULT_FIXTURE, FixtureError


def _render_text(result: dict[str, Any]) -> str:
    answer_status = result["answer_review_status"]
    hetuvidya_status = result["validators"]["hetuvidya"]["status"]
    collected_topics_status = result["validators"]["collected_topics"]["status"]
    madhyamaka_prasanga_status = result["validators"]["madhyamaka_prasanga"]["status"]
    cognitive_analysis_status = result["validators"]["cognitive_analysis"]["status"]
    agama_evidence_status = result["validators"]["agama_evidence"]["status"]
    lines = [
        "# Reasoning Contract Runner",
        "",
        f"Query ID: {result['query_id']}",
        f"Query: {result['query']}",
        f"Overall status: {result['overall_status']}",
        f"Role coverage: {result['role_coverage']['coverage_status']}",
        f"Answer review: {answer_status}",
        f"Hetuvidya validator: {hetuvidya_status}",
        f"Collected Topics analyzer: {collected_topics_status}",
        f"Madhyamaka critique engine: {madhyamaka_prasanga_status}",
        f"Cognitive-analysis mapper: {cognitive_analysis_status}",
        f"Agama evidence checker: {agama_evidence_status}",
        "",
        "Boundary: local fixture runner only; this is not runtime platform validation.",
        "",
        "## Missing Needs",
    ]
    missing_needs = result["role_coverage"]["missing_needs"]
    if missing_needs:
        for need in missing_needs:
            lines.append(f"- {need}")
    else:
        lines.append("- none")

    lines.extend(["", "## Limitations"])
    for limitation in result["limitations"]:
        lines.append(f"- {limitation}")

    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        description="Run local fixture-based reasoning contract checks for a semantic query."
    )
    parser.add_argument("--fixture", type=Path, default=DEFAULT_FIXTURE, help="Semantic chunks fixture YAML path.")
    parser.add_argument(
        "--cases",
        type=Path,
        default=hetuvidya_validator.DEFAULT_CASES,
        help="Reasoning cases YAML path.",
    )
    parser.add_argument("--query-id", help="Query fixture id, such as SRQ-05.")
    parser.add_argument("--query", help="Exact query text to match from the fixture.")
    parser.add_argument("--limit", type=int, help="Maximum expected chunks to include before review.")
    parser.add_argument("--answer-text", help="Answer text to review against answer contracts.")
    parser.add_argument("--answer-file", type=Path, help="UTF-8 answer text file to review against answer contracts.")
    parser.add_argument("--sample-id", help="Checked-in answer contract sample id to review.")
    parser.add_argument("--json", action="store_true", dest="json_output", help="Emit machine-readable JSON.")
    args = parser.parse_args()

    try:
        result = build_reasoning_contract_run(
            args.fixture,
            args.cases,
            query_id=args.query_id,
            query=args.query,
            limit=args.limit,
            answer_text=args.answer_text,
            answer_file=args.answer_file,
            sample_id=args.sample_id,
        )
    except (
        FixtureError,
        hetuvidya_validator.HetuvidyaValidatorError,
        collected_topics_analyzer.CollectedTopicsAnalyzerError,
        madhyamaka_critique_engine.MadhyamakaCritiqueEngineError,
        cognitive_analysis_mapper.CognitiveAnalysisMapperError,
        agama_evidence_checker.AgamaEvidenceCheckerError,
    ) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    if args.json_output:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(_render_text(result), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
