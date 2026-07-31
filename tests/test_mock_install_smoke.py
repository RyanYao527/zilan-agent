from __future__ import annotations

from pathlib import Path

from mock_install_smoke import _copy_repo_to_skill, run_mock_install

ROOT = Path(__file__).resolve().parents[1]


def test_mock_install_creates_expected_claude_layout(tmp_path: Path) -> None:
    result = run_mock_install(root=ROOT, base_dir=tmp_path)

    assert result.passed
    assert Path(result.mock_home).parts[-1] == "home"
    assert Path(result.skill_dir, "SKILL.md").exists()
    assert Path(result.skill_dir, "scripts", "search_agama.py").exists()
    assert Path(result.skill_dir, "context", "agama", "agama-index.md").exists()
    assert Path(result.agent_file).exists()
    assert "Found 1 matches" in result.search_excerpt


def test_mock_install_copy_ignores_build_artifacts(tmp_path: Path) -> None:
    source_repo = tmp_path / "repo"
    source_repo.mkdir()
    build_artifact = source_repo / "build" / "bdist.win-amd64" / "wheel" / "stale.egg-info"
    build_artifact.mkdir(parents=True)
    (build_artifact / "PKG-INFO").write_text("stale build metadata\n", encoding="utf-8")

    skill_dir = tmp_path / "skill"
    _copy_repo_to_skill(source_repo, skill_dir)

    assert not (skill_dir / "build").exists()


def test_mock_install_refuses_existing_skill_dir(tmp_path: Path) -> None:
    run_mock_install(root=ROOT, base_dir=tmp_path)

    try:
        run_mock_install(root=ROOT, base_dir=tmp_path)
    except RuntimeError as exc:
        assert "already exists" in str(exc)
    else:
        raise AssertionError("mock install should refuse to overwrite an existing mock skill directory")
