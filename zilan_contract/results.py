from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ContractIssue:
    source: str
    contract_id: str
    kind: str
    label: str
    detail: str


class ContractResult:
    """Structured result from a contract check."""

    def __init__(self, raw: dict[str, Any]):
        self.raw = raw
        self.overall_status: str = str(raw.get("overall_status", "unknown"))
        self.answer_review_status: str = str(raw.get("answer_review_status", "unknown"))
        validators = raw.get("validators", {})
        self.validators: dict[str, Any] = validators if isinstance(validators, dict) else {}
        self.query_id: str | None = raw.get("query_id") if isinstance(raw.get("query_id"), str) else None
        self.query: str | None = raw.get("query") if isinstance(raw.get("query"), str) else None

    def __repr__(self) -> str:
        return f"ContractResult(overall={self.overall_status!r}, review={self.answer_review_status!r})"

    def passed(self) -> bool:
        """True if the contract check passed."""
        return self.overall_status == "pass"

    def failed_validators(self) -> list[str]:
        """Names of validators that did not pass."""
        failed: list[str] = []
        for name, validator in self.validators.items():
            if not isinstance(validator, dict):
                failed.append(name)
                continue
            if validator.get("status") not in ("pass", "run", "not_applicable"):
                failed.append(name)
        return failed

    def issues(self) -> list[ContractIssue]:
        """Return answer-contract issues in a small public shape."""
        review = self.raw.get("answer_contract_review")
        if not isinstance(review, dict):
            return []

        issues: list[ContractIssue] = []
        for item in review.get("reviews", []):
            if not isinstance(item, dict):
                continue
            contract_id = str(item.get("contract_id", ""))
            for term in _string_items(item.get("missing_required_terms")):
                issues.append(
                    ContractIssue(
                        source="answer_contract",
                        contract_id=contract_id,
                        kind="missing_required_term",
                        label=term,
                        detail=f"Missing required term: {term}",
                    )
                )
            for term in _string_items(item.get("present_forbidden_terms")):
                issues.append(
                    ContractIssue(
                        source="answer_contract",
                        contract_id=contract_id,
                        kind="present_forbidden_term",
                        label=term,
                        detail=f"Present forbidden term: {term}",
                    )
                )
            for label in _string_items(item.get("missing_required_slots")):
                issues.append(
                    ContractIssue(
                        source="answer_contract",
                        contract_id=contract_id,
                        kind="missing_required_slot",
                        label=label,
                        detail=f"Missing required slot: {label}",
                    )
                )
        return issues

    def to_summary(self) -> dict[str, object]:
        """Return a compact JSON-compatible summary."""
        return {
            "overall_status": self.overall_status,
            "answer_review_status": self.answer_review_status,
            "query_id": self.query_id,
            "failed_validators": self.failed_validators(),
            "issue_count": len(self.issues()),
        }

    def to_markdown(self) -> str:
        """Render a compact human-readable review."""
        failed = ", ".join(self.failed_validators()) or "none"
        lines = [
            "# zilan_contract Review",
            "",
            f"Overall status: {self.overall_status}",
            f"Answer review status: {self.answer_review_status}",
            f"Query ID: {self.query_id or 'none'}",
            f"Failed validators: {failed}",
            "",
            "## Issues",
        ]
        issues = self.issues()
        if not issues:
            lines.append("- none")
        else:
            for issue in issues:
                lines.append(f"- {issue.contract_id}: {issue.detail}")
        return "\n".join(lines).rstrip() + "\n"


def _string_items(value: object) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item) for item in value if isinstance(item, str)]
