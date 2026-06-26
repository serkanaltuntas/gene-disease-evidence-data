#!/usr/bin/env python3
"""Rebuild figure-input JSON snapshots from public subset tables."""

from __future__ import annotations

import argparse
import csv
import filecmp
import json
from pathlib import Path
from typing import Any


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=False) + "\n", encoding="utf-8")


def subset_root_from_script() -> Path:
    return Path(__file__).resolve().parents[1]


def build_figure_inputs(table_root: Path, review_table_root: Path) -> dict[str, dict[str, Any]]:
    dataset_overview = read_tsv(table_root / "dataset_overview.tsv")
    disease_counts = read_tsv(table_root / "disease_counts.tsv")
    disease_source_coverage = read_tsv(table_root / "disease_source_coverage.tsv")
    source_coverage = read_tsv(table_root / "source_coverage.tsv")
    review_gates = read_tsv(review_table_root / "review_gates.tsv")
    overview = {row["metric"]: row["value"] for row in dataset_overview}
    return {
        "pipeline_overview": pipeline_overview_payload(
            overview=overview,
            disease_counts=disease_counts,
            review_gates=review_gates,
        ),
        "source_support_silence": source_support_silence_payload(
            source_coverage=source_coverage,
            disease_source_coverage=disease_source_coverage,
        ),
        "render_raw_traceability": render_raw_traceability_payload(
            overview=overview,
            disease_counts=disease_counts,
        ),
    }


def pipeline_overview_payload(
    *,
    overview: dict[str, str],
    disease_counts: list[dict[str, str]],
    review_gates: list[dict[str, str]],
) -> dict[str, Any]:
    gate_nodes = [
        {
            "id": f"gate:{row['gate']}",
            "label": row["gate"].replace("_", " "),
            "kind": "review_gate",
            "result": row["result"],
            "details": row["details"],
        }
        for row in review_gates
    ]
    disease_release_nodes = [
        {
            "id": f"release:{row['release_id']}",
            "label": row["disease_label"],
            "kind": "disease_release",
            "association_count": int(row["association_count"]),
            "evidence_row_count": int(row["evidence_row_count"]),
        }
        for row in disease_counts
    ]
    nodes = [
        {"id": "source:opentargets", "label": "OpenTargets", "kind": "source"},
        {"id": "source:clinvar", "label": "ClinVar", "kind": "source"},
        {
            "id": "stage:snapshot_materialization",
            "label": "Source snapshot materialization",
            "kind": "pipeline_stage",
            "source_snapshot_count": int(overview["source_snapshots"]),
        },
        {
            "id": "stage:release_generation",
            "label": "Disease-scoped release generation",
            "kind": "pipeline_stage",
            "disease_count": int(overview["diseases"]),
            "association_count": int(overview["associations"]),
        },
        *disease_release_nodes,
        *gate_nodes,
        {
            "id": f"aggregate:{overview['release_id']}",
            "label": overview["release_id"],
            "kind": "public_aggregate",
            "unique_genes": int(overview["unique_genes"]),
            "evidence_rows": int(overview["evidence_rows"]),
        },
        {
            "id": "surface:serkan_ai",
            "label": "Rendered serkan.ai resource",
            "kind": "rendered_surface",
        },
    ]
    edges = [
        {"source": "source:opentargets", "target": "stage:snapshot_materialization"},
        {"source": "source:clinvar", "target": "stage:snapshot_materialization"},
        {"source": "stage:snapshot_materialization", "target": "stage:release_generation"},
    ]
    edges.extend(
        {"source": "stage:release_generation", "target": f"release:{row['release_id']}"}
        for row in disease_counts
    )
    edges.extend(
        {
            "source": f"release:{row['release_id']}",
            "target": "gate:source_silence_disagreement",
        }
        for row in disease_counts
    )
    edges.extend(
        {"source": f"gate:{row['gate']}", "target": f"aggregate:{overview['release_id']}"}
        for row in review_gates
    )
    edges.append(
        {"source": f"aggregate:{overview['release_id']}", "target": "surface:serkan_ai"}
    )
    return {
        "figure_id": "pipeline_overview",
        "title": "Release pipeline and review gates",
        "nodes": nodes,
        "edges": edges,
    }


def source_support_silence_payload(
    *,
    source_coverage: list[dict[str, str]],
    disease_source_coverage: list[dict[str, str]],
) -> dict[str, Any]:
    return {
        "figure_id": "source_support_silence",
        "title": "Included-source support and source silence",
        "source_totals": [
            {
                "source_id": row["source_id"],
                "supporting_associations": int(row["supporting_associations"]),
                "silent_associations": int(row["silent_associations"]),
                "conflicting_associations": int(row["conflicting_associations"]),
            }
            for row in source_coverage
        ],
        "per_disease": [
            {
                "disease_label": row["disease_label"],
                "disease_id": row["disease_id"],
                "association_count": int(row["association_count"]),
                "clinvar_supporting": int(row["clinvar_supporting"]),
                "clinvar_silent": int(row["clinvar_silent"]),
                "opentargets_supporting": int(row["opentargets_supporting"]),
                "multi_source_support": int(row["multi_source_support"]),
                "single_source_support_with_source_silence": int(
                    row["single_source_support_with_source_silence"]
                ),
            }
            for row in disease_source_coverage
        ],
        "caveat": (
            "Source silence is scoped to included sources and release candidates; "
            "it is not evidence of biological or clinical absence."
        ),
    }


def render_raw_traceability_payload(
    *,
    overview: dict[str, str],
    disease_counts: list[dict[str, str]],
) -> dict[str, Any]:
    release_id = overview["release_id"]
    return {
        "figure_id": "render_raw_traceability",
        "title": "Rendered page to raw artifact traceability",
        "release_id": release_id,
        "rendered_routes": [
            "/gene-disease-evidence/",
            "/gene-disease-evidence/methods/",
            "/gene-disease-evidence/gene/<HGNC symbol>/",
        ],
        "raw_artifacts": [
            {
                "kind": "aggregate_release",
                "path": f"releases/{release_id}/release.json",
            },
            {
                "kind": "aggregate_manifest",
                "path": f"releases/{release_id}/batch-manifest.json",
            },
            {
                "kind": "aggregate_integrity",
                "path": f"releases/{release_id}/integrity.json",
            },
            {
                "kind": "aggregate_archive",
                "path": overview["archive_path"],
                "sha256": overview["archive_sha256"],
            },
        ],
        "disease_release_dirs": [
            {
                "disease_label": row["disease_label"],
                "release_id": row["release_id"],
                "release_dir": f"releases/{row['release_id']}",
            }
            for row in disease_counts
        ],
        "table_manifest": {
            "path": "docs/methods/tables/manifest.json",
            "input_count": 9,
            "output_count": 10,
        },
    }


def write_outputs(output_dir: Path, payloads: dict[str, dict[str, Any]]) -> None:
    for figure_id, payload in payloads.items():
        write_json(output_dir / f"{figure_id}.json", payload)


def compare_outputs(output_dir: Path, expected_dir: Path) -> list[dict[str, str]]:
    mismatches = []
    for output in sorted(output_dir.glob("*.json")):
        expected = expected_dir / output.name
        if not expected.exists():
            mismatches.append({"file": output.name, "reason": "missing_expected"})
        elif not filecmp.cmp(output, expected, shallow=False):
            mismatches.append({"file": output.name, "reason": "content_mismatch"})
    return mismatches


def build_parser() -> argparse.ArgumentParser:
    subset_root = subset_root_from_script()
    parser = argparse.ArgumentParser(description="Rebuild figure-input JSON snapshots.")
    parser.add_argument(
        "--table-dir",
        type=Path,
        default=subset_root / "tables" / "public-release",
    )
    parser.add_argument(
        "--review-table-dir",
        type=Path,
        default=subset_root / "tables" / "review-gate-snapshots",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=subset_root / "generated" / "figure-inputs",
    )
    parser.add_argument(
        "--expected-dir",
        type=Path,
        default=subset_root / "figures" / "inputs",
    )
    parser.add_argument("--no-compare", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    payloads = build_figure_inputs(args.table_dir.resolve(), args.review_table_dir.resolve())
    output_dir = args.output_dir.resolve()
    write_outputs(output_dir, payloads)
    mismatches = [] if args.no_compare else compare_outputs(output_dir, args.expected_dir)
    print(
        json.dumps(
            {
                "status": "ok" if not mismatches else "mismatch",
                "output_dir": output_dir.as_posix(),
                "figure_input_count": len(payloads),
                "mismatches": mismatches,
            },
            indent=2,
        )
    )
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
