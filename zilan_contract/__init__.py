"""
zilan-contract: Deterministic output-contract validators for LLM responses.

A lightweight Python library that checks LLM outputs against structured
contracts — required terms, forbidden phrases, and boundary statements —
without calling any model or API.

Quick start::

    from zilan_contract import ContractRunner

    runner = ContractRunner()
    result = runner.check(
        query_id="SRQ-04",
        sample_id="srq04-agama-citation-boundary-pass",
    )
    print(result.overall_status)  # 'pass'

See docs/zilan-contract-quickstart.md for the full guide.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Ensure the bundled zilanlib is importable in both dev and installed modes.
_scripts_dir = Path(__file__).resolve().parents[1] / "scripts"
if _scripts_dir.is_dir() and str(_scripts_dir) not in sys.path:
    sys.path.insert(0, str(_scripts_dir))

from zilanlib.repository import detect_source_root  # noqa: E402

from zilan_contract.answer_contracts import (  # noqa: E402
    AnswerContractResult,
    AnswerContractRunner,
    AnswerContractSchemaError,
    validate_contracts,
)
from zilan_contract.results import ContractIssue, ContractResult  # noqa: E402

__version__ = "2.5.6"
__all__ = [
    "AnswerContractResult",
    "AnswerContractRunner",
    "AnswerContractSchemaError",
    "ContractIssue",
    "ContractRunner",
    "ContractResult",
    "HetuvidyaValidator",
    "get_fixture_path",
    "get_cases_path",
    "validate_contracts",
    "__version__",
]

_FIXTURE_DIR = Path(__file__).resolve().parent / "fixtures"
_CASES_FILE = _FIXTURE_DIR / "reasoning_cases.yaml"
_SEMANTIC_FIXTURE = _FIXTURE_DIR / "retrieval_chunks" / "semantic_chunks.yaml"

# Fallback to project layout during development
_PROJECT_ROOT = Path(__file__).resolve().parents[1]
_DEV_FIXTURES = _PROJECT_ROOT / "tests" / "fixtures"
_DEV_CASES = _PROJECT_ROOT / "tests" / "reasoning_cases.yaml"
_DEFAULT_SOURCE_ROOT = detect_source_root(_PROJECT_ROOT)


def get_fixture_path(name: str = "semantic_chunks.yaml") -> Path:
    """Return the path to a bundled fixture file.

    Resolves fixtures whether installed as a pip package or running
    from the zilan-agent repository root in development mode.
    """
    if name == "semantic_chunks.yaml":
        if _SEMANTIC_FIXTURE.exists():
            return _SEMANTIC_FIXTURE
        dev_path = _DEV_FIXTURES / "retrieval_chunks" / "semantic_chunks.yaml"
        if dev_path.exists():
            return dev_path
        raise FileNotFoundError(f"Fixture '{name}' not found. Tried: {_SEMANTIC_FIXTURE}, {dev_path}")

    dev_path = _DEV_FIXTURES / name
    if dev_path.exists():
        return dev_path

    bundled = _FIXTURE_DIR / name
    if bundled.exists():
        return bundled

    raise FileNotFoundError(f"Fixture '{name}' not found. Tried: {bundled}, {dev_path}")


def get_cases_path() -> Path:
    """Return the path to reasoning_cases.yaml."""
    if _CASES_FILE.exists():
        return _CASES_FILE
    if _DEV_CASES.exists():
        return _DEV_CASES
    raise FileNotFoundError(f"Reasoning cases not found. Tried: {_CASES_FILE}, {_DEV_CASES}")


class ContractRunner:
    """Run output-contract checks against an LLM response.

    This is the main entry point. It wraps the reasoning contract runner
    with automatic fixture resolution.

    Usage::

        runner = ContractRunner()
        result = runner.check(
            query_id="SRQ-04",
            sample_id="srq04-agama-citation-boundary-pass",
        )

    Parameters
    ----------
    fixture_path:
        Override the default semantic fixture path.
    cases_path:
        Override the default reasoning cases path.
    source_root:
        Optional source checkout root for repository-only local evidence checks. If absent, bundled package fixtures
        mark local Agama source-anchor checks as not_applicable.
    """

    def __init__(
        self,
        fixture_path: Path | None = None,
        cases_path: Path | None = None,
        source_root: Path | None = _DEFAULT_SOURCE_ROOT,
    ):
        self._fixture_path = fixture_path or get_fixture_path()
        self._cases_path = cases_path or get_cases_path()
        self._source_root = source_root

    def check(
        self,
        *,
        query_id: str | None = None,
        query: str | None = None,
        limit: int | None = None,
        answer_text: str | None = None,
        answer_file: Path | None = None,
        sample_id: str | None = None,
    ) -> ContractResult:
        """Run contract checks and return a structured result.

        Provide exactly one of *answer_text*, *answer_file*, or *sample_id*.
        """
        from zilanlib.reasoning.contract_runner import (
            build_reasoning_contract_run,
        )

        raw = build_reasoning_contract_run(
            fixture_path=self._fixture_path,
            cases_path=self._cases_path,
            query_id=query_id,
            query=query,
            limit=limit,
            answer_text=answer_text,
            answer_file=answer_file,
            sample_id=sample_id,
            source_root=self._source_root,
        )
        return ContractResult(raw)


class HetuvidyaValidator:
    """Standalone Hetuvidya (Buddhist logic) validator.

    Checks whether a structured argument satisfies the three marks
    (因三相) of Buddhist logic, deterministically, from YAML fixtures.

    Usage::

        v = HetuvidyaValidator()
        result = v.validate(case_id="ZR-01")
        print(result["status"])  # 'pass'
    """

    def __init__(self, cases_path: Path | None = None):
        self._cases_path = cases_path or get_cases_path()

    def validate(self, *, case_id: str | None = None) -> dict:
        """Run Hetuvidya validation and return a structured result dict."""
        from zilanlib.reasoning.hetuvidya_validator import (
            build_hetuvidya_validation,
        )

        return build_hetuvidya_validation(
            self._cases_path,
            case_id=case_id,
        )
