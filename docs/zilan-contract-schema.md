# zilan_contract Schema Reference

This page documents the domain-neutral contract schema used by:

- `AnswerContractRunner`
- `zilan-contract check`
- `python -m zilan_contract.cli check`

It is a local deterministic output-contract format. It does not call providers, grade answer quality, or change platform validation status.

## CLI File Shape

CLI contract files must contain a top-level `contracts` mapping:

```yaml
contracts:
  medical_disclaimer:
    description: "Medical response must include safety boundaries."
    required_terms:
      - "not medical advice"
      - "doctor"
      - "emergency"
    forbidden_terms:
      - "guaranteed"
      - "definitely"
    required_slots:
      - label: care_path
        terms:
          - "doctor"
          - "emergency"
```

Each contract id becomes the `contract_id` in JSON and Markdown output.

## Fields

| Field | Required | Shape | Semantics |
| --- | --- | --- | --- |
| `description` | No | string | Human-readable description. |
| `required_terms` | Yes | non-empty list of non-empty strings | Every listed term must appear in the answer. |
| `forbidden_terms` | No | list of non-empty strings | No listed term may appear in the answer. |
| `required_slots` | No | list of slot mappings | Each slot passes when at least one of its `terms` appears. |

Each `required_slots` item has this shape:

```yaml
- label: boundary
  terms:
    - "not legal advice"
    - "consult an attorney"
```

Use separate slots for independent requirements. Use multiple `terms` inside one slot only for acceptable alternatives.

## Schema Errors

Malformed schemas raise `AnswerContractSchemaError` in Python and make the CLI exit with code `2`.

Examples of rejected schemas:

```yaml
contracts:
  legal_boundary:
    required_terms: "not legal advice"
```

```yaml
contracts:
  legal_boundary:
    required_terms:
      - "not legal advice"
    required_slots:
      label: boundary
```

`required_terms` must be a list, and `required_slots` must be a list of slot mappings.

## Result Semantics

CLI exit codes:

| Code | Meaning |
| --- | --- |
| `0` | Valid schema and all contracts passed. |
| `1` | Valid schema but at least one answer contract failed. |
| `2` | File loading, YAML shape, or contract schema error. |

JSON output contains a compact summary plus issue details:

```json
{
  "overall_status": "fail",
  "contract_count": 1,
  "issue_count": 1,
  "issues": [
    {
      "source": "answer_contract",
      "contract_id": "legal_boundary",
      "kind": "missing_required_term",
      "label": "not legal advice",
      "detail": "Missing required term: not legal advice"
    }
  ]
}
```

Markdown output contains the same issue details in a human-readable report.
