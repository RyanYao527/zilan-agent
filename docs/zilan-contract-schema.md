# zilan_contract Schema Reference

This page documents the domain-neutral answer-contract schema used by:

- `AnswerContractRunner`
- `zilan-contract check`
- `python -m zilan_contract.cli check`

It is a deterministic local output-contract format. It does not call providers, grade prose quality, infer semantic intent, or change platform validation status.

## Scope

The schema checks whether an answer contains required boundary phrases, avoids forbidden phrases, and covers labeled alternative-term slots. It is intentionally small so installed-package smoke tests, CI jobs, and repository evidence reviews can run without network access.

Use it for:

- public SDK quickstart smoke tests;
- provider transcript spot reviews;
- deterministic answer-boundary checks;
- regression guards around known answer failures.

Do not use it as:

- a general LLM judge;
- a Buddhist scholarship verifier;
- a replacement for structured reasoning validators;
- evidence that any provider route is `tested` in `docs/platform-validation.md`.

## CLI file shape

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

Each mapping key under `contracts` becomes the public `contract_id` in JSON and Markdown output. The CLI coerces YAML mapping keys to strings, but Python callers should pass string keys directly.

The top-level wrapper is required only for CLI files. A file without `contracts` is rejected with:

```text
Contract file must contain a top-level contracts mapping.
```

Invalid YAML is rejected with an error beginning:

```text
Contract file contains invalid YAML
```

## Python API shape

Python callers pass the inner contracts mapping directly to `AnswerContractRunner.check()`:

```python
from zilan_contract import AnswerContractRunner

runner = AnswerContractRunner()
result = runner.check(
    answer_text="This is not medical advice. Contact a doctor in an emergency.",
    contracts={
        "medical_disclaimer": {
            "description": "Medical response must include safety boundaries.",
            "required_terms": ["not medical advice", "doctor", "emergency"],
            "forbidden_terms": ["guaranteed"],
            "required_slots": [
                {"label": "care_path", "terms": ["doctor", "emergency"]},
            ],
        },
    },
)

assert result.overall_status == "pass"
```

Passing the CLI wrapper shape to Python, such as `{"contracts": {...}}`, is not the API contract. Use the CLI wrapper only in YAML files consumed by `zilan-contract check --contract-file`.

## Contract fields

Each contract definition must be a mapping.

| Field | Required | Shape | Default | Semantics |
| --- | --- | --- | --- | --- |
| `description` | No | string | `""` | Human-readable explanation included in output. |
| `required_terms` | Yes | non-empty list of non-empty strings | none | Every listed term must appear in the answer. |
| `forbidden_terms` | No | list of non-empty strings | `[]` | No listed term may appear in the answer. |
| `required_slots` | No | list of slot mappings | `[]` | Each slot passes when at least one of its `terms` appears. |

Each `required_slots` item has this shape:

```yaml
- label: boundary
  terms:
    - "not legal advice"
    - "consult an attorney"
```

Use separate slots for independent requirements. Use multiple `terms` inside one slot only for acceptable alternatives.

## Matching semantics

Matching is a simple case-sensitive substring check.

- `required_terms`: every term must be present as a case-sensitive substring of `answer_text`.
- `forbidden_terms`: if any term appears as a case-sensitive substring, the contract fails.
- `required_slots`: every slot must pass; a slot passes when at least one alternative term appears as a case-sensitive substring.
- Empty strings are invalid in term lists and slot labels.
- Empty contract mappings are invalid. Python schema validation raises `Contracts must contain at least one contract.`

The checker does not trim, normalize, tokenize, stem, translate, or case-fold answer text. Put every accepted spelling or wording variant explicitly in `terms` when a slot allows alternatives.

## Issue kinds

Failed checks produce stable machine-readable issue kinds:

| Kind | Trigger | Label |
| --- | --- | --- |
| `missing_required_term` | One `required_terms` item was absent. | The missing term. |
| `present_forbidden_term` | One `forbidden_terms` item was present. | The forbidden term. |
| `missing_required_slot` | No alternative in a slot's `terms` appeared. | The slot `label`. |

These issue kinds are part of the public result surface and are safe to use in CI assertions.

## Schema errors

Malformed schemas raise `AnswerContractSchemaError` in Python. The CLI converts file loading, YAML shape, and schema errors into exit code `2` with stderr beginning `zilan-contract failed:`.

Examples of rejected schemas:

```yaml
contracts:
  legal_boundary:
    required_terms: "not legal advice"
```

`required_terms` must be a non-empty list of non-empty strings.

```yaml
contracts:
  legal_boundary:
    required_terms:
      - "not legal advice"
    required_slots:
      label: boundary
```

`required_slots` must be a list of slot mappings.

```yaml
contracts:
  legal_boundary:
    required_terms:
      - "not legal advice"
    required_slots:
      - label: boundary
        terms: []
```

Each slot `terms` value must be a non-empty list of non-empty strings.

## Result semantics

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

Markdown output contains the same issue details in a human-readable report:

```markdown
# zilan_contract answer review

- Overall status: fail
- Contracts: 1
- Issues: 1

## Issues

- `[legal_boundary]` missing_required_term: Missing required term: not legal advice
```

## Unsupported by v2.5.7

The v2.5.7 schema is intentionally exact-match only:

- v2.5.7 does not support regex matching.
- It does not support case-insensitive matching or Unicode normalization.
- It does not support tokenization, stemming, translation, or semantic similarity.
- It does not support nested boolean logic such as `(A and B) or (C and D)`.
- It does not support per-issue severity levels; every issue contributes to a fail result.
- It does not replace domain validators such as Hetuvidya, Collected Topics, Madhyamaka, or Agama evidence checkers.

Use `required_slots` for narrow alternative wording. Add a structured validator when a requirement depends on reasoning shape rather than exact visible terms.

## CI integration

For CI, treat exit code `1` and exit code `2` differently:

- `1` means the answer did not satisfy a valid contract.
- `2` means the contract file or schema is invalid and should be fixed before reviewing answers.

Example:

```powershell
zilan-contract check `
  --contract-file tests/fixtures/zilan_contract/custom_contract.yaml `
  --answer-file tests/fixtures/zilan_contract/custom_answer.md `
  --json
```

Keep provider status changes separate. Passing this CLI check can support a runtime evidence note, but platform `tested` status remains governed by `agents/openai.yaml` and `docs/platform-validation.md`.
