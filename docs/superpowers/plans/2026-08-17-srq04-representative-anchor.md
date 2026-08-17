# SRQ-04 Representative Anchor Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reject SRQ-04 answers that claim the right CBETA work identifier while omitting its checked representative local citation anchor.

**Architecture:** The fixture-defined `agama_citation_boundary` contract receives one additional required slot. The existing deterministic answer-contract reviewer already evaluates required slots, so no Python production code or retrieval behavior changes.

**Tech Stack:** Python 3.11, pytest, YAML fixtures, existing `zilanlib` answer-contract review.

## Global Constraints

- Preserve `scripts/search_agama.py` as a compatibility surface.
- Do not change provider routes, platform validation, or scholarly-collation status.
- Keep the representative citation limited to the checked local working-corpus anchor; it does not assert publication-level collation.
- Do not remove existing regression cases or boundary checks.

---

### Task 1: Guard the SRQ-04 representative anchor

**Files:**

- Modify: `tests/test_semantic_answer_contract_review_srq04.py`
- Modify: `tests/fixtures/retrieval_chunks/semantic_chunks.yaml`

**Interfaces:**

- Consumes: `build_answer_contract_review(DEFAULT_FIXTURE, query_id="SRQ-04", answer_text=...)`.
- Produces: `representative_agama_anchor` in the existing `missing_required_slots` list.

- [ ] **Step 1: Write the failing test**

```python
def test_answer_contract_review_rejects_srq04_mismatched_representative_anchor() -> None:
    result = build_answer_contract_review(
        DEFAULT_FIXTURE,
        query_id="SRQ-04",
        answer_text=MISMATCHED_REPRESENTATIVE_ANCHOR_ANSWER,
    )

    assert result["overall_status"] == "fail"
    assert result["reviews"][0]["missing_required_slots"] == ["representative_agama_anchor"]
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest -q tests/test_semantic_answer_contract_review_srq04.py::test_answer_contract_review_rejects_srq04_mismatched_representative_anchor`

Expected: FAIL because the current generic CBETA and `context/agama/` terms incorrectly allow the mismatched citation.

- [ ] **Step 3: Add the minimal fixture slot**

```yaml
- label: representative_agama_anchor
  terms:
  - "context/agama/T0099-za-agama.md:147"
```

Add this under `SRQ-04.answer_contracts.agama_citation_boundary.required_slots`.

- [ ] **Step 4: Run focused checks**

Run: `python -m pytest -q tests/test_semantic_answer_contract_review_srq04.py tests/test_semantic_retrieval_dry_run.py tests/test_reasoning_contract_runner.py`

Expected: PASS. The checked passing sample retains the required anchor and the new mismatch sample fails only on the new slot.

- [ ] **Step 5: Run repository checks**

Run: `python scripts/validate_zilan_repo.py --check-generated --strict-yaml; python -m ruff check scripts tests; python -m mypy; python -m pytest -q`

Expected: all commands pass.
