#!/usr/bin/env python3
"""Rebuild public-only manuscript support tables from public release artifacts."""

from __future__ import annotations

import argparse
import csv
import filecmp
import hashlib
import json
import zipfile
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

RELEASE_ID = "top120-public-preview-v0.1.3"
SOURCE_IDS = ("source:clinvar", "source:opentargets")


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def compact_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def write_tsv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys()) if rows else []
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=fieldnames,
            delimiter="\t",
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)


def repo_root_from_script() -> Path:
    return Path(__file__).resolve().parents[4]


def subset_root_from_script() -> Path:
    return Path(__file__).resolve().parents[1]


def build_tables(repo_root: Path, release_id: str) -> dict[str, list[dict[str, Any]]]:
    release_dir = repo_root / "releases" / release_id
    batch_manifest = read_json(release_dir / "batch-manifest.json")
    integrity = read_json(release_dir / "integrity.json")
    archive_path = repo_root / integrity["archives"][0]["path"]
    release_rows = batch_manifest["releases"]

    return {
        "dataset_overview": dataset_overview_rows(batch_manifest, integrity),
        "disease_counts": disease_count_rows(batch_manifest),
        "source_coverage": source_coverage_rows(repo_root, release_rows),
        "disease_source_coverage": disease_source_coverage_rows(repo_root, release_rows),
        "support_states": support_state_rows(repo_root, release_rows),
        "source_freshness": source_freshness_rows(repo_root, release_rows),
        "open_targets_datatype_channels": open_targets_channel_rows(archive_path, "datatype"),
        "open_targets_datasource_channels": open_targets_channel_rows(archive_path, "datasource"),
    }


def dataset_overview_rows(
    batch_manifest: dict[str, Any],
    integrity: dict[str, Any],
) -> list[dict[str, Any]]:
    totals = batch_manifest["totals"]
    archive = integrity["archives"][0]
    return [
        {
            "metric": "release_id",
            "value": batch_manifest["manifest_id"],
            "source": "batch-manifest",
        },
        {"metric": "diseases", "value": totals["disease_count"], "source": "batch-manifest"},
        {"metric": "associations", "value": totals["associations"], "source": "batch-manifest"},
        {"metric": "gene_rows", "value": totals["gene_rows"], "source": "batch-manifest"},
        {"metric": "unique_genes", "value": totals["unique_genes"], "source": "batch-manifest"},
        {"metric": "evidence_rows", "value": totals["evidence_rows"], "source": "batch-manifest"},
        {
            "metric": "source_snapshots",
            "value": totals["source_snapshots"],
            "source": "batch-manifest",
        },
        {
            "metric": "review_artifacts",
            "value": totals["review_artifacts"],
            "source": "batch-manifest",
        },
        {"metric": "archive_path", "value": archive["path"], "source": "integrity"},
        {"metric": "archive_sha256", "value": archive["sha256"], "source": "integrity"},
        {"metric": "archive_bytes", "value": archive["bytes"], "source": "integrity"},
    ]


def disease_count_rows(batch_manifest: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "disease_label": release["disease_label"],
            "disease_id": release["disease_id"],
            "release_id": release["release_id"],
            "release_status": release["release_status"],
            "gene_count": release["gene_count"],
            "association_count": release["association_count"],
            "evidence_row_count": release["evidence_row_count"],
            "source_snapshot_count": release["source_snapshot_count"],
        }
        for release in batch_manifest["releases"]
    ]


def load_release_records(
    repo_root: Path,
    release: dict[str, Any],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    release_dir = repo_root / release["release_dir"]
    return (
        read_json(release_dir / "associations.json"),
        read_jsonl(release_dir / "evidence_rows.jsonl"),
        read_json(release_dir / "sources.json"),
        read_json(release_dir / "source_snapshots.json"),
    )


def disease_source_coverage_rows(
    repo_root: Path,
    release_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rows = []
    for release in release_rows:
        associations, evidence_rows, _, _ = load_release_records(repo_root, release)
        source_counts = association_source_counts(associations)
        support_counts = support_state_counts(associations)
        rows.append(
            {
                "disease_label": release["disease_label"],
                "disease_id": release["disease_id"],
                "association_count": len(associations),
                "evidence_row_count": len(evidence_rows),
                "clinvar_supporting": source_counts["supporting"]["source:clinvar"],
                "clinvar_silent": source_counts["silent"]["source:clinvar"],
                "clinvar_conflicting": source_counts["conflicting"]["source:clinvar"],
                "opentargets_supporting": source_counts["supporting"]["source:opentargets"],
                "opentargets_silent": source_counts["silent"]["source:opentargets"],
                "opentargets_conflicting": source_counts["conflicting"]["source:opentargets"],
                "multi_source_support": support_counts["multi_source_support"],
                "single_source_support_with_source_silence": support_counts[
                    "single_source_support_with_source_silence"
                ],
            }
        )
    return rows


def source_coverage_rows(
    repo_root: Path,
    release_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    totals = {
        source_id: {"supporting": 0, "silent": 0, "conflicting": 0}
        for source_id in SOURCE_IDS
    }
    for release in release_rows:
        associations, _, _, _ = load_release_records(repo_root, release)
        source_counts = association_source_counts(associations)
        for state in ("supporting", "silent", "conflicting"):
            for source_id in SOURCE_IDS:
                totals[source_id][state] += source_counts[state][source_id]
    return [
        {
            "source_id": source_id,
            "supporting_associations": totals[source_id]["supporting"],
            "silent_associations": totals[source_id]["silent"],
            "conflicting_associations": totals[source_id]["conflicting"],
        }
        for source_id in sorted(totals)
    ]


def association_source_counts(
    associations: list[dict[str, Any]],
) -> dict[str, Counter[str]]:
    source_counts = {
        "supporting": Counter(),
        "silent": Counter(),
        "conflicting": Counter(),
    }
    for association in associations:
        coverage = association.get("source_coverage", {})
        source_counts["supporting"].update(coverage.get("supporting_source_ids", []))
        source_counts["silent"].update(coverage.get("silent_source_ids", []))
        source_counts["conflicting"].update(coverage.get("conflicting_source_ids", []))
    return source_counts


def support_state_rows(
    repo_root: Path,
    release_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    totals = Counter()
    conflicting_association_count = 0
    for release in release_rows:
        associations, _, _, _ = load_release_records(repo_root, release)
        counts = support_state_counts(associations)
        totals.update(counts)
        conflicting_association_count += counts["conflicting_association_count"]
    rows = [
        {
            "support_state": "multi_source_support",
            "association_count": totals["multi_source_support"],
        },
        {
            "support_state": "single_source_support_with_source_silence",
            "association_count": totals["single_source_support_with_source_silence"],
        },
        {
            "support_state": "conflicting_association_count",
            "association_count": conflicting_association_count,
        },
    ]
    return rows


def support_state_counts(associations: list[dict[str, Any]]) -> Counter:
    counts: Counter[str] = Counter()
    for association in associations:
        coverage = association.get("source_coverage", {})
        supporting = coverage.get("supporting_source_ids", [])
        silent = coverage.get("silent_source_ids", [])
        conflicting = coverage.get("conflicting_source_ids", [])
        if conflicting:
            counts["conflicting_association_count"] += 1
        elif len(supporting) > 1:
            counts["multi_source_support"] += 1
        elif supporting and silent:
            counts["single_source_support_with_source_silence"] += 1
    return counts


def source_freshness_rows(
    repo_root: Path,
    release_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    summaries: dict[str, dict[str, Any]] = {}
    for release in release_rows:
        _, _, sources, snapshots = load_release_records(repo_root, release)
        disease_id = release["disease_id"]
        for source in sources:
            source_id = source["id"]
            summary = source_summary(summaries, source_id)
            summary["disease_ids"].add(disease_id)
            summary["source_record_count"] += 1
            summary["roles"][source_role(source_id)] += 1
            add_freshness(summary, source.get("freshness"), source.get("accessed_at"))
        for snapshot in snapshots:
            for source_id in snapshot.get("source_ids", []):
                summary = source_summary(summaries, source_id)
                summary["disease_ids"].add(disease_id)
                summary["snapshot_count"] += 1
                summary["snapshot_record_count"] += int(snapshot.get("record_count") or 0)
                summary["roles"]["evidence_snapshot"] += 1
                add_freshness(summary, snapshot.get("freshness"), snapshot.get("accessed_at"))

    rows = []
    for source_id in sorted(summaries):
        summary = summaries[source_id]
        rows.append(
            {
                "source_id": source_id,
                "roles": compact_json(dict(sorted(summary["roles"].items()))),
                "disease_count": len(summary["disease_ids"]),
                "source_record_count": summary["source_record_count"],
                "snapshot_count": summary["snapshot_count"],
                "snapshot_record_count": summary["snapshot_record_count"],
                "freshness_status_counts": compact_json(
                    dict(sorted(summary["freshness_status_counts"].items()))
                ),
                "accessed_at_values": ";".join(sorted(summary["accessed_at_values"])),
                "next_review_due_values": ";".join(sorted(summary["next_review_due_values"])),
                "missing_freshness_count": summary["missing_freshness_count"],
                "paper_grade_blocker_count": summary["paper_grade_blocker_count"],
            }
        )
    return rows


def source_summary(summaries: dict[str, dict[str, Any]], source_id: str) -> dict[str, Any]:
    if source_id not in summaries:
        summaries[source_id] = {
            "disease_ids": set(),
            "source_record_count": 0,
            "snapshot_count": 0,
            "snapshot_record_count": 0,
            "roles": Counter(),
            "freshness_status_counts": Counter(),
            "accessed_at_values": set(),
            "next_review_due_values": set(),
            "missing_freshness_count": 0,
            "paper_grade_blocker_count": 0,
        }
    return summaries[source_id]


def source_role(source_id: str) -> str:
    return {
        "source:clinvar": "evidence",
        "source:opentargets": "evidence",
        "source:hgnc": "gene_identity",
        "source:mondo": "disease_identity",
        "source:efo": "ontology_crosswalk_context",
    }.get(source_id, "context")


def add_freshness(
    summary: dict[str, Any],
    freshness: dict[str, Any] | None,
    accessed_at: str | None,
) -> None:
    if accessed_at:
        summary["accessed_at_values"].add(accessed_at)
    if not freshness:
        summary["missing_freshness_count"] += 1
        return
    status = freshness.get("status")
    if status:
        summary["freshness_status_counts"][status] += 1
    next_review_due = freshness.get("next_review_due")
    if next_review_due:
        summary["next_review_due_values"].add(next_review_due)
    if freshness.get("paper_grade_blocker"):
        summary["paper_grade_blocker_count"] += 1


def open_targets_channel_rows(archive_path: Path, channel_kind: str) -> list[dict[str, Any]]:
    summaries: dict[str, dict[str, Any]] = defaultdict(new_channel_summary)
    total_open_targets_rows = 0
    missing_score_rows = 0
    score_key = f"open_targets_{channel_kind}_scores"

    with zipfile.ZipFile(archive_path) as archive:
        names = sorted(
            name
            for name in archive.namelist()
            if name.startswith("releases/") and name.endswith("/evidence_rows.jsonl")
        )
        for name in names:
            release_id = name.split("/")[1]
            for raw_line in archive.read(name).decode("utf-8").splitlines():
                if not raw_line.strip():
                    continue
                row = json.loads(raw_line)
                if row.get("source_id") != "source:opentargets":
                    continue
                total_open_targets_rows += 1
                score_rows = (row.get("source_metrics") or {}).get(score_key) or []
                if not score_rows:
                    missing_score_rows += 1
                add_channel_scores(summaries, score_rows, row=row, release_id=release_id)

    rows = []
    for channel_id, summary in summaries.items():
        rows.append(
            {
                "channel_id": channel_id,
                "association_count": len(summary["association_ids"]),
                "evidence_row_count": len(summary["evidence_row_ids"]),
                "disease_release_count": len(summary["release_ids"]),
                "total_open_targets_evidence_rows": total_open_targets_rows,
                "missing_channel_score_rows": missing_score_rows,
            }
        )
    return sorted(rows, key=lambda row: (-row["association_count"], row["channel_id"]))


def new_channel_summary() -> dict[str, Any]:
    return {
        "association_ids": set(),
        "evidence_row_ids": set(),
        "release_ids": set(),
    }


def add_channel_scores(
    summaries: dict[str, dict[str, Any]],
    score_rows: list[dict[str, Any]],
    *,
    row: dict[str, Any],
    release_id: str,
) -> None:
    association_id = row.get("association_id")
    evidence_row_id = row.get("id")
    for score_row in score_rows:
        channel_id = score_row.get("id")
        score = score_row.get("score")
        if not channel_id or not isinstance(score, (int, float)) or score <= 0:
            continue
        summary = summaries[channel_id]
        if association_id:
            summary["association_ids"].add(association_id)
        if evidence_row_id:
            summary["evidence_row_ids"].add(evidence_row_id)
        summary["release_ids"].add(release_id)


def write_tables(output_dir: Path, tables: dict[str, list[dict[str, Any]]]) -> None:
    for table_id, rows in tables.items():
        write_tsv(output_dir / f"{table_id}.tsv", rows)


def compare_outputs(output_dir: Path, expected_dir: Path) -> list[dict[str, str]]:
    mismatches = []
    for generated in sorted(output_dir.glob("*.tsv")):
        expected = expected_dir / generated.name
        if not expected.exists():
            mismatches.append({"file": generated.name, "reason": "missing_expected"})
        elif not filecmp.cmp(generated, expected, shallow=False):
            mismatches.append(
                {
                    "file": generated.name,
                    "reason": "content_mismatch",
                    "generated_sha256": sha256_file(generated),
                    "expected_sha256": sha256_file(expected),
                }
            )
    return mismatches


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Rebuild public-only methods tables from the public data release."
    )
    parser.add_argument("--repo-root", type=Path, default=repo_root_from_script())
    parser.add_argument("--release-id", default=RELEASE_ID)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=subset_root_from_script() / "generated" / "public-release",
    )
    parser.add_argument(
        "--expected-dir",
        type=Path,
        default=subset_root_from_script() / "tables" / "public-release",
    )
    parser.add_argument("--no-compare", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    repo_root = args.repo_root.resolve()
    output_dir = args.output_dir.resolve()
    tables = build_tables(repo_root, args.release_id)
    write_tables(output_dir, tables)
    mismatches = [] if args.no_compare else compare_outputs(output_dir, args.expected_dir)
    print(
        json.dumps(
            {
                "status": "ok" if not mismatches else "mismatch",
                "release_id": args.release_id,
                "output_dir": output_dir.relative_to(repo_root).as_posix()
                if output_dir.is_relative_to(repo_root)
                else output_dir.as_posix(),
                "table_count": len(tables),
                "mismatches": mismatches,
            },
            indent=2,
        )
    )
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
