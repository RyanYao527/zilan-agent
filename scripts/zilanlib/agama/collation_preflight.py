from __future__ import annotations

import argparse
import json
import sys
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
NS = {"tei": "http://www.tei-c.org/ns/1.0"}
XML_LANG = "{http://www.w3.org/XML/1998/namespace}lang"
XML_ID = "{http://www.w3.org/XML/1998/namespace}id"


@dataclass(frozen=True)
class CollationWork:
    work_id: str
    label: str
    markdown_file: str
    xml_file: str


DEFAULT_WORKS = (
    CollationWork(
        work_id="T01n0001",
        label="Digha Agama",
        markdown_file="context/agama/T0001-chang-agama.md",
        xml_file="context/agama/_source/T01n0001.xml",
    ),
    CollationWork(
        work_id="T01n0026",
        label="Madhyama Agama",
        markdown_file="context/agama/T0026-zhong-agama.md",
        xml_file="context/agama/_source/T01n0026.xml",
    ),
    CollationWork(
        work_id="T02n0099",
        label="Samyukta Agama",
        markdown_file="context/agama/T0099-za-agama.md",
        xml_file="context/agama/_source/T02n0099.xml",
    ),
    CollationWork(
        work_id="T02n0125",
        label="Ekottarika Agama",
        markdown_file="context/agama/T0125-ekottarika-agama.md",
        xml_file="context/agama/_source/T02n0125.xml",
    ),
)

LIMITATIONS = (
    "Local preflight only; does not perform publication-level collation.",
    "Reads committed CBETA XML-P5 and Markdown files only; no providers, network calls, embeddings, or vector DB.",
    "Parallel Chinese translations, Pali parallels, Sanskrit fragments, and human scholarly judgment remain pending.",
)


class CollationPreflightError(ValueError):
    """Raised when the preflight CLI cannot complete due to malformed input."""


def _text_or_empty(element: ET.Element | None) -> str:
    if element is None:
        return ""
    return " ".join("".join(element.itertext()).split())


def _xml_title(root: ET.Element) -> str:
    for item in root.findall(".//tei:titleStmt/tei:title", NS):
        if item.attrib.get(XML_LANG) == "zh-Hant" and item.attrib.get("level") == "m":
            return _text_or_empty(item)
    titles = root.findall(".//tei:titleStmt/tei:title", NS)
    return _text_or_empty(titles[0]) if titles else ""


def _xml_metadata(path: Path) -> dict[str, Any]:
    try:
        root = ET.parse(path).getroot()
    except ET.ParseError as exc:
        raise CollationPreflightError(f"Failed to parse CBETA XML-P5 source {path.as_posix()}: {exc}") from exc

    return {
        "xml_id": root.attrib.get(XML_ID, path.stem),
        "title": _xml_title(root),
        "author": _text_or_empty(root.find(".//tei:titleStmt/tei:author", NS)),
        "edition": _text_or_empty(root.find(".//tei:editionStmt/tei:edition", NS)),
        "extent": _text_or_empty(root.find(".//tei:extent", NS)),
        "publication_date": _text_or_empty(root.find(".//tei:publicationStmt/tei:date", NS)),
        "availability": _text_or_empty(root.find(".//tei:publicationStmt/tei:availability", NS)),
        "source_desc": _text_or_empty(root.find(".//tei:sourceDesc", NS)),
        "has_tei_header": root.find(".//tei:teiHeader", NS) is not None,
        "has_publication_stmt": root.find(".//tei:publicationStmt", NS) is not None,
        "has_source_desc": root.find(".//tei:sourceDesc", NS) is not None,
    }


def _issue(*, work_id: str, severity: str, code: str, message: str) -> dict[str, str]:
    return {"work_id": work_id, "severity": severity, "code": code, "message": message}


def _work_status(work_issues: list[dict[str, str]]) -> str:
    # Reserved for future warning-level checks; current route blockers are intentionally errors.
    if any(issue["severity"] == "error" for issue in work_issues):
        return "blocked"
    if work_issues:
        return "review_needed"
    return "ready"


def _top_status(issues: list[dict[str, str]]) -> str:
    if any(issue["severity"] == "error" for issue in issues):
        return "fail"
    if issues:
        return "review_needed"
    return "pass"


def build_preflight(root: Path = ROOT, works: tuple[CollationWork, ...] = DEFAULT_WORKS) -> dict[str, Any]:
    entries: list[dict[str, Any]] = []
    issues: list[dict[str, str]] = []

    for work in works:
        xml_path = root / work.xml_file
        markdown_path = root / work.markdown_file
        work_issues: list[dict[str, str]] = []
        xml: dict[str, Any] | None = None

        if not xml_path.exists():
            work_issues.append(
                _issue(
                    work_id=work.work_id,
                    severity="error",
                    code="missing_xml_source",
                    message=f"Missing CBETA XML-P5 source: {work.xml_file}",
                )
            )
        else:
            xml = _xml_metadata(xml_path)
            if xml["xml_id"] != work.work_id:
                work_issues.append(
                    _issue(
                        work_id=work.work_id,
                        severity="error",
                        code="xml_id_mismatch",
                        message=f"CBETA XML-P5 xml:id must be {work.work_id}.",
                    )
                )
            for field, code in (
                ("has_tei_header", "missing_tei_header"),
                ("has_publication_stmt", "missing_publication_stmt"),
                ("has_source_desc", "missing_source_desc"),
            ):
                if not xml[field]:
                    work_issues.append(
                        _issue(
                            work_id=work.work_id,
                            severity="error",
                            code=code,
                            message=f"CBETA XML-P5 source lacks {field.replace('_', ' ')}.",
                        )
                    )

        markdown: dict[str, Any]
        if not markdown_path.exists():
            markdown = {
                "path": work.markdown_file,
                "exists": False,
                "references_work_id": False,
                "references_xml_source": False,
            }
            work_issues.append(
                _issue(
                    work_id=work.work_id,
                    severity="error",
                    code="missing_markdown_view",
                    message=f"Missing generated Markdown view: {work.markdown_file}",
                )
            )
        else:
            markdown_text = markdown_path.read_text(encoding="utf-8")
            markdown = {
                "path": work.markdown_file,
                "exists": True,
                "references_work_id": f"`{work.work_id}`" in markdown_text,
                "references_xml_source": f"_source/{xml_path.name}" in markdown_text,
            }
            if not markdown["references_work_id"]:
                work_issues.append(
                    _issue(
                        work_id=work.work_id,
                        severity="error",
                        code="markdown_missing_work_id",
                        message=f"Markdown view must reference CBETA work id {work.work_id}.",
                    )
                )
            if not markdown["references_xml_source"]:
                work_issues.append(
                    _issue(
                        work_id=work.work_id,
                        severity="error",
                        code="markdown_missing_xml_source_ref",
                        message=f"Markdown view must reference XML source _source/{xml_path.name}.",
                    )
                )

        status = _work_status(work_issues)
        issues.extend(work_issues)
        entries.append(
            {
                "work_id": work.work_id,
                "label": work.label,
                "status": status,
                "markdown": markdown,
                "xml": xml,
                "route": {
                    "working_corpus": work.markdown_file,
                    "xml_p5_source": work.xml_file,
                    "publication_boundary": "publication-level use requires XML-P5 and parallel-text collation",
                },
                "issues": work_issues,
            }
        )

    summary = {
        "works": len(entries),
        "ready": sum(1 for item in entries if item["status"] == "ready"),
        "review_needed": sum(1 for item in entries if item["status"] == "review_needed"),
        "blocked": sum(1 for item in entries if item["status"] == "blocked"),
        "issues": len(issues),
    }
    return {
        "mode": "cbeta-xml-p5-collation-preflight",
        "status": _top_status(issues),
        "summary": summary,
        "works": entries,
        "issues": issues,
        "limitations": list(LIMITATIONS),
    }


def _print_text(result: dict[str, Any]) -> None:
    summary = result["summary"]
    print(f"mode: {result['mode']}")
    print(f"status: {result['status']}")
    print(
        "summary: "
        f"works={summary['works']}, "
        f"ready={summary['ready']}, "
        f"review_needed={summary['review_needed']}, "
        f"blocked={summary['blocked']}, "
        f"issues={summary['issues']}"
    )
    for item in result["works"]:
        print(f"- {item['work_id']}: {item['status']} ({item['markdown']['path']} -> {item['route']['xml_p5_source']})")
    if result["issues"]:
        print("issues:")
        for item in result["issues"]:
            print(f"- {item['work_id']} {item['severity']} {item['code']}: {item['message']}")
    print("limitations:")
    for item in result["limitations"]:
        print(f"- {item}")


def _reconfigure_stream(stream: object) -> None:
    reconfigure = getattr(stream, "reconfigure", None)
    if callable(reconfigure):
        reconfigure(encoding="utf-8")


def main() -> int:
    _reconfigure_stream(sys.stdout)
    _reconfigure_stream(sys.stderr)

    parser = argparse.ArgumentParser(
        description="Preflight the local publication-level route from Agama Markdown hits back to CBETA XML-P5."
    )
    parser.add_argument("--root", type=Path, default=ROOT, help="Repository root.")
    parser.add_argument("--json", action="store_true", dest="json_output", help="Emit JSON.")
    args = parser.parse_args()

    try:
        result = build_preflight(root=args.root)
    except CollationPreflightError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    if args.json_output:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        _print_text(result)
    return 0 if result["status"] != "fail" else 1


__all__ = [
    "CollationPreflightError",
    "CollationWork",
    "DEFAULT_WORKS",
    "LIMITATIONS",
    "build_preflight",
    "main",
]
