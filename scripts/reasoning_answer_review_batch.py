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
from zilanlib.reasoning.answer_review_batch import BatchReviewError, build_reasoning_answer_review_batch
from zilanlib.semantic.retrieval_dry_run import DEFAULT_FIXTURE, FixtureError


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        description="Build compact local answer reviews from a YAML batch manifest."
    )
    parser.add_argument("--batch", type=Path, required=True, help="Answer-review batch YAML manifest path.")
    parser.add_argument("--fixture", type=Path, default=DEFAULT_FIXTURE, help="Semantic chunks fixture YAML path.")
    parser.add_argument(
        "--cases",
        type=Path,
        default=hetuvidya_validator.DEFAULT_CASES,
        help="Reasoning cases YAML path.",
    )
    parser.add_argument("--json", action="store_true", dest="json_output", help="Emit machine-readable JSON.")
    args = parser.parse_args()

    try:
        result = build_reasoning_answer_review_batch(
            args.batch,
            fixture_path=args.fixture,
            cases_path=args.cases,
        )
    except (
        BatchReviewError,
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