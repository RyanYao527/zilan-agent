from __future__ import annotations

import re
from pathlib import Path, PurePosixPath
from typing import cast

from zilanlib.agama.collation_preflight import AnchorProbe, build_anchor_report
from zilanlib.yaml_io import load_yaml_for_validation

COLLATION_FIXTURE_DIR = Path("tests/fixtures/collation")
ANCHOR_PROBES_PATH = COLLATION_FIXTURE_DIR / "cbeta_anchor_probes.yaml"
PARALLEL_CANDIDATES_PATH = COLLATION_FIXTURE_DIR / "high_value_no_self_parallel_candidates.yaml"
RETRIEVAL_CHUNKS_PATH = "tests/fixtures/retrieval_chunks/semantic_chunks.yaml"
ALLOWED_PARALLEL_RELATIONS = ("doctrinal_theme_parallel", "possible_textual_parallel")
ALLOWED_PARALLEL_CONFIDENCE = ("review_candidate",)
ALLOWED_CANDIDATE_SET_STATUSES = ("candidate_map_only", "manual_theme_collation_recorded")
ALLOWED_COLLATION_STATUSES = ("pending_manual_collation", "manual_theme_collation_recorded")
MANUAL_COLLATION_EVIDENCE_STATUS = "manual_theme_collation_recorded"


def _is_text(value: object) -> bool:
    return isinstance(value, str) and bool(value)


def _line_range(value: object) -> tuple[int, int] | None:
    if not isinstance(value, dict):
        return None
    start = value.get("start")
    end = value.get("end")
    if isinstance(start, int) and isinstance(end, int) and start >= 1 and end >= start:
        return start, end
    return None


def _anchor_value(value: object, field: str) -> str | None:
    if not isinstance(value, dict):
        return None
    item = value.get(field)
    return item if isinstance(item, str) and item else None


def _load_anchor_probes(
    root: Path,
    failures: list[str],
    warnings: list[str],
    strict_yaml: bool,
) -> tuple[AnchorProbe, ...]:
    data = load_yaml_for_validation(root, ANCHOR_PROBES_PATH.as_posix(), failures, warnings, strict_yaml)
    if data is None:
        return ()
    if not isinstance(data, dict):
        failures.append(f"{ANCHOR_PROBES_PATH.as_posix()} must contain a mapping.")
        return ()
    if data.get("version") != 1:
        failures.append(f"{ANCHOR_PROBES_PATH.as_posix()} version must be 1.")

    raw_probes = data.get("anchor_probes")
    if not isinstance(raw_probes, list) or not raw_probes:
        failures.append(f"{ANCHOR_PROBES_PATH.as_posix()} anchor_probes must be a non-empty list.")
        return ()

    probes: list[AnchorProbe] = []
    seen_ids: set[str] = set()
    for item in raw_probes:
        if not isinstance(item, dict):
            failures.append(f"{ANCHOR_PROBES_PATH.as_posix()} contains a non-mapping anchor_probes item.")
            continue

        probe_id = item.get("probe_id")
        if not _is_text(probe_id) or not re.fullmatch(r"cbeta-anchor:T\d{2}n\d{4}:line-\d+", cast(str, probe_id)):
            failures.append(f"{ANCHOR_PROBES_PATH.as_posix()} anchor probe id must use cbeta-anchor:<work>:line-<n>.")
            continue
        probe_id = cast(str, probe_id)
        if probe_id in seen_ids:
            failures.append(f"{ANCHOR_PROBES_PATH.as_posix()} contains duplicate anchor probe id: {probe_id}")
            continue
        seen_ids.add(probe_id)

        work_id = item.get("work_id")
        source_file = item.get("source_file")
        xml_file = item.get("xml_file")
        line_range = _line_range(item.get("line_range"))
        if not _is_text(work_id) or not _is_text(source_file) or not _is_text(xml_file) or line_range is None:
            failures.append(f"{ANCHOR_PROBES_PATH.as_posix()} {probe_id} has invalid source fields.")
            continue
        expected_start = item.get("expected_start")
        expected_end = item.get("expected_end")
        probes.append(
            AnchorProbe(
                probe_id=probe_id,
                work_id=cast(str, work_id),
                markdown_file=cast(str, source_file),
                xml_file=cast(str, xml_file),
                start_line=line_range[0],
                end_line=line_range[1],
                expected_start_pb=_anchor_value(expected_start, "pb"),
                expected_start_lb=_anchor_value(expected_start, "lb"),
                expected_end_pb=_anchor_value(expected_end, "pb"),
                expected_end_lb=_anchor_value(expected_end, "lb"),
            )
        )

    return tuple(probes)


def _validate_anchor_probe_locations(root: Path, probes: tuple[AnchorProbe, ...], failures: list[str]) -> None:
    if not probes:
        return
    result = build_anchor_report(root=root, probes=probes)
    for issue in result["issues"]:
        failures.append(
            f"{ANCHOR_PROBES_PATH.as_posix()} {issue['probe_id']} {issue['code']}: {issue['message']}"
        )


def _load_retrieval_chunk_ids(root: Path, failures: list[str], warnings: list[str], strict_yaml: bool) -> set[str]:
    data = load_yaml_for_validation(root, RETRIEVAL_CHUNKS_PATH, failures, warnings, strict_yaml)
    if not isinstance(data, dict) or not isinstance(data.get("chunks"), list):
        return set()
    return {
        item["chunk_id"]
        for item in data["chunks"]
        if isinstance(item, dict) and isinstance(item.get("chunk_id"), str)
    }


def _validate_manual_collation_evidence(
    root: Path,
    value: object,
    context: str,
    required_terms: tuple[str, ...],
    failures: list[str],
) -> None:
    generic_error = (
        f"{PARALLEL_CANDIDATES_PATH.as_posix()} {context} manual_collation_evidence must reference "
        "an existing docs/runtime-evidence Markdown file."
    )
    if not _is_text(value):
        failures.append(generic_error)
        return

    evidence_path = PurePosixPath(cast(str, value))
    if evidence_path.is_absolute() or evidence_path.suffix != ".md" or evidence_path.parts[:2] != (
        "docs",
        "runtime-evidence",
    ):
        failures.append(generic_error)
        return

    full_path = root.joinpath(*evidence_path.parts)
    if not full_path.is_file():
        failures.append(generic_error)
        return

    evidence_text = full_path.read_text(encoding="utf-8")
    missing_terms = tuple(term for term in required_terms if term not in evidence_text)
    if missing_terms:
        failures.append(
            f"{PARALLEL_CANDIDATES_PATH.as_posix()} {context} manual_collation_evidence must mention: "
            f"{', '.join(missing_terms)}."
        )


def _validate_parallel_candidates(
    root: Path,
    anchor_probe_ids: set[str],
    retrieval_chunk_ids: set[str],
    failures: list[str],
    warnings: list[str],
    strict_yaml: bool,
) -> None:
    data = load_yaml_for_validation(root, PARALLEL_CANDIDATES_PATH.as_posix(), failures, warnings, strict_yaml)
    if data is None:
        return
    if not isinstance(data, dict):
        failures.append(f"{PARALLEL_CANDIDATES_PATH.as_posix()} must contain a mapping.")
        return
    if data.get("version") != 1:
        failures.append(f"{PARALLEL_CANDIDATES_PATH.as_posix()} version must be 1.")

    candidate_sets = data.get("candidate_sets")
    if not isinstance(candidate_sets, list) or not candidate_sets:
        failures.append(f"{PARALLEL_CANDIDATES_PATH.as_posix()} candidate_sets must be a non-empty list.")
        return

    seen_ids: set[str] = set()
    for candidate_set in candidate_sets:
        if not isinstance(candidate_set, dict):
            failures.append(f"{PARALLEL_CANDIDATES_PATH.as_posix()} contains a non-mapping candidate_sets item.")
            continue
        set_id = candidate_set.get("set_id")
        if not _is_text(set_id) or not re.fullmatch(r"[a-z0-9][a-z0-9-]*", cast(str, set_id)):
            failures.append(f"{PARALLEL_CANDIDATES_PATH.as_posix()} candidate set id must be kebab-case.")
            continue
        set_id = cast(str, set_id)
        if set_id in seen_ids:
            failures.append(f"{PARALLEL_CANDIDATES_PATH.as_posix()} contains duplicate candidate set id: {set_id}")
            continue
        seen_ids.add(set_id)

        status = candidate_set.get("status")
        if status not in ALLOWED_CANDIDATE_SET_STATUSES:
            failures.append(
                f"{PARALLEL_CANDIDATES_PATH.as_posix()} {set_id} status must be "
                "candidate_map_only or manual_theme_collation_recorded."
            )
        source_probe = candidate_set.get("source_anchor_probe")
        if source_probe not in anchor_probe_ids:
            failures.append(
                f"{PARALLEL_CANDIDATES_PATH.as_posix()} {set_id} "
                "source_anchor_probe must reference a known anchor probe."
            )
        source_chunk_id = candidate_set.get("source_chunk_id")
        if source_chunk_id not in retrieval_chunk_ids:
            failures.append(
                f"{PARALLEL_CANDIDATES_PATH.as_posix()} {set_id} source_chunk_id must reference a retrieval chunk."
            )

        boundaries = candidate_set.get("boundaries")
        if (
            not isinstance(boundaries, list)
            or not any(
                isinstance(item, str) and "does not prove publication-level equivalence" in item
                for item in boundaries
            )
        ):
            failures.append(
                f"{PARALLEL_CANDIDATES_PATH.as_posix()} {set_id} boundaries must preserve the non-equivalence boundary."
            )
        if status == MANUAL_COLLATION_EVIDENCE_STATUS:
            required_terms = (set_id,) + ((cast(str, source_probe),) if _is_text(source_probe) else ())
            _validate_manual_collation_evidence(
                root,
                candidate_set.get("manual_collation_evidence"),
                set_id,
                required_terms,
                failures,
            )

        parallels = candidate_set.get("candidate_parallels")
        if not isinstance(parallels, list) or not parallels:
            failures.append(f"{PARALLEL_CANDIDATES_PATH.as_posix()} {set_id} candidate_parallels must be non-empty.")
            continue
        for parallel in parallels:
            if not isinstance(parallel, dict):
                failures.append(f"{PARALLEL_CANDIDATES_PATH.as_posix()} {set_id} contains a non-mapping candidate.")
                continue
            anchor_probe = parallel.get("anchor_probe")
            if anchor_probe not in anchor_probe_ids:
                failures.append(
                    f"{PARALLEL_CANDIDATES_PATH.as_posix()} {set_id} candidate {anchor_probe} "
                    "must reference a known anchor probe."
                )
            chunk_id = parallel.get("chunk_id")
            if chunk_id not in retrieval_chunk_ids:
                failures.append(
                    f"{PARALLEL_CANDIDATES_PATH.as_posix()} {set_id} candidate {chunk_id} "
                    "must reference a retrieval chunk."
                )
            if parallel.get("relation") not in ALLOWED_PARALLEL_RELATIONS:
                failures.append(
                    f"{PARALLEL_CANDIDATES_PATH.as_posix()} {set_id} candidate relation must be allowed."
                )
            if parallel.get("confidence") not in ALLOWED_PARALLEL_CONFIDENCE:
                failures.append(
                    f"{PARALLEL_CANDIDATES_PATH.as_posix()} {set_id} candidate confidence must be review_candidate."
                )
            collation_status = parallel.get("collation_status")
            if collation_status not in ALLOWED_COLLATION_STATUSES:
                failures.append(
                    f"{PARALLEL_CANDIDATES_PATH.as_posix()} {set_id} candidate collation_status must be "
                    "pending_manual_collation or manual_theme_collation_recorded."
                )
            if collation_status == MANUAL_COLLATION_EVIDENCE_STATUS:
                required_terms = (set_id,)
                if _is_text(source_probe):
                    required_terms += (cast(str, source_probe),)
                if _is_text(anchor_probe):
                    required_terms += (cast(str, anchor_probe),)
                _validate_manual_collation_evidence(
                    root,
                    parallel.get("manual_collation_evidence"),
                    f"{set_id} candidate {anchor_probe}",
                    required_terms,
                    failures,
                )
            if not _is_text(parallel.get("rationale")):
                failures.append(
                    f"{PARALLEL_CANDIDATES_PATH.as_posix()} {set_id} "
                    "candidate rationale must be non-empty."
                )


def validate_collation_fixtures(
    root: Path,
    failures: list[str],
    warnings: list[str],
    strict_yaml: bool,
) -> None:
    probes = _load_anchor_probes(root, failures, warnings, strict_yaml)
    _validate_anchor_probe_locations(root, probes, failures)
    retrieval_chunk_ids = _load_retrieval_chunk_ids(root, failures, warnings, strict_yaml)
    _validate_parallel_candidates(
        root,
        {probe.probe_id for probe in probes},
        retrieval_chunk_ids,
        failures,
        warnings,
        strict_yaml,
    )
