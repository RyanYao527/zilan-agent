from pathlib import Path

import build_agama_context as builder

MINI_TEI = """\
<TEI xmlns="http://www.tei-c.org/ns/1.0" xml:id="T01n0001">
  <teiHeader>
    <fileDesc>
      <titleStmt>
        <title xml:lang="zh-Hant" level="m">Mini Sutra</title>
        <author>Sample Translator</author>
      </titleStmt>
      <extent>1 fascicle</extent>
    </fileDesc>
  </teiHeader>
  <text>
    <body>
      <milestone unit="juan" n="1"/>
      <p>Alpha <note>ignored note</note><choice><orig>Wrong</orig><corr>Correct</corr></choice> Omega</p>
      <p>Beta<lb/>Gamma<pb n="0001a"/></p>
    </body>
  </text>
</TEI>
"""


def test_normalize_space_collapses_inline_newlines_and_blank_runs() -> None:
    assert builder.normalize_space(" Alpha \n Beta \n\n\n Gamma ") == "AlphaBeta\n\nGamma"


def test_build_text_file_extracts_metadata_and_body(tmp_path: Path, monkeypatch) -> None:
    agama_dir = tmp_path / "agama"
    source_dir = agama_dir / "_source"
    source_dir.mkdir(parents=True)
    xml_path = source_dir / "T01n0001.xml"
    xml_path.write_text(MINI_TEI, encoding="utf-8")

    monkeypatch.setattr(builder, "AGAMA_DIR", agama_dir)
    out_path = builder.build_text_file(xml_path)

    assert out_path == agama_dir / "T0001-chang-agama.md"
    text = out_path.read_text(encoding="utf-8")
    assert "# Mini Sutra" in text
    assert "_source/T01n0001.xml" in text
    assert "Sample Translator" in text
    assert "1 fascicle" in text
    assert "Alpha Correct Omega" in text
    assert "Omega Omega" not in text
    assert "ignored note" not in text
    assert "Wrong" not in text
    assert "BetaGamma" in text
    assert "[0001a]" in text


def test_build_index_writes_fixture_safe_index(tmp_path: Path, monkeypatch) -> None:
    agama_dir = tmp_path / "agama"
    agama_dir.mkdir()
    monkeypatch.setattr(builder, "AGAMA_DIR", agama_dir)

    out_path = builder.build_index([])

    assert out_path == agama_dir / "agama-index.md"
    text = out_path.read_text(encoding="utf-8")
    assert "T01n 0001" in text
    assert "`T0001-chang-agama.md`" in text
    assert "`_source/`" in text


def test_main_builds_text_and_index_from_temp_source(tmp_path: Path, monkeypatch, capsys) -> None:
    agama_dir = tmp_path / "agama"
    source_dir = agama_dir / "_source"
    source_dir.mkdir(parents=True)
    (source_dir / "T01n0001.xml").write_text(MINI_TEI, encoding="utf-8")

    monkeypatch.setattr(builder, "AGAMA_DIR", agama_dir)
    monkeypatch.setattr(builder, "SOURCE_DIR", source_dir)

    builder.main()

    captured = capsys.readouterr()
    assert "T0001-chang-agama.md" in captured.out
    assert "agama-index.md" in captured.out
    assert (agama_dir / "T0001-chang-agama.md").exists()
    assert (agama_dir / "agama-index.md").exists()
