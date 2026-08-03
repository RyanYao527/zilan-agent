from __future__ import annotations

import subprocess
from pathlib import Path

from zilanlib.validation import agama_corpus


class _SearchMatch:
    def __init__(self, *, file: str, text: str) -> None:
        self.file = file
        self.text = text


def test_agama_search_reports_empty_smoke_result(monkeypatch) -> None:
    monkeypatch.setattr(agama_corpus, "search_agama", lambda *args, **kwargs: [])
    failures: list[str] = []

    agama_corpus.validate_agama_search(Path("."), failures)

    assert failures == ["Agama smoke search returned no matches."]


def test_agama_search_reports_source_hits_and_false_positive_filter_drift(monkeypatch) -> None:
    def fake_search(terms: str, **kwargs):
        if terms == "無我|非我|緣起":
            return [_SearchMatch(file="context/agama/_source/T02n0099.xml", text="無我")]
        return [_SearchMatch(file="context/agama/T0099-za-agama.md", text="無我活為")]

    monkeypatch.setattr(agama_corpus, "search_agama", fake_search)
    monkeypatch.setattr(agama_corpus, "DEFAULT_FALSE_POSITIVE_PHRASES", ("無我活為",))
    failures: list[str] = []

    agama_corpus.validate_agama_search(Path("."), failures)

    assert "Agama smoke search should not return _source XML matches." in failures
    assert "Agama search did not filter known false positives." in failures


def test_generated_agama_reports_builder_failure(monkeypatch) -> None:
    result = subprocess.CompletedProcess(args=["build"], returncode=1, stdout="bad out", stderr="bad err")
    monkeypatch.setattr(agama_corpus, "run_build_agama", lambda root: result)
    failures: list[str] = []

    agama_corpus.validate_generated_agama(Path("."), failures)

    assert failures == ["build_agama_context.py failed:\nstdout:\nbad out\nstderr:\nbad err"]


def test_generated_agama_reports_idempotency_drift(tmp_path: Path, monkeypatch) -> None:
    generated = tmp_path / "generated.md"
    generated.write_text("first\n", encoding="utf-8")
    runs = 0

    def fake_run_build_agama(root: Path) -> subprocess.CompletedProcess[str]:
        nonlocal runs
        runs += 1
        generated.write_text(f"run {runs}\n", encoding="utf-8")
        return subprocess.CompletedProcess(args=["build"], returncode=0, stdout="", stderr="")

    monkeypatch.setattr(agama_corpus, "GENERATED_AGAMA_FILES", ("generated.md",))
    monkeypatch.setattr(agama_corpus, "run_build_agama", fake_run_build_agama)
    failures: list[str] = []

    agama_corpus.validate_generated_agama(tmp_path, failures)

    assert failures == ["Agama Markdown generation is not idempotent: generated.md"]

def test_generated_agama_reports_second_builder_failure(tmp_path: Path, monkeypatch) -> None:
    generated = tmp_path / "generated.md"
    generated.write_text("stable\n", encoding="utf-8")
    first = subprocess.CompletedProcess(args=["build"], returncode=0, stdout="", stderr="")
    second = subprocess.CompletedProcess(args=["build"], returncode=1, stdout="second out", stderr="second err")
    results = iter((first, second))

    monkeypatch.setattr(agama_corpus, "GENERATED_AGAMA_FILES", ("generated.md",))
    monkeypatch.setattr(agama_corpus, "run_build_agama", lambda root: next(results))
    failures: list[str] = []

    agama_corpus.validate_generated_agama(tmp_path, failures)

    assert failures == ["Second build_agama_context.py run failed:\nstdout:\nsecond out\nstderr:\nsecond err"]


def test_generated_agama_reports_committed_content_drift(tmp_path: Path, monkeypatch) -> None:
    generated = tmp_path / "generated.md"
    generated.write_text("stable\n", encoding="utf-8")
    ok = subprocess.CompletedProcess(args=["build"], returncode=0, stdout="", stderr="")
    diff = subprocess.CompletedProcess(args=["git", "diff"], returncode=1, stdout="", stderr="")
    subprocess_calls: list[list[str]] = []

    def fake_subprocess_run(args, **kwargs):
        subprocess_calls.append(args)
        return diff

    monkeypatch.setattr(agama_corpus, "GENERATED_AGAMA_FILES", ("generated.md",))
    monkeypatch.setattr(agama_corpus, "run_build_agama", lambda root: ok)
    monkeypatch.setattr(agama_corpus.subprocess, "run", fake_subprocess_run)
    failures: list[str] = []

    agama_corpus.validate_generated_agama(tmp_path, failures)

    assert subprocess_calls == [["git", "diff", "--quiet", "--", "generated.md"]]
    assert failures == [
        "Generated Agama Markdown differs from committed content. "
        "Run scripts/build_agama_context.py and review the diff."
    ]
