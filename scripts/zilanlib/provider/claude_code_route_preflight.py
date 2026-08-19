from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

REPORT_MODE = "claude-code-route-preflight-v1"
OFFICIAL_ANTHROPIC_BASE_URL = "https://api.anthropic.com"
MODEL_ENV_KEYS = (
    "ANTHROPIC_MODEL",
    "ANTHROPIC_DEFAULT_SONNET_MODEL",
    "ANTHROPIC_DEFAULT_OPUS_MODEL",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL",
    "ANTHROPIC_REASONING_MODEL",
)
SENSITIVE_ENV_RE = re.compile(r"(?:TOKEN|KEY|SECRET|PASSWORD)", re.IGNORECASE)
OBSERVED_ERROR_RE = re.compile(r"\[claude-code:(?P<code>[^\]]+)\]\s*(?P<payload>\{[^`\n]+?\})")


def _default_settings_path() -> Path:
    return Path.home() / ".claude" / "settings.json"


def _is_sensitive_key(key: str) -> bool:
    return SENSITIVE_ENV_RE.search(key) is not None


def _normalize_base_url(base_url: str | None) -> str | None:
    if base_url is None:
        return None
    return base_url.rstrip("/")


def _load_settings(settings_path: Path) -> dict[str, Any]:
    if not settings_path.exists():
        return {}
    data = json.loads(settings_path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"Claude settings must be a JSON object: {settings_path}")
    return data


def _settings_env(data: dict[str, Any]) -> dict[str, str]:
    env = data.get("env")
    if not isinstance(env, dict):
        return {}
    result: dict[str, str] = {}
    for key, value in env.items():
        if isinstance(key, str) and isinstance(value, str):
            result[key] = value
    return result


def _selected_model(data: dict[str, Any], env: dict[str, str]) -> str | None:
    for key in ("ANTHROPIC_MODEL", "ANTHROPIC_DEFAULT_SONNET_MODEL", "ANTHROPIC_DEFAULT_OPUS_MODEL"):
        value = env.get(key)
        if value:
            return value
    model = data.get("model")
    return model if isinstance(model, str) and model else None


def _settings_summary(settings_path: Path) -> dict[str, Any]:
    data = _load_settings(settings_path)
    env = _settings_env(data)
    base_url = _normalize_base_url(env.get("ANTHROPIC_BASE_URL"))
    model_fields = {key: env[key] for key in MODEL_ENV_KEYS if key in env and env[key]}
    bracketed_model_aliases = sorted({value for value in model_fields.values() if "[" in value or "]" in value})
    sensitive_keys = sorted(key for key, value in env.items() if value and _is_sensitive_key(key))
    selected_model = _selected_model(data, env)
    return {
        "path": str(settings_path),
        "exists": settings_path.exists(),
        "anthropic_base_url": base_url,
        "custom_anthropic_base_url": base_url is not None and base_url != OFFICIAL_ANTHROPIC_BASE_URL,
        "selected_model": selected_model,
        "model_fields": model_fields,
        "bracketed_model_aliases": bracketed_model_aliases,
        "sensitive_env_keys_present": sensitive_keys,
    }


def parse_observed_error(text: str | None) -> dict[str, str] | None:
    if not text:
        return None
    match = OBSERVED_ERROR_RE.search(text)
    if match is None:
        return None
    payload_text = match.group("payload")
    try:
        payload = json.loads(payload_text)
    except json.JSONDecodeError:
        payload = {}
    observed = {"code": match.group("code")}
    for key in ("model", "query_source"):
        value = payload.get(key)
        if isinstance(value, str) and value:
            observed[key] = value
    return observed


def _detect_claude_cli(*, claude_path: str | None, claude_version: str | None) -> dict[str, Any]:
    if claude_version is not None:
        return {
            "available": True,
            "path": claude_path or "claude",
            "version": claude_version.strip(),
            "version_error": None,
        }

    resolved_path = claude_path or shutil.which("claude")
    if resolved_path is None:
        return {"available": False, "path": None, "version": None, "version_error": "claude executable not found"}

    try:
        result = subprocess.run(
            [resolved_path, "--version"],
            text=True,
            encoding="utf-8",
            capture_output=True,
            timeout=10,
            check=False,
        )
    except OSError as exc:
        return {"available": False, "path": resolved_path, "version": None, "version_error": str(exc)}

    output = (result.stdout or result.stderr).strip()
    return {
        "available": result.returncode == 0,
        "path": resolved_path,
        "version": output if result.returncode == 0 else None,
        "version_error": None if result.returncode == 0 else output,
    }


def _findings(settings: dict[str, Any], cli: dict[str, Any], observed_error: dict[str, str] | None) -> list[str]:
    findings = ["no_provider_call_performed"]
    findings.append("claude_cli_available" if cli["available"] else "claude_cli_missing_or_unusable")
    if settings["custom_anthropic_base_url"]:
        findings.append("custom_anthropic_base_url")
    if settings["bracketed_model_aliases"]:
        findings.append("custom_model_aliases_detected")
    if observed_error is not None and observed_error.get("code") == "unrecognized_model":
        findings.append("observed_unrecognized_model")
    return findings


def _route_status(settings: dict[str, Any], cli: dict[str, Any], observed_error: dict[str, str] | None) -> str:
    if not cli["available"]:
        return "blocked"
    if observed_error is not None and observed_error.get("code") == "unrecognized_model":
        return "blocked"
    if settings["custom_anthropic_base_url"] or settings["bracketed_model_aliases"]:
        return "manual_review_required"
    return "ready_for_bounded_runtime_attempt"


def build_preflight(
    *,
    settings_path: Path | None = None,
    claude_path: str | None = None,
    claude_version: str | None = None,
    observed_error_text: str | None = None,
) -> dict[str, Any]:
    resolved_settings_path = settings_path or _default_settings_path()
    settings = _settings_summary(resolved_settings_path)
    cli = _detect_claude_cli(claude_path=claude_path, claude_version=claude_version)
    observed_error = parse_observed_error(observed_error_text)
    status = _route_status(settings, cli, observed_error)
    return {
        "mode": REPORT_MODE,
        "route_status": status,
        "cli": cli,
        "settings": settings,
        "observed_error": observed_error,
        "findings": _findings(settings, cli, observed_error),
        "status_boundary": (
            "Preflight only: no provider calls, no answer generation, no runtime pass, "
            "and no change to platform validation status."
        ),
        "limitations": [
            "This preflight reads local Claude Code route configuration and optional recorded error text only.",
            "It does not edit user settings or prove answer quality.",
            "A ready result means a bounded runtime attempt may be reasonable; it is not runtime validation.",
        ],
    }


def render_markdown_report(report: dict[str, Any]) -> str:
    settings = report["settings"]
    cli = report["cli"]
    observed_error = report.get("observed_error")
    lines = [
        "# Claude Code Route Preflight",
        "",
        f"- Route status: `{report['route_status']}`",
        f"- CLI available: `{cli['available']}`",
        f"- CLI version: `{cli.get('version') or 'unknown'}`",
        f"- Settings file: `{settings['path']}`",
        f"- Custom Anthropic base URL: `{settings['custom_anthropic_base_url']}`",
        f"- Selected model: `{settings.get('selected_model') or 'unknown'}`",
        f"- Sensitive env keys present: `{', '.join(settings['sensitive_env_keys_present']) or 'none'}`",
        "",
        "## Findings",
        "",
    ]
    lines.extend(f"- `{finding}`" for finding in report["findings"])
    if observed_error is not None:
        lines.extend(
            [
                "",
                "## Observed Error",
                "",
                f"- Code: `{observed_error.get('code')}`",
                f"- Model: `{observed_error.get('model', 'unknown')}`",
                f"- Query source: `{observed_error.get('query_source', 'unknown')}`",
            ]
        )
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "No provider calls, answer generation, runtime pass, or settings edits are performed by this preflight.",
            (
                "A `blocked` result keeps the corresponding runtime pending until a bounded rerun produces "
                "a reviewable answer."
            ),
            "This report does not change platform validation status.",
            "",
            "## Limitations",
            "",
        ]
    )
    lines.extend(f"- {limitation}" for limitation in report["limitations"])
    return "\n".join(lines) + "\n"


def main() -> int:
    stdout_reconfigure = getattr(sys.stdout, "reconfigure", None)
    stderr_reconfigure = getattr(sys.stderr, "reconfigure", None)
    if callable(stdout_reconfigure):
        stdout_reconfigure(encoding="utf-8")
    if callable(stderr_reconfigure):
        stderr_reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description="Preflight the local Claude Code route without provider calls.")
    parser.add_argument("--settings", type=Path, help="Claude settings JSON path. Defaults to ~/.claude/settings.json.")
    parser.add_argument("--claude-path", help="Path to the claude executable. Defaults to PATH lookup.")
    parser.add_argument(
        "--claude-version",
        help="Use a pre-recorded Claude Code version string instead of invoking `claude --version`.",
    )
    parser.add_argument("--observed-error", help="Recorded Claude Code error text to parse.")
    parser.add_argument("--observed-error-file", type=Path, help="File containing recorded Claude Code error text.")
    parser.add_argument("--json", action="store_true", help="Emit JSON output.")
    args = parser.parse_args()

    observed_error_text = args.observed_error
    if args.observed_error_file is not None:
        observed_error_text = args.observed_error_file.read_text(encoding="utf-8")

    try:
        report = build_preflight(
            settings_path=args.settings,
            claude_path=args.claude_path,
            claude_version=args.claude_version,
            observed_error_text=observed_error_text,
        )
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"claude-code-route-preflight failed: {exc}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(render_markdown_report(report), end="")
    return 0
