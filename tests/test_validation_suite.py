from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

from zilanlib.validation import suite


def test_validation_suite_runs_validators_in_stable_order(monkeypatch, tmp_path: Path) -> None:
    calls: list[str] = []

    def record(name: str) -> Callable[..., None]:
        def _validator(*_args: object, **_kwargs: object) -> None:
            calls.append(name)

        return _validator

    monkeypatch.setattr(suite.repository_metadata_validation, "check_paths", record("check_paths"))
    monkeypatch.setattr(
        suite.repository_metadata_validation,
        "check_version_consistency",
        record("check_version_consistency"),
    )
    monkeypatch.setattr(
        suite.repository_metadata_validation,
        "check_regression_matrix",
        record("check_regression_matrix"),
    )
    monkeypatch.setattr(suite.regression_cases_validation, "validate_regression_cases", record("regression_cases"))
    monkeypatch.setattr(suite.reasoning_cases_validation, "validate_reasoning_cases", record("reasoning_cases"))
    monkeypatch.setattr(suite.retrieval_chunks_validation, "validate_retrieval_chunks", record("retrieval_chunks"))
    monkeypatch.setattr(suite.collation_validation, "validate_collation_fixtures", record("collation"))
    monkeypatch.setattr(suite.agent_prompt_validation, "validate_agent_prompts", record("agent_prompts"))
    monkeypatch.setattr(
        suite.public_docs_validation,
        "check_readme_platform_validation_links",
        record("readme_links"),
    )
    monkeypatch.setattr(suite.public_docs_validation, "check_third_party_notices", record("third_party_notices"))
    monkeypatch.setattr(suite.public_docs_validation, "check_skill_script_inventory", record("skill_inventory"))
    monkeypatch.setattr(suite.public_docs_validation, "check_public_style_boundaries", record("style_boundaries"))
    monkeypatch.setattr(suite.runtime_evidence_validation, "validate_runtime_evidence", record("runtime_evidence"))
    monkeypatch.setattr(suite.public_docs_validation, "check_portable_upgrade_doc", record("portable_upgrade_doc"))
    monkeypatch.setattr(suite.platform_validation, "validate_platform_yaml_metadata", record("platform_yaml"))
    monkeypatch.setattr(suite.agama_corpus_validation, "validate_agama_search", record("agama_search"))
    monkeypatch.setattr(suite.agama_corpus_validation, "validate_generated_agama", record("generated_agama"))

    failures, warnings = suite.run_checks(tmp_path, check_generated=True, strict_yaml=True)

    assert failures == []
    assert warnings == []
    assert calls == [
        "check_paths",
        "check_version_consistency",
        "check_regression_matrix",
        "regression_cases",
        "reasoning_cases",
        "retrieval_chunks",
        "collation",
        "agent_prompts",
        "readme_links",
        "third_party_notices",
        "skill_inventory",
        "style_boundaries",
        "runtime_evidence",
        "portable_upgrade_doc",
        "platform_yaml",
        "agama_search",
        "generated_agama",
    ]


def test_validation_suite_passes_shared_state_and_flags(monkeypatch, tmp_path: Path) -> None:
    resolved_root = tmp_path.resolve()
    observed_simple: list[tuple[str, bool, int]] = []
    observed_yaml: list[tuple[str, bool, int, int, bool, tuple[str, ...]]] = []

    def record_simple(name: str) -> Callable[[Path, list[str]], None]:
        def _validator(root: Path, failures: list[str]) -> None:
            observed_simple.append((name, root == resolved_root, id(failures)))
            failures.append(f"{name} failure")

        return _validator

    def record_yaml(name: str) -> Callable[[Path, list[str], list[str], bool], None]:
        def _validator(root: Path, failures: list[str], warnings: list[str], strict_yaml: bool) -> None:
            observed_yaml.append(
                (name, root == resolved_root, id(failures), id(warnings), strict_yaml, tuple(failures))
            )
            warnings.append(f"{name} warning")

        return _validator

    monkeypatch.setattr(suite.repository_metadata_validation, "check_paths", record_simple("check_paths"))
    monkeypatch.setattr(suite.repository_metadata_validation, "check_version_consistency", record_simple("version"))
    monkeypatch.setattr(suite.repository_metadata_validation, "check_regression_matrix", record_simple("matrix"))
    monkeypatch.setattr(suite.regression_cases_validation, "validate_regression_cases", record_yaml("regression"))
    monkeypatch.setattr(suite.reasoning_cases_validation, "validate_reasoning_cases", record_yaml("reasoning"))
    monkeypatch.setattr(suite.retrieval_chunks_validation, "validate_retrieval_chunks", record_yaml("retrieval"))
    monkeypatch.setattr(suite.collation_validation, "validate_collation_fixtures", record_yaml("collation"))
    def noop_two(_root: Path, _failures: list[str]) -> None:
        return None

    monkeypatch.setattr(suite.agent_prompt_validation, "validate_agent_prompts", noop_two)
    monkeypatch.setattr(suite.public_docs_validation, "check_readme_platform_validation_links", noop_two)
    monkeypatch.setattr(suite.public_docs_validation, "check_third_party_notices", noop_two)
    monkeypatch.setattr(suite.public_docs_validation, "check_skill_script_inventory", noop_two)
    monkeypatch.setattr(suite.public_docs_validation, "check_public_style_boundaries", noop_two)
    monkeypatch.setattr(suite.runtime_evidence_validation, "validate_runtime_evidence", noop_two)
    monkeypatch.setattr(suite.public_docs_validation, "check_portable_upgrade_doc", noop_two)
    monkeypatch.setattr(suite.platform_validation, "validate_platform_yaml_metadata", record_yaml("platform"))
    monkeypatch.setattr(suite.agama_corpus_validation, "validate_agama_search", noop_two)
    monkeypatch.setattr(suite.agama_corpus_validation, "validate_generated_agama", noop_two)

    failures, warnings = suite.run_checks(tmp_path / ".", check_generated=False, strict_yaml=True)

    assert failures == ["check_paths failure", "version failure", "matrix failure"]
    assert warnings == [
        "regression warning",
        "reasoning warning",
        "retrieval warning",
        "collation warning",
        "platform warning",
    ]
    failure_ids = {failure_id for _name, _root, failure_id in observed_simple}
    failure_ids.update(failure_id for _name, _root, failure_id, _warnings_id, _flag, _seen in observed_yaml)
    warning_ids = {warning_id for _name, _root, _failure_id, warning_id, _flag, _seen in observed_yaml}

    assert len(failure_ids) == 1
    assert len(warning_ids) == 1
    assert all(root_is_resolved for _name, root_is_resolved, _failure_id in observed_simple)
    assert all(root_is_resolved for _name, root_is_resolved, _failure_id, _warnings_id, _flag, _seen in observed_yaml)
    assert all(flag for _name, _root, _failure_id, _warnings_id, flag, _seen in observed_yaml)
    assert observed_yaml[0][5] == ("check_paths failure", "version failure", "matrix failure")


def test_validation_suite_skips_generated_agama_when_not_requested(monkeypatch, tmp_path: Path) -> None:
    generated_called = False

    def fail_if_generated(_root: Path, _failures: list[str]) -> None:
        nonlocal generated_called
        generated_called = True

    def noop_two(_root: Path, _failures: list[str]) -> None:
        return None

    monkeypatch.setattr(suite.repository_metadata_validation, "check_paths", noop_two)
    monkeypatch.setattr(suite.repository_metadata_validation, "check_version_consistency", noop_two)
    monkeypatch.setattr(suite.repository_metadata_validation, "check_regression_matrix", noop_two)
    monkeypatch.setattr(
        suite.regression_cases_validation,
        "validate_regression_cases",
        lambda _root, _failures, _warnings, _strict_yaml: None,
    )
    monkeypatch.setattr(
        suite.reasoning_cases_validation,
        "validate_reasoning_cases",
        lambda _root, _failures, _warnings, _strict_yaml: None,
    )
    monkeypatch.setattr(
        suite.retrieval_chunks_validation,
        "validate_retrieval_chunks",
        lambda _root, _failures, _warnings, _strict_yaml: None,
    )
    monkeypatch.setattr(
        suite.collation_validation,
        "validate_collation_fixtures",
        lambda _root, _failures, _warnings, _strict_yaml: None,
    )
    monkeypatch.setattr(suite.agent_prompt_validation, "validate_agent_prompts", noop_two)
    monkeypatch.setattr(suite.public_docs_validation, "check_readme_platform_validation_links", noop_two)
    monkeypatch.setattr(suite.public_docs_validation, "check_third_party_notices", noop_two)
    monkeypatch.setattr(suite.public_docs_validation, "check_skill_script_inventory", noop_two)
    monkeypatch.setattr(suite.public_docs_validation, "check_public_style_boundaries", noop_two)
    monkeypatch.setattr(suite.runtime_evidence_validation, "validate_runtime_evidence", noop_two)
    monkeypatch.setattr(suite.public_docs_validation, "check_portable_upgrade_doc", noop_two)
    monkeypatch.setattr(
        suite.platform_validation,
        "validate_platform_yaml_metadata",
        lambda _root, _failures, _warnings, _strict_yaml: None,
    )
    monkeypatch.setattr(suite.agama_corpus_validation, "validate_agama_search", noop_two)
    monkeypatch.setattr(suite.agama_corpus_validation, "validate_generated_agama", fail_if_generated)

    failures, warnings = suite.run_checks(tmp_path, check_generated=False, strict_yaml=False)

    assert failures == []
    assert warnings == []
    assert generated_called is False
