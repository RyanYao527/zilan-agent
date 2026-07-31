from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from dataclasses import asdict, dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

COPY_IGNORE_PATTERNS = (
    ".git",
    ".pytest_cache",
    ".ruff_cache",
    "build",
    "__pycache__",
    "*.pyc",
)

REQUIRED_SKILL_PATHS = (
    "SKILL.md",
    "agents/zilan-claude-code.md",
    "scripts/search_agama.py",
    "scripts/build_agama_context.py",
    "context/因明推理引擎.md",
    "context/摄类学工具箱.md",
    "context/agama/agama-index.md",
    "context/agama/T0099-za-agama.md",
)

REQUIRED_AGENT_FRAGMENTS = (
    "name: zilan",
    "tools:",
    "search_agama.py",
    "context/",
)


@dataclass(frozen=True)
class InstallCheck:
    name: str
    passed: bool
    detail: str


@dataclass(frozen=True)
class MockInstallResult:
    mode: str
    root: str
    mock_home: str
    skill_dir: str
    agent_file: str
    checks: list[InstallCheck]
    search_exit_code: int
    search_excerpt: str

    @property
    def passed(self) -> bool:
        return all(check.passed for check in self.checks) and self.search_exit_code == 0


def _copy_repo_to_skill(root: Path, skill_dir: Path) -> None:
    if skill_dir.exists():
        raise RuntimeError(f"Mock skill directory already exists: {skill_dir}")
    shutil.copytree(
        root,
        skill_dir,
        ignore=shutil.ignore_patterns(*COPY_IGNORE_PATTERNS),
    )


def _install_agent_definition(root: Path, agent_file: Path) -> None:
    if agent_file.exists():
        raise RuntimeError(f"Mock agent file already exists: {agent_file}")
    agent_file.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(root / "agents" / "zilan-claude-code.md", agent_file)


def _run_installed_search(skill_dir: Path) -> tuple[int, str]:
    result = subprocess.run(
        [sys.executable, str(skill_dir / "scripts" / "search_agama.py"), "--terms", "緣起", "--limit", "1"],
        cwd=skill_dir,
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=False,
    )
    output = result.stdout.strip() or result.stderr.strip()
    return result.returncode, "\n".join(output.splitlines()[:4])


def run_mock_install(root: Path = ROOT, base_dir: Path | None = None) -> MockInstallResult:
    root = root.resolve()
    if base_dir is None:
        base_dir = Path(tempfile.mkdtemp(prefix="zilan-mock-install-"))
    else:
        base_dir = base_dir.resolve()
        base_dir.mkdir(parents=True, exist_ok=True)

    mock_home = base_dir / "home"
    skill_dir = mock_home / ".claude" / "skills" / "zilan-agent"
    agent_file = mock_home / ".claude" / "agents" / "zilan.md"

    _copy_repo_to_skill(root, skill_dir)
    _install_agent_definition(root, agent_file)

    checks: list[InstallCheck] = []
    for rel_path in REQUIRED_SKILL_PATHS:
        path = skill_dir / rel_path
        checks.append(InstallCheck(name=f"skill:{rel_path}", passed=path.exists(), detail=str(path)))

    source_agent = root / "agents" / "zilan-claude-code.md"
    checks.append(
        InstallCheck(
            name="agent:file",
            passed=agent_file.exists(),
            detail=str(agent_file),
        )
    )
    checks.append(
        InstallCheck(
            name="agent:matches-source",
            passed=agent_file.read_text(encoding="utf-8") == source_agent.read_text(encoding="utf-8"),
            detail=str(source_agent),
        )
    )

    agent_text = agent_file.read_text(encoding="utf-8")
    for fragment in REQUIRED_AGENT_FRAGMENTS:
        checks.append(
            InstallCheck(
                name=f"agent-fragment:{fragment}",
                passed=fragment in agent_text,
                detail=fragment,
            )
        )

    search_exit_code, search_excerpt = _run_installed_search(skill_dir)
    return MockInstallResult(
        mode="mock-claude-install",
        root=str(root),
        mock_home=str(mock_home),
        skill_dir=str(skill_dir),
        agent_file=str(agent_file),
        checks=checks,
        search_exit_code=search_exit_code,
        search_excerpt=search_excerpt,
    )


def _print_text(result: MockInstallResult) -> None:
    print(f"mode: {result.mode}")
    print(f"mock_home: {result.mock_home}")
    print(f"skill_dir: {result.skill_dir}")
    print(f"agent_file: {result.agent_file}")
    print("checks:")
    for check in result.checks:
        status = "pass" if check.passed else "fail"
        print(f"  - {check.name}: {status}")
    print(f"search_exit_code: {result.search_exit_code}")
    print("search_excerpt:")
    print(result.search_excerpt)


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description="Smoke-test a mock Claude Code install without touching ~/.claude.")
    parser.add_argument("--root", type=Path, default=ROOT, help="Repository root.")
    parser.add_argument(
        "--dest",
        type=Path,
        help="Destination base directory. Defaults to a temporary directory that is removed after the run.",
    )
    parser.add_argument("--json", action="store_true", help="Emit JSON output.")
    args = parser.parse_args()

    try:
        if args.dest is None:
            with tempfile.TemporaryDirectory(prefix="zilan-mock-install-") as temp_dir:
                result = run_mock_install(root=args.root, base_dir=Path(temp_dir))
                if args.json:
                    data = asdict(result)
                    data["passed"] = result.passed
                    print(json.dumps(data, ensure_ascii=False, indent=2))
                else:
                    _print_text(result)
                return 0 if result.passed else 1
        result = run_mock_install(root=args.root, base_dir=args.dest)
    except (OSError, RuntimeError, subprocess.SubprocessError) as exc:
        print(f"mock-install-smoke failed: {exc}", file=sys.stderr)
        return 1

    if args.json:
        data = asdict(result)
        data["passed"] = result.passed
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        _print_text(result)
    return 0 if result.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
