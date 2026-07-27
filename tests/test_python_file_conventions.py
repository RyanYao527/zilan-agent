from __future__ import annotations

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _python_files() -> list[Path]:
    files = [
        path
        for root in (ROOT / "scripts", ROOT / "tests")
        for path in root.rglob("*.py")
        if "__pycache__" not in path.parts
    ]
    return sorted(files)


def _is_string_expr(statement: ast.stmt) -> bool:
    return (
        isinstance(statement, ast.Expr)
        and isinstance(statement.value, ast.Constant)
        and isinstance(statement.value.value, str)
    )


def _has_future_annotations(path: Path) -> bool:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    body = tree.body
    if body and _is_string_expr(body[0]):
        body = body[1:]

    if not body:
        return False

    first_statement = body[0]
    if not isinstance(first_statement, ast.ImportFrom) or first_statement.module != "__future__":
        return False
    if not any(alias.name == "annotations" for alias in first_statement.names):
        return False

    return not (len(body) > 1 and _is_string_expr(body[1]))

def test_python_files_use_future_annotations() -> None:
    missing = [
        str(path.relative_to(ROOT)).replace("\\", "/")
        for path in _python_files()
        if not _has_future_annotations(path)
    ]

    assert missing == []


def test_future_annotations_preserves_module_docstring(tmp_path: Path) -> None:
    good = tmp_path / "good.py"
    good.write_text(
        '"""Module docs."""\n\nfrom __future__ import annotations\n\nVALUE: list[str] = []\n',
        encoding="utf-8",
    )

    bad = tmp_path / "bad.py"
    bad.write_text(
        'from __future__ import annotations\n\n"""Module docs."""\n\nVALUE: list[str] = []\n',
        encoding="utf-8",
    )

    no_docstring = tmp_path / "no_docstring.py"
    no_docstring.write_text(
        "from __future__ import annotations\n\nVALUE: list[str] = []\n",
        encoding="utf-8",
    )

    assert _has_future_annotations(good)
    assert not _has_future_annotations(bad)
    assert _has_future_annotations(no_docstring)
