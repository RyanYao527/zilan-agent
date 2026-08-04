from __future__ import annotations

from pathlib import Path

from zilanlib import repository

ROOT = Path(__file__).resolve().parents[1]


def test_zilanlib_package_metadata_is_declared() -> None:
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")

    assert (ROOT / "scripts" / "zilanlib" / "py.typed").is_file()
    assert repository.__name__ == "zilanlib.repository"

    expected_snippets = [
        '"wheel>=0.42"',
        '"Typing :: Typed"',
        "[project.urls]",
        'Homepage = "https://github.com/RyanYao527/zilan-agent"',
        'Repository = "https://github.com/RyanYao527/zilan-agent"',
        'Issues = "https://github.com/RyanYao527/zilan-agent/issues"',
        'Changelog = "https://github.com/RyanYao527/zilan-agent/blob/main/CHANGELOG.md"',
        "[project.scripts]",
        'zilan-contract = "zilan_contract.cli:main"',
        "[tool.setuptools.packages.find]",
        'license-files = ["LICENSE", "THIRD_PARTY_NOTICES.md"]',
        'where = [".", "scripts"]',
        'include = ["zilan_contract*", "zilanlib*"]',
        "[tool.setuptools.package-data]",
        'zilanlib = ["py.typed"]',
        'zilan_contract = ["py.typed", "fixtures/*.yaml", "fixtures/**/*.yaml", "fixtures/**/*.md"]',
    ]
    for snippet in expected_snippets:
        assert snippet in pyproject


def test_zilan_contract_answer_samples_are_bundled() -> None:
    source_dir = ROOT / "tests" / "fixtures" / "answers"
    bundled_dir = ROOT / "zilan_contract" / "fixtures" / "answers"
    source_files = sorted(source_dir.glob("*.md"))
    bundled_files = sorted(bundled_dir.glob("*.md"))

    assert [path.name for path in bundled_files] == [path.name for path in source_files]
    for source_file in source_files:
        bundled_file = bundled_dir / source_file.name
        assert bundled_file.read_text(encoding="utf-8") == source_file.read_text(encoding="utf-8")


def test_zilan_contract_yaml_fixtures_are_bundled_without_drift() -> None:
    pairs = [
        (ROOT / "tests" / "reasoning_cases.yaml", ROOT / "zilan_contract" / "fixtures" / "reasoning_cases.yaml"),
        (
            ROOT / "tests" / "fixtures" / "retrieval_chunks" / "semantic_chunks.yaml",
            ROOT / "zilan_contract" / "fixtures" / "retrieval_chunks" / "semantic_chunks.yaml",
        ),
    ]

    for source_file, bundled_file in pairs:
        assert bundled_file.read_text(encoding="utf-8") == source_file.read_text(encoding="utf-8")
