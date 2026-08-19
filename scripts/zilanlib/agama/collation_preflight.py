from __future__ import annotations

import argparse
import hashlib
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


@dataclass(frozen=True)
class AnchorProbe:
    probe_id: str
    work_id: str
    markdown_file: str
    xml_file: str
    start_line: int
    end_line: int
    expected_start_pb: str | None = None
    expected_start_lb: str | None = None
    expected_end_pb: str | None = None
    expected_end_lb: str | None = None


@dataclass(frozen=True)
class _XmlAnchor:
    pb: str | None
    pb_xml_id: str | None
    lb: str | None


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

DEFAULT_ANCHOR_PROBES = (
    AnchorProbe(
        probe_id="cbeta-anchor:T02n0099:line-147",
        work_id="T02n0099",
        markdown_file="context/agama/T0099-za-agama.md",
        xml_file="context/agama/_source/T02n0099.xml",
        start_line=147,
        end_line=149,
        expected_start_pb="0002a",
        expected_start_lb="0002a03",
        expected_end_pb="0002a",
        expected_end_lb="0002a10",
    ),
    AnchorProbe(
        probe_id="cbeta-anchor:T01n0001:line-3997",
        work_id="T01n0001",
        markdown_file="context/agama/T0001-chang-agama.md",
        xml_file="context/agama/_source/T01n0001.xml",
        start_line=3997,
        end_line=3997,
        expected_start_pb="0061c",
        expected_start_lb="0061c06",
        expected_end_pb="0061c",
        expected_end_lb="0061c22",
    ),
    AnchorProbe(
        probe_id="cbeta-anchor:T01n0001:line-881",
        work_id="T01n0001",
        markdown_file="context/agama/T0001-chang-agama.md",
        xml_file="context/agama/_source/T01n0001.xml",
        start_line=881,
        end_line=881,
        expected_start_pb="0009b",
        expected_start_lb="0009b12",
        expected_end_pb="0009b",
        expected_end_lb="0009b12",
    ),
    AnchorProbe(
        probe_id="cbeta-anchor:T01n0001:line-1829",
        work_id="T01n0001",
        markdown_file="context/agama/T0001-chang-agama.md",
        xml_file="context/agama/_source/T01n0001.xml",
        start_line=1829,
        end_line=1829,
        expected_start_pb="0021a",
        expected_start_lb="0021a18",
        expected_end_pb="0021a",
        expected_end_lb="0021a18",
    ),
)

LIMITATIONS = (
    "Local preflight only; does not perform publication-level collation.",
    "Reads committed CBETA XML-P5 and Markdown files only; no providers, network calls, embeddings, or vector DB.",
    "Parallel Chinese translations, Pali parallels, Sanskrit fragments, and human scholarly judgment remain pending.",
)
ANCHOR_LIMITATIONS = (
    "Local anchor locator only; does not prove publication-level collation.",
    "Matches committed Markdown line text against committed CBETA XML-P5 body text by normalized exact text.",
    "Parallel-text comparison, variant witnesses, and human scholarly judgment remain pending.",
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


def _probe_issue(*, probe_id: str, severity: str, code: str, message: str) -> dict[str, str]:
    return {"probe_id": probe_id, "severity": severity, "code": code, "message": message}


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


def _line_text_hash(text: str) -> str:
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    return f"sha256:{digest}"


def _selected_markdown_text(lines: list[str], start_line: int, end_line: int) -> str:
    return "\n".join(line.strip() for line in lines[start_line - 1 : end_line] if line.strip())


def _normalized_text(text: str) -> str:
    return "".join(char for char in text if not char.isspace())


def _local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1] if "}" in tag else tag


def _xml_body_index(path: Path) -> tuple[str, list[_XmlAnchor]]:
    try:
        root = ET.parse(path).getroot()
    except ET.ParseError as exc:
        raise CollationPreflightError(f"Failed to parse CBETA XML-P5 source {path.as_posix()}: {exc}") from exc

    body = root.find(".//tei:text/tei:body", NS)
    if body is None:
        body = root.find(".//tei:body", NS)
    if body is None:
        return "", []

    state: dict[str, str | None] = {"pb": None, "pb_xml_id": None, "lb": None}
    chars: list[str] = []
    anchors: list[_XmlAnchor] = []

    def append_text(text: str | None) -> None:
        if not text:
            return
        anchor = _XmlAnchor(pb=state["pb"], pb_xml_id=state["pb_xml_id"], lb=state["lb"])
        for char in text:
            if char.isspace():
                continue
            chars.append(char)
            anchors.append(anchor)

    def walk(element: ET.Element) -> None:
        local = _local_name(element.tag)
        if local == "pb":
            state["pb"] = element.attrib.get("n")
            state["pb_xml_id"] = element.attrib.get(XML_ID)
        elif local == "lb":
            state["lb"] = element.attrib.get("n")

        append_text(element.text)
        for child in list(element):
            walk(child)
            append_text(child.tail)

    walk(body)
    return "".join(chars), anchors


def _anchor_dict(start_anchor: _XmlAnchor, end_anchor: _XmlAnchor) -> dict[str, str | None]:
    return {
        "start_pb": start_anchor.pb,
        "start_pb_xml_id": start_anchor.pb_xml_id,
        "start_lb": start_anchor.lb,
        "end_pb": end_anchor.pb,
        "end_pb_xml_id": end_anchor.pb_xml_id,
        "end_lb": end_anchor.lb,
    }


def build_anchor_report(root: Path = ROOT, probes: tuple[AnchorProbe, ...] = DEFAULT_ANCHOR_PROBES) -> dict[str, Any]:
    entries: list[dict[str, Any]] = []
    issues: list[dict[str, str]] = []
    xml_indexes: dict[Path, tuple[str, list[_XmlAnchor]]] = {}

    for probe in probes:
        probe_issues: list[dict[str, str]] = []
        markdown_path = root / probe.markdown_file
        xml_path = root / probe.xml_file
        markdown: dict[str, Any] = {
            "path": probe.markdown_file,
            "line_range": {"start": probe.start_line, "end": probe.end_line},
            "line_text_hash": None,
        }
        xml_anchor: dict[str, str | None] | None = None

        if probe.start_line < 1 or probe.end_line < probe.start_line:
            probe_issues.append(
                _probe_issue(
                    probe_id=probe.probe_id,
                    severity="error",
                    code="invalid_markdown_line_range",
                    message="Markdown line range must be positive and ordered.",
                )
            )
        elif not markdown_path.exists():
            probe_issues.append(
                _probe_issue(
                    probe_id=probe.probe_id,
                    severity="error",
                    code="missing_markdown_view",
                    message=f"Missing generated Markdown view: {probe.markdown_file}",
                )
            )
        elif not xml_path.exists():
            probe_issues.append(
                _probe_issue(
                    probe_id=probe.probe_id,
                    severity="error",
                    code="missing_xml_source",
                    message=f"Missing CBETA XML-P5 source: {probe.xml_file}",
                )
            )
        else:
            lines = markdown_path.read_text(encoding="utf-8").splitlines()
            if probe.end_line > len(lines):
                probe_issues.append(
                    _probe_issue(
                        probe_id=probe.probe_id,
                        severity="error",
                        code="markdown_line_range_exceeds_source",
                        message=f"Markdown line range exceeds source length: {probe.markdown_file}",
                    )
                )
            else:
                selected_text = _selected_markdown_text(lines, probe.start_line, probe.end_line)
                markdown["line_text_hash"] = _line_text_hash(selected_text)
                needle = _normalized_text(selected_text)
                if not needle:
                    probe_issues.append(
                        _probe_issue(
                            probe_id=probe.probe_id,
                            severity="error",
                            code="empty_markdown_line_range",
                            message="Markdown line range must include non-empty text.",
                        )
                    )
                else:
                    if xml_path not in xml_indexes:
                        xml_indexes[xml_path] = _xml_body_index(xml_path)
                    xml_text, anchors = xml_indexes[xml_path]
                    start_index = xml_text.find(needle)
                    if start_index < 0:
                        probe_issues.append(
                            _probe_issue(
                                probe_id=probe.probe_id,
                                severity="error",
                                code="xml_anchor_not_found",
                                message="Markdown line text was not found in the CBETA XML-P5 body.",
                            )
                        )
                    else:
                        start_anchor = anchors[start_index]
                        end_anchor = anchors[start_index + len(needle) - 1]
                        xml_anchor = _anchor_dict(start_anchor, end_anchor)
                        expected = {
                            "start_pb": probe.expected_start_pb,
                            "start_lb": probe.expected_start_lb,
                            "end_pb": probe.expected_end_pb,
                            "end_lb": probe.expected_end_lb,
                        }
                        for field, expected_value in expected.items():
                            if expected_value is not None and xml_anchor[field] != expected_value:
                                probe_issues.append(
                                    _probe_issue(
                                        probe_id=probe.probe_id,
                                        severity="error",
                                        code="xml_anchor_mismatch",
                                        message=f"{field} expected {expected_value}, got {xml_anchor[field]}.",
                                    )
                                )

        status = "blocked" if probe_issues else "located"
        issues.extend(probe_issues)
        entries.append(
            {
                "probe_id": probe.probe_id,
                "work_id": probe.work_id,
                "status": status,
                "markdown": markdown,
                "xml_source": probe.xml_file,
                "xml_anchor": xml_anchor,
                "issues": probe_issues,
            }
        )

    summary = {
        "probes": len(entries),
        "located": sum(1 for item in entries if item["status"] == "located"),
        "blocked": sum(1 for item in entries if item["status"] == "blocked"),
        "issues": len(issues),
    }
    return {
        "mode": "cbeta-xml-anchor-locator",
        "status": _top_status(issues),
        "summary": summary,
        "probes": entries,
        "issues": issues,
        "limitations": list(ANCHOR_LIMITATIONS),
    }


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
    parser.add_argument(
        "--check-anchors",
        action="store_true",
        help="Also run the checked Markdown-line to XML pb/lb anchor locator probes.",
    )
    args = parser.parse_args()

    try:
        result = build_preflight(root=args.root)
        if args.check_anchors:
            result["anchor_report"] = build_anchor_report(root=args.root)
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
    "AnchorProbe",
    "CollationWork",
    "DEFAULT_ANCHOR_PROBES",
    "DEFAULT_WORKS",
    "LIMITATIONS",
    "build_anchor_report",
    "build_preflight",
    "main",
]
