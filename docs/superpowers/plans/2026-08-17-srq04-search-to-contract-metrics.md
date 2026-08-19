# SRQ-04 Search-to-Contract and Metrics Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Regression-test the SRQ-04 source-to-answer citation handoff and publish the resulting 285-test local baseline.

**Architecture:** Reuse the stable search API and deterministic answer-contract reviewer in a new cross-module test. No production implementation changes are required; P2 updates only the two existing public metric strings after full pytest confirms the expected count.

**Tech Stack:** Python 3.11, pytest, existing `zilanlib.agama.search` and `zilanlib.semantic.answer_contract_review` modules.

## Global Constraints

- Preserve `scripts/search_agama.py` behavior and output format.
- Do not call providers or change platform status.
- Keep CBETA XML-P5 and publication-level collation boundaries unchanged.
- Do not modify or remove existing regression cases.

---

### Task 1: Test the SRQ-04 source-to-answer citation handoff

**Files:**

- Create: `tests/test_srq04_search_to_contract.py`

**Interfaces:**

- Consumes: `search_agama(pattern, root=ROOT, limit=0)` and `build_answer_contract_review(DEFAULT_FIXTURE, query_id="SRQ-04", answer_text=...)`.
- Produces: a passing deterministic assertion that the returned `T02n0099` line-147 citation satisfies `representative_agama_anchor` when placed in a bounded answer.

- [ ] **Step 1: Write the source-to-answer regression**

```python
matches = search_agama("色無常，無常即苦，苦即非我", root=ROOT, limit=0)
representative = next(match for match in matches if match.cbeta_id == "T02n0099" and match.line == 147)
answer = f"检索范围：本次只基于本地 context/agama/ 做代表性检索。\n代表性引文：{representative.citation}\nCBETA 编号保留。\n边界：这是初步证据，出版级引文仍待校勘。"
result = build_answer_contract_review(DEFAULT_FIXTURE, query_id="SRQ-04", answer_text=answer)
assert result["overall_status"] == "pass"
```

- [ ] **Step 2: Run the cross-module regression**

Run: `python -m pytest -q tests/test_srq04_search_to_contract.py`

Expected: PASS because the stable search citation contains `context/agama/T0099-za-agama.md:147`.

### Task 2: Refresh verified public metrics

**Files:**

- Modify: `README.md:68`
- Modify: `CHANGELOG.md:33`

- [ ] **Step 1: Confirm full-suite count**

Run: `python -m pytest -q`

Expected: `285 passed` after Task 1 adds one test to the committed 284-test baseline.

- [ ] **Step 2: Update the two metric strings**

```text
285 tests    ·    84% code coverage (zilanlib)
Refreshed public engineering metrics to the current local baseline of 285 tests, 84% zilanlib coverage, and 65 mypy-checked source files.
```

- [ ] **Step 3: Run final checks**

Run: `python scripts/validate_zilan_repo.py --check-generated --strict-yaml; python -m ruff check scripts tests; python -m mypy; python -m pytest -q`

Expected: all commands pass, with `285 passed`.
