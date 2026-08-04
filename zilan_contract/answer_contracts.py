from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from zilan_contract.results import ContractIssue


@dataclass(frozen=True)
class AnswerContractResult:
    overall_status: str
    reviews: list[dict[str, Any]]

    def passed(self) -> bool:
        return self.overall_status == "pass"

    def issues(self) -> list[ContractIssue]:
        issues: list[ContractIssue] = []
        for review in self.reviews:
            contract_id = str(review["contract_id"])
            for term in review["missing_required_terms"]:
                issues.append(
                    ContractIssue(
                        source="answer_contract",
                        contract_id=contract_id,
                        kind="missing_required_term",
                        label=str(term),
                        detail=f"Missing required term: {term}",
                    )
                )
            for term in review["present_forbidden_terms"]:
                issues.append(
                    ContractIssue(
                        source="answer_contract",
                        contract_id=contract_id,
                        kind="present_forbidden_term",
                        label=str(term),
                        detail=f"Present forbidden term: {term}",
                    )
                )
            for label in review["missing_required_slots"]:
                issues.append(
                    ContractIssue(
                        source="answer_contract",
                        contract_id=contract_id,
                        kind="missing_required_slot",
                        label=str(label),
                        detail=f"Missing required slot: {label}",
                    )
                )
        return issues

    def to_summary(self) -> dict[str, object]:
        return {
            "overall_status": self.overall_status,
            "contract_count": len(self.reviews),
            "issue_count": len(self.issues()),
        }

    def to_markdown(self) -> str:
        lines = ["# Answer Contract Review", "", f"Overall status: {self.overall_status}", "", "## Contracts"]
        for review in self.reviews:
            lines.append(f"- {review['contract_id']}: {review['status']}")
        return "\n".join(lines).rstrip() + "\n"


class AnswerContractRunner:
    """Run domain-neutral answer-contract checks without SRQ fixtures."""

    def check(self, *, answer_text: str, contracts: dict[str, object]) -> AnswerContractResult:
        reviews = [_review_contract(contract_id, contract, answer_text) for contract_id, contract in contracts.items()]
        status = "pass" if reviews and all(review["status"] == "pass" for review in reviews) else "fail"
        return AnswerContractResult(overall_status=status, reviews=reviews)

    def check_file(self, *, answer_file: Path, contracts: dict[str, object]) -> AnswerContractResult:
        return self.check(answer_text=answer_file.read_text(encoding="utf-8"), contracts=contracts)


def _review_contract(contract_id: str, contract: object, answer_text: str) -> dict[str, Any]:
    if not isinstance(contract, dict):
        return {
            "contract_id": contract_id,
            "status": "fail",
            "description": "",
            "required_terms": [],
            "missing_required_terms": ["<invalid contract>"],
            "forbidden_terms": [],
            "present_forbidden_terms": [],
            "required_slots": [],
            "missing_required_slots": [],
        }

    required_terms = _string_list(contract.get("required_terms"))
    forbidden_terms = _string_list(contract.get("forbidden_terms"))
    missing_required_terms = [term for term in required_terms if term not in answer_text]
    present_forbidden_terms = [term for term in forbidden_terms if term in answer_text]
    required_slots = [
        _review_required_slot(slot, answer_text)
        for slot in _mapping_list(contract.get("required_slots"))
    ]
    missing_required_slots = [slot["label"] for slot in required_slots if slot["status"] == "fail"]
    status = (
        "pass"
        if not missing_required_terms and not present_forbidden_terms and not missing_required_slots
        else "fail"
    )

    return {
        "contract_id": contract_id,
        "status": status,
        "description": contract.get("description", ""),
        "required_terms": required_terms,
        "missing_required_terms": missing_required_terms,
        "forbidden_terms": forbidden_terms,
        "present_forbidden_terms": present_forbidden_terms,
        "required_slots": required_slots,
        "missing_required_slots": missing_required_slots,
    }


def _review_required_slot(slot: dict[str, Any], answer_text: str) -> dict[str, Any]:
    label = str(slot.get("label", ""))
    terms = _string_list(slot.get("terms"))
    matched_terms = [term for term in terms if term in answer_text]
    return {
        "label": label,
        "terms": terms,
        "matched_terms": matched_terms,
        "status": "pass" if matched_terms else "fail",
    }


def _string_list(value: object) -> list[str]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, str) and item]


def _mapping_list(value: object) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, dict)]
