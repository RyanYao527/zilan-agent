from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import cognitive_analysis_mapper
import collected_topics_analyzer
import hetuvidya_validator
import madhyamaka_critique_engine
from zilanlib.reasoning.agama_evidence_checker import AgamaEvidenceCheckerError
from zilanlib.reasoning.answer_review import build_reasoning_answer_review
from zilanlib.semantic.retrieval_dry_run import DEFAULT_FIXTURE, FixtureError


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        description="Build a compact local answer review from reasoning contract fixtures."
    )
    parser.add_argument("--fixture", type=Path, default=DEFAULT_FIXTURE, help="Semantic chunks fixture YAML path.")
    parser.add_argument(
        "--cases",
        type=Path,
        default=hetuvidya_validator.DEFAULT_CASES,
        help="Reasoning cases YAML path.",
    )
    parser.add_argument("--query-id", help="Query fixture id, such as SRQ-04.")
    parser.add_argument("--query", help="Exact query text to match from the fixture.")
    parser.add_argument("--limit", type=int, help="Maximum expected chunks to include before review.")
    parser.add_argument("--answer-text", help="Answer text to review against answer contracts.")
    parser.add_argument("--answer-file", type=Path, help="UTF-8 answer text file to review against answer contracts.")
    parser.add_argument("--sample-id", help="Checked-in answer contract sample id to review.")
    parser.add_argument("--json", action="store_true", dest="json_output", help="Emit machine-readable JSON.")
    args = parser.parse_args()

    try:
        result = build_reasoning_answer_review(
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
        AgamaEvidenceCheckerError,
    ) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    if args.json_output:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(result["review_text"], end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
