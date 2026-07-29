# Third-Party Notices

This file documents third-party source material included in or excerpted by `zilan-agent`.

## Project-Original Material

Unless a file states otherwise, project-original software, prompt definitions, documentation, tests, and validation scripts authored in this repository are provided under the MIT License in `LICENSE`.

## CBETA-Derived Agama Corpus

The local Agama corpus is derived from CBETA XML-P5 material published by CBETA:

- Source repository: https://github.com/cbeta-org/xml-p5
- Copyright and usage terms: https://www.cbeta.org/copyright.php

CBETA-derived material is not relicensed under the MIT License by this repository. CBETA currently describes its database as non-commercial and, except for specially noted materials, released under Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0). Use, copying, modification, redistribution, publication, or commercial use of CBETA-derived material must follow the CBETA terms and any attribution, non-commercial, share-alike, or other requirements described by CBETA.

Primary covered paths:

- `context/agama/_source/T01n0001.xml`
- `context/agama/_source/T01n0026.xml`
- `context/agama/_source/T02n0099.xml`
- `context/agama/_source/T02n0125.xml`
- `context/agama/T0001-chang-agama.md`
- `context/agama/T0026-zhong-agama.md`
- `context/agama/T0099-za-agama.md`
- `context/agama/T0125-ekottarika-agama.md`

Derivative or excerpt-bearing paths may also include:

- `context/agama/agama-index.md`
- `tests/fixtures/retrieval_chunks/semantic_chunks.yaml`
- `zilan_contract/fixtures/retrieval_chunks/semantic_chunks.yaml`
- `tests/fixtures/retrieval_chunks/agama_bad_anchor_chunks.yaml`
- `tests/fixtures/answers/`
- `zilan_contract/fixtures/answers/`
- `docs/runtime-evidence/`
- generated citations or excerpts emitted by `scripts/search_agama.py` and copied into validation logs

The Markdown files under `context/agama/` are searchable working views generated from the XML-P5 corpus. They are not a critical edition. Publication-level use should verify passages against CBETA XML-P5 and relevant parallel texts where appropriate.