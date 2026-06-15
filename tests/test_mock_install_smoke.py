from pathlib import Path

from mock_install_smoke import run_mock_install

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


def test_mock_install_refuses_existing_skill_dir(tmp_path: Path) -> None:
    run_mock_install(root=ROOT, base_dir=tmp_path)

    try:
        run_mock_install(root=ROOT, base_dir=tmp_path)
    except RuntimeError as exc:
        assert "already exists" in str(exc)
    else:
        raise AssertionError("mock install should refuse to overwrite an existing mock skill directory")
