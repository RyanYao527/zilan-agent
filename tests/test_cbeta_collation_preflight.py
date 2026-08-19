from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest
from zilanlib.agama.collation_preflight import AnchorProbe, CollationWork, build_anchor_report, build_preflight

MINI_TEI = """\
<TEI xmlns="http://www.tei-c.org/ns/1.0" xml:id="T02n0099">
  <teiHeader>
    <fileDesc>
      <titleStmt>
        <title xml:lang="zh-Hant" level="m">Mini Agama</title>
        <author>Sample Translator</author>
      </titleStmt>
      <editionStmt>
        <edition>XML TEI P5</edition>
      </editionStmt>
      <extent>1 fascicle</extent>
      <publicationStmt>
        <availability>
          <p>Available for non-commercial use when distributed with this header intact.</p>
        </availability>
        <date>2026-03-17 01:25:01 +0800</date>
      </publicationStmt>
      <sourceDesc>
        <bibl>Taisho source witness</bibl>
      </sourceDesc>
    </fileDesc>
  </teiHeader>
  <text>
    <body>
      <p>sample passage</p>
    </body>
  </text>
</TEI>
"""

ANCHOR_TEI = """\
<TEI xmlns="http://www.tei-c.org/ns/1.0" xml:id="T02n0099">
  <teiHeader>
    <fileDesc>
      <titleStmt><title xml:lang="zh-Hant" level="m">Mini Agama</title></titleStmt>
      <publicationStmt><p>Published for fixture tests.</p></publicationStmt>
      <sourceDesc><p>Fixture source.</p></sourceDesc>
    </fileDesc>
  </teiHeader>
  <text>
    <body>
      <pb n="0002a" xml:id="T02.0099.0002a" ed="T"/>
      <lb n="0002a03" ed="T"/><p xml:id="pT02p0002a0303">爾時，世尊告諸比丘：「色無常，無常即
      <lb n="0002a04" ed="T"/>苦，苦即非我，非我者亦非我所。</p>
    </body>
  </text>
</TEI>
"""


def _work() -> CollationWork:
    return CollationWork(
        work_id="T02n0099",
        label="Mini Agama",
        markdown_file="context/agama/T0099-za-agama.md",
        xml_file="context/agama/_source/T02n0099.xml",
    )


def _write_markdown(root: Path, text: str | None = None) -> None:
    markdown = root / "context" / "agama" / "T0099-za-agama.md"
    markdown.parent.mkdir(parents=True, exist_ok=True)
    markdown.write_text(
        text
        or """# Mini Agama

- 来源：CBETA XML-P5，`T02n0099`，原始 XML 保留于 `_source/T02n0099.xml`。

sample passage
""",
        encoding="utf-8",
    )


def _write_xml(root: Path, text: str = MINI_TEI) -> None:
    source = root / "context" / "agama" / "_source" / "T02n0099.xml"
    source.parent.mkdir(parents=True, exist_ok=True)
    source.write_text(text, encoding="utf-8")


def _anchor_probe() -> AnchorProbe:
    return AnchorProbe(
        probe_id="cbeta-anchor:T02n0099:line-7",
        work_id="T02n0099",
        markdown_file="context/agama/T0099-za-agama.md",
        xml_file="context/agama/_source/T02n0099.xml",
        start_line=7,
        end_line=7,
        expected_start_pb="0002a",
        expected_start_lb="0002a03",
        expected_end_pb="0002a",
        expected_end_lb="0002a04",
    )


def test_cbeta_collation_preflight_reports_ready_xml_markdown_route(tmp_path: Path) -> None:
    _write_markdown(tmp_path)
    _write_xml(tmp_path)

    result = build_preflight(root=tmp_path, works=(_work(),))

    assert result["mode"] == "cbeta-xml-p5-collation-preflight"
    assert result["status"] == "pass"
    assert result["summary"] == {
        "works": 1,
        "ready": 1,
        "review_needed": 0,
        "blocked": 0,
        "issues": 0,
    }
    assert result["works"][0]["status"] == "ready"
    assert result["works"][0]["xml"]["xml_id"] == "T02n0099"
    assert result["works"][0]["xml"]["title"] == "Mini Agama"
    assert result["works"][0]["xml"]["edition"] == "XML TEI P5"
    assert result["works"][0]["xml"]["source_desc"] == "Taisho source witness"
    assert result["works"][0]["markdown"]["references_xml_source"] is True
    assert any("does not perform publication-level collation" in item for item in result["limitations"])


def test_cbeta_collation_preflight_blocks_missing_xml_source(tmp_path: Path) -> None:
    _write_markdown(tmp_path)

    result = build_preflight(root=tmp_path, works=(_work(),))

    assert result["status"] == "fail"
    assert result["summary"]["blocked"] == 1
    assert result["issues"] == [
        {
            "work_id": "T02n0099",
            "severity": "error",
            "code": "missing_xml_source",
            "message": "Missing CBETA XML-P5 source: context/agama/_source/T02n0099.xml",
        }
    ]


@pytest.mark.parametrize(
    ("xml_text", "expected_code"),
    [
        (MINI_TEI.replace('xml:id="T02n0099"', 'xml:id="T02n0000"'), "xml_id_mismatch"),
        (MINI_TEI.replace("<teiHeader>", "<header>").replace("</teiHeader>", "</header>"), "missing_tei_header"),
        (
            MINI_TEI.replace("<publicationStmt>", "<publication>").replace("</publicationStmt>", "</publication>"),
            "missing_publication_stmt",
        ),
        (MINI_TEI.replace("<sourceDesc>", "<source>").replace("</sourceDesc>", "</source>"), "missing_source_desc"),
    ],
)
def test_cbeta_collation_preflight_blocks_xml_metadata_drift(
    tmp_path: Path,
    xml_text: str,
    expected_code: str,
) -> None:
    _write_markdown(tmp_path)
    _write_xml(tmp_path, xml_text)

    result = build_preflight(root=tmp_path, works=(_work(),))

    assert result["status"] == "fail"
    assert result["summary"]["blocked"] == 1
    assert expected_code in {issue["code"] for issue in result["issues"]}


def test_cbeta_collation_preflight_blocks_markdown_work_id_drift(tmp_path: Path) -> None:
    _write_xml(tmp_path)
    _write_markdown(
        tmp_path,
        text="""# Mini Agama

- 原始 XML 保留于 `_source/T02n0099.xml`。

sample passage
""",
    )

    result = build_preflight(root=tmp_path, works=(_work(),))

    assert result["status"] == "fail"
    assert result["summary"]["blocked"] == 1
    assert result["issues"][0]["code"] == "markdown_missing_work_id"
    assert result["works"][0]["markdown"]["references_work_id"] is False


def test_cbeta_collation_preflight_cli_reports_malformed_xml(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    import cbeta_collation_preflight

    _write_markdown(tmp_path)
    _write_xml(tmp_path, "<TEI>")
    monkeypatch.setattr(sys, "argv", ["cbeta_collation_preflight.py", "--root", str(tmp_path), "--json"])

    assert cbeta_collation_preflight.main() == 2
    captured = capsys.readouterr()

    assert "ERROR: Failed to parse CBETA XML-P5 source" in captured.err


def test_cbeta_collation_preflight_blocks_markdown_source_reference_drift(tmp_path: Path) -> None:
    _write_xml(tmp_path)
    _write_markdown(tmp_path, text="# Mini Agama\n\n`T02n0099`\n\nsample passage\n")

    result = build_preflight(root=tmp_path, works=(_work(),))

    assert result["status"] == "fail"
    assert result["summary"]["blocked"] == 1
    assert result["issues"][0]["code"] == "markdown_missing_xml_source_ref"
    assert result["works"][0]["markdown"]["references_xml_source"] is False


def test_cbeta_collation_preflight_cli_runs_json_in_process(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    import cbeta_collation_preflight

    monkeypatch.setattr(sys, "argv", ["cbeta_collation_preflight.py", "--json"])

    assert cbeta_collation_preflight.main() == 0
    captured = capsys.readouterr()
    data = json.loads(captured.out)

    assert data["mode"] == "cbeta-xml-p5-collation-preflight"
    assert data["summary"]["works"] == 4


def test_markdown_line_anchor_report_locates_mini_tei_lb_span(tmp_path: Path) -> None:
    _write_xml(tmp_path, ANCHOR_TEI)
    _write_markdown(
        tmp_path,
        text="""# Mini Agama

## 正文

## 卷 1

爾時，世尊告諸比丘：「色無常，無常即苦，苦即非我，非我者亦非我所。
""",
    )

    result = build_anchor_report(root=tmp_path, probes=(_anchor_probe(),))

    assert result["mode"] == "cbeta-xml-anchor-locator"
    assert result["status"] == "pass"
    assert result["summary"] == {"probes": 1, "located": 1, "blocked": 0, "issues": 0}
    assert result["probes"][0]["status"] == "located"
    assert result["probes"][0]["xml_anchor"] == {
        "start_pb": "0002a",
        "start_pb_xml_id": "T02.0099.0002a",
        "start_lb": "0002a03",
        "end_pb": "0002a",
        "end_pb_xml_id": "T02.0099.0002a",
        "end_lb": "0002a04",
    }
    assert result["probes"][0]["markdown"]["line_text_hash"].startswith("sha256:")
    assert any("does not prove publication-level collation" in item for item in result["limitations"])


def test_markdown_line_anchor_report_blocks_unmatched_markdown_text(tmp_path: Path) -> None:
    _write_xml(tmp_path, ANCHOR_TEI)
    _write_markdown(
        tmp_path,
        text="""# Mini Agama

## 正文

## 卷 1

this passage is not in the XML body
""",
    )

    result = build_anchor_report(root=tmp_path, probes=(_anchor_probe(),))

    assert result["status"] == "fail"
    assert result["summary"] == {"probes": 1, "located": 0, "blocked": 1, "issues": 1}
    assert result["issues"][0]["code"] == "xml_anchor_not_found"


def test_default_markdown_line_anchor_report_checks_committed_fixture_subset() -> None:
    result = build_anchor_report()

    assert result["status"] == "pass"
    assert result["summary"]["probes"] >= 2
    assert result["summary"]["located"] == result["summary"]["probes"]
    assert {probe["probe_id"] for probe in result["probes"]} >= {
        "cbeta-anchor:T02n0099:line-147",
        "cbeta-anchor:T01n0001:line-3997",
        "cbeta-anchor:T01n0001:line-881",
        "cbeta-anchor:T01n0001:line-1829",
    }
