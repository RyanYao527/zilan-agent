from __future__ import annotations

from typing import Any


def case_ids_from_items(items: list[dict[str, Any]]) -> list[str]:
    """Return stable case ids from validator payload items."""

    case_ids: list[str] = []
    for item in items:
        case_id = item.get("case_id")
        if isinstance(case_id, str) and case_id and case_id not in case_ids:
            case_ids.append(case_id)
    return case_ids


def build_validator_output(
    *,
    validator: str,
    contract_family: str,
    mode: str,
    output_schema: str,
    source: str,
    case_id: str | None,
    payload_key: str,
    payload: list[dict[str, Any]],
    limitations: list[str] | tuple[str, ...],
) -> dict[str, Any]:
    """Build the shared top-level output envelope for local reasoning validators."""

    return {
        "status": "run",
        "validator": validator,
        "contract_family": contract_family,
        "mode": mode,
        "output_schema": output_schema,
        "source": source,
        "case_id": case_id,
        "case_ids": case_ids_from_items(payload),
        "count": len(payload),
        payload_key: payload,
        "limitations": list(limitations),
    }


def build_not_applicable_validator_output(
    *,
    validator: str,
    contract_family: str,
    output_schema: str,
    source: str,
    payload_key: str,
    limitation: str,
) -> dict[str, Any]:
    """Build the shared envelope for validators skipped by a query fixture."""

    return {
        "status": "not_applicable",
        "validator": validator,
        "contract_family": contract_family,
        "output_schema": output_schema,
        "source": source,
        "case_ids": [],
        payload_key: [],
        "limitations": [limitation],
    }
