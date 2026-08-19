from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from zilanlib.provider.claude_code_route_preflight import build_preflight, render_markdown_report

ROOT = Path(__file__).resolve().parents[1]


def _write_settings(path: Path, env: dict[str, str], *, model: str = "sonnet") -> None:
    path.write_text(json.dumps({"env": env, "model": model}, ensure_ascii=False), encoding="utf-8")


def test_claude_code_preflight_marks_observed_unrecognized_model_as_blocked_and_redacts_secrets(
    tmp_path: Path,
) -> None:
    settings_path = tmp_path / "settings.json"
    _write_settings(
        settings_path,
        {
            "ANTHROPIC_AUTH_TOKEN": "secret-token-value",
            "ANTHROPIC_BASE_URL": "https://api.deepseek.com/anthropic",
            "ANTHROPIC_MODEL": "deepseek-v4-pro[1m]",
            "ANTHROPIC_DEFAULT_SONNET_MODEL": "deepseek-v4-pro[1m]",
        },
    )

    report = build_preflight(
        settings_path=settings_path,
        claude_path="C:/fake/claude.cmd",
        claude_version="2.1.234",
        observed_error_text='[claude-code:unrecognized_model] {"model":"deepseek-v4-pro[1m]","query_source":"sdk"}',
    )

    assert report["mode"] == "claude-code-route-preflight-v1"
    assert report["route_status"] == "blocked"
    assert report["cli"]["available"] is True
    assert report["cli"]["version"] == "2.1.234"
    assert report["settings"]["custom_anthropic_base_url"] is True
    assert report["settings"]["anthropic_base_url"] == "https://api.deepseek.com/anthropic"
    assert report["settings"]["selected_model"] == "deepseek-v4-pro[1m]"
    assert report["settings"]["sensitive_env_keys_present"] == ["ANTHROPIC_AUTH_TOKEN"]
    assert report["observed_error"]["code"] == "unrecognized_model"
    assert report["observed_error"]["model"] == "deepseek-v4-pro[1m]"
    assert "observed_unrecognized_model" in report["findings"]
    assert "secret-token-value" not in json.dumps(report, ensure_ascii=False)


def test_claude_code_preflight_custom_route_without_observed_error_requires_manual_review(tmp_path: Path) -> None:
    settings_path = tmp_path / "settings.json"
    _write_settings(
        settings_path,
        {
            "ANTHROPIC_BASE_URL": "https://api.deepseek.com/anthropic",
            "ANTHROPIC_MODEL": "deepseek-v4-pro[1m]",
        },
    )

    report = build_preflight(
        settings_path=settings_path,
        claude_path="C:/fake/claude.cmd",
        claude_version="2.1.234",
        observed_error_text=None,
    )

    assert report["route_status"] == "manual_review_required"
    assert "custom_anthropic_base_url" in report["findings"]
    assert "custom_model_aliases_detected" in report["findings"]


def test_claude_code_preflight_official_route_is_ready_for_bounded_runtime_attempt(tmp_path: Path) -> None:
    settings_path = tmp_path / "settings.json"
    _write_settings(
        settings_path,
        {
            "ANTHROPIC_BASE_URL": "https://api.anthropic.com",
            "ANTHROPIC_MODEL": "claude-sonnet-4-20250514",
        },
    )

    report = build_preflight(
        settings_path=settings_path,
        claude_path="C:/fake/claude.cmd",
        claude_version="2.1.234",
        observed_error_text=None,
    )

    assert report["route_status"] == "ready_for_bounded_runtime_attempt"
    assert report["settings"]["custom_anthropic_base_url"] is False
    assert report["settings"]["selected_model"] == "claude-sonnet-4-20250514"


def test_claude_code_preflight_markdown_declares_boundaries(tmp_path: Path) -> None:
    settings_path = tmp_path / "settings.json"
    _write_settings(
        settings_path,
        {
            "ANTHROPIC_BASE_URL": "https://api.deepseek.com/anthropic",
            "ANTHROPIC_MODEL": "deepseek-v4-pro[1m]",
        },
    )

    report = build_preflight(
        settings_path=settings_path,
        claude_path="C:/fake/claude.cmd",
        claude_version="2.1.234",
        observed_error_text='[claude-code:unrecognized_model] {"model":"deepseek-v4-pro[1m]","query_source":"sdk"}',
    )
    markdown = render_markdown_report(report)

    assert "# Claude Code Route Preflight" in markdown
    assert "`blocked`" in markdown
    assert "runtime pending" in markdown
    assert "No provider calls" in markdown
    assert "does not change platform validation status" in markdown


def test_claude_code_route_preflight_root_cli_outputs_json_without_invoking_claude(tmp_path: Path) -> None:
    settings_path = tmp_path / "settings.json"
    error_path = tmp_path / "runtime-error.txt"
    _write_settings(
        settings_path,
        {
            "ANTHROPIC_AUTH_TOKEN": "secret-token-value",
            "ANTHROPIC_BASE_URL": "https://api.deepseek.com/anthropic",
            "ANTHROPIC_MODEL": "deepseek-v4-pro[1m]",
        },
    )
    error_path.write_text(
        '[claude-code:unrecognized_model] {"model":"deepseek-v4-pro[1m]","query_source":"sdk"}',
        encoding="utf-8",
    )

    result = subprocess.run(
        [
            sys.executable,
            "scripts/claude_code_route_preflight.py",
            "--settings",
            str(settings_path),
            "--observed-error-file",
            str(error_path),
            "--claude-version",
            "2.1.234",
            "--json",
        ],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=True,
    )
    payload = json.loads(result.stdout)

    assert payload["mode"] == "claude-code-route-preflight-v1"
    assert payload["route_status"] == "blocked"
    assert payload["observed_error"]["code"] == "unrecognized_model"
    assert "secret-token-value" not in result.stdout
