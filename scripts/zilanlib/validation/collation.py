from __future__ import annotations

import re
from pathlib import Path
from typing import cast

from zilanlib.agama.collation_preflight import AnchorProbe, build_anchor_report
from zilanlib.yaml_io import load_yaml_for_validation

COLLATION_FIXTURE_DIR = Path("tests/fixtures/collation")
ANCHOR_PROBES_PATH = COLLATION_FIXTURE_DIR / "cbeta_anchor_probes.yaml"
PARALLEL_CANDIDATES_PATH = COLLATION_FIXTURE_DIR / "high_value_no_self_parallel_candidates.yaml"
RETRIEVAL_CHUNKS_PATH = "tests/fixtures/retrieval_chunks/semantic_chunks.yaml"
ALLOWED_PARALLEL_RELATIONS = ("doctrinal_theme_parallel", "possible_textual_parallel")
ALLOWED_CANDIDATE_SET_STATUSES = ("candidate_map_only", "manual_collation_reviewed")
ALLOWED_PARALLEL_CONFIDENCE = ("review_candidate", "manual_limited_theme_parallel")
ALLOWED_COLLATION_STATUSES = ("pending_manual_collation", "manual_xml_p5_theme_parallel_reviewed")
ALLOWED_MANUAL_REVIEW_CONCLUSIONS = ("limited_doctrinal_theme_parallel",)


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


def _repo_relative_existing_path(root: Path, value: object) -> str | None:
    if not _is_text(value):
        return None
    rel_path = cast(str, value).replace("\\", "/")
    if Path(rel_path).is_absolute() or "<" in rel_path or ">" in rel_path:
        return None
    path = root / rel_path
    try:
        path.resolve().relative_to(root.resolve())
    except ValueError:
        return None
    return rel_path if path.is_file() else None


def _validate_manual_review(root: Path, set_id: str, manual_review: object, failures: list[str]) -> None:
    if not isinstance(manual_review, dict):
        failures.append(f"{PARALLEL_CANDIDATES_PATH.as_posix()} {set_id} manual_review must be a mapping.")
        return

    date = manual_review.get("date")
    if not _is_text(date) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", cast(str, date)):
        failures.append(f"{PARALLEL_CANDIDATES_PATH.as_posix()} {set_id} manual_review.date must use YYYY-MM-DD.")
    if manual_review.get("conclusion") not in ALLOWED_MANUAL_REVIEW_CONCLUSIONS:
        failures.append(
            f"{PARALLEL_CANDIDATES_PATH.as_posix()} {set_id} manual_review.conclusion must be "
            "limited_doctrinal_theme_parallel."
        )
    if not _is_text(manual_review.get("reviewer")):
        failures.append(f"{PARALLEL_CANDIDATES_PATH.as_posix()} {set_id} manual_review.reviewer must be non-empty.")
    if _repo_relative_existing_path(root, manual_review.get("evidence_file")) is None:
        failures.append(
            f"{PARALLEL_CANDIDATES_PATH.as_posix()} {set_id} manual_review.evidence_file must exist."
        )


def _manual_review_evidence_text(root: Path, manual_review: object) -> str | None:
    if not isinstance(manual_review, dict):
        return None
    evidence_path = _repo_relative_existing_path(root, manual_review.get("evidence_file"))
    if evidence_path is None:
        return None
    return (root / evidence_path).read_text(encoding="utf-8")


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

        set_status = candidate_set.get("status")
        if set_status not in ALLOWED_CANDIDATE_SET_STATUSES:
            failures.append(
                f"{PARALLEL_CANDIDATES_PATH.as_posix()} {set_id} status must be one of "
                f"{', '.join(ALLOWED_CANDIDATE_SET_STATUSES)}."
            )
        if set_status == "manual_collation_reviewed":
            _validate_manual_review(root, set_id, candidate_set.get("manual_review"), failures)
        elif "manual_review" in candidate_set:
            failures.append(
                f"{PARALLEL_CANDIDATES_PATH.as_posix()} {set_id} manual_review requires manual_collation_reviewed."
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
        evidence_text = (
            _manual_review_evidence_text(root, candidate_set.get("manual_review"))
            if set_status == "manual_collation_reviewed"
            else None
        )
        if evidence_text is not None and (
            not isinstance(source_probe, str)
            or not isinstance(source_chunk_id, str)
            or source_probe not in evidence_text
            or source_chunk_id not in evidence_text
        ):
            failures.append(
                f"{PARALLEL_CANDIDATES_PATH.as_posix()} {set_id} manual_review.evidence_file must identify "
                "the source anchor and chunk."
            )

        boundaries = candidate_set.get("boundaries")
        boundary_texts = [item for item in boundaries if isinstance(item, str)] if isinstance(boundaries, list) else []
        if not any("does not prove publication-level equivalence" in item for item in boundary_texts):
            failures.append(
                f"{PARALLEL_CANDIDATES_PATH.as_posix()} {set_id} boundaries must preserve the non-equivalence boundary."
            )
        if set_status == "manual_collation_reviewed":
            for required_boundary in (
                "does not prove textual equivalence",
                "does not change runtime or platform validation status",
            ):
                if not any(required_boundary in item for item in boundary_texts):
                    failures.append(
                        f"{PARALLEL_CANDIDATES_PATH.as_posix()} {set_id} boundaries must preserve: "
                        f"{required_boundary}."
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
            confidence = parallel.get("confidence")
            if confidence not in ALLOWED_PARALLEL_CONFIDENCE:
                failures.append(
                    f"{PARALLEL_CANDIDATES_PATH.as_posix()} {set_id} candidate confidence must be allowed."
                )
            collation_status = parallel.get("collation_status")
            if collation_status == "anchor_located_collation_pending":
                failures.append(
                    f"{PARALLEL_CANDIDATES_PATH.as_posix()} {set_id} candidate "
                    "anchor-located status cannot be used as manual collation."
                )
            elif collation_status not in ALLOWED_COLLATION_STATUSES:
                failures.append(
                    f"{PARALLEL_CANDIDATES_PATH.as_posix()} {set_id} candidate collation_status must be "
                    "allowed."
                )
            if not _is_text(parallel.get("rationale")):
                failures.append(
                    f"{PARALLEL_CANDIDATES_PATH.as_posix()} {set_id} "
                    "candidate rationale must be non-empty."
                )
            if set_status == "candidate_map_only":
                if confidence != "review_candidate":
                    failures.append(
                        f"{PARALLEL_CANDIDATES_PATH.as_posix()} {set_id} "
                        "candidate_map_only confidence must be review_candidate."
                    )
                if collation_status != "pending_manual_collation":
                    failures.append(
                        f"{PARALLEL_CANDIDATES_PATH.as_posix()} {set_id} "
                        "candidate_map_only collation_status must be pending_manual_collation."
                    )
            if set_status == "manual_collation_reviewed":
                if confidence != "manual_limited_theme_parallel":
                    failures.append(
                        f"{PARALLEL_CANDIDATES_PATH.as_posix()} {set_id} "
                        "manual reviewed candidate confidence must be manual_limited_theme_parallel."
                    )
                if collation_status != "manual_xml_p5_theme_parallel_reviewed":
                    failures.append(
                        f"{PARALLEL_CANDIDATES_PATH.as_posix()} {set_id} "
                        "manual reviewed candidate collation_status must be "
                        "manual_xml_p5_theme_parallel_reviewed."
                    )
                if parallel.get("equivalence_claim") is not False:
                    failures.append(
                        f"{PARALLEL_CANDIDATES_PATH.as_posix()} {set_id} "
                        "manual reviewed candidate equivalence_claim must be false."
                    )
                if parallel.get("source_dependence_claim") is not False:
                    failures.append(
                        f"{PARALLEL_CANDIDATES_PATH.as_posix()} {set_id} "
                        "manual reviewed candidate source_dependence_claim must be false."
                    )
                if parallel.get("publication_ready") is not False:
                    failures.append(
                        f"{PARALLEL_CANDIDATES_PATH.as_posix()} {set_id} "
                        "manual reviewed candidate publication_ready must be false."
                    )
                if not _is_text(parallel.get("qualified_conclusion")):
                    failures.append(
                        f"{PARALLEL_CANDIDATES_PATH.as_posix()} {set_id} "
                        "manual reviewed candidate qualified_conclusion must be non-empty."
                    )
                if evidence_text is not None and (
                    not isinstance(anchor_probe, str)
                    or not isinstance(chunk_id, str)
                    or anchor_probe not in evidence_text
                    or chunk_id not in evidence_text
                ):
                    failures.append(
                        f"{PARALLEL_CANDIDATES_PATH.as_posix()} {set_id} manual_review.evidence_file must identify "
                        "every candidate anchor and chunk."
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
