from __future__ import annotations

from pathlib import Path
from typing import Any


def display_path(path: Path, *, root: Path) -> str:
    """Return a stable repository-relative path when possible."""
    try:
        return path.resolve().relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def load_yaml_mapping(
    path: Path,
    *,
    root: Path,
    error_type: type[ValueError],
    missing_message: str,
    missing_file_label: str,
    parse_label: str,
    mapping_label: str,
) -> dict[str, Any]:
    """Load a YAML file and require a mapping at the top level."""
    shown_path = display_path(path, root=root)
    if not path.exists():
        raise error_type(f"{missing_file_label}: {shown_path}")

    try:
        import yaml
    except ModuleNotFoundError as exc:
        raise error_type(missing_message) from exc

    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001 - keep parser failures visible in CLI output.
        raise error_type(f"{parse_label} {shown_path}: {exc}") from exc

    if not isinstance(data, dict):
        raise error_type(f"{mapping_label}: {shown_path}")
    return data
