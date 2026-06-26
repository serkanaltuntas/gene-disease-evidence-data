#!/usr/bin/env python3
"""Build or verify the public reproducibility subset manifest."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

RELEASE_ID = "top120-public-preview-v0.1.3"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def repo_root_from_script() -> Path:
    return Path(__file__).resolve().parents[4]


def subset_root_from_script() -> Path:
    return Path(__file__).resolve().parents[1]


def display_path(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix()


def file_entry(root: Path, path: Path, *, role: str) -> dict[str, Any]:
    return {
        "path": display_path(root, path),
        "role": role,
        "bytes": path.stat().st_size,
        "sha256": sha256_file(path),
    }


def external_anchor_entry(repo_root: Path, repo_relative_path: str, *, role: str) -> dict[str, Any]:
    path = repo_root / repo_relative_path
    return {
        "path": repo_relative_path,
        "role": role,
        "bytes": path.stat().st_size,
        "sha256": sha256_file(path),
    }


def infer_role(relative_path: str) -> str:
    if relative_path == "README.md":
        return "subset_readme"
    if relative_path.startswith("scripts/"):
        return "public_helper_script"
    if relative_path.startswith("docs/"):
        return "sanitized_reproducibility_note"
    if relative_path.startswith("tables/public-release/"):
        return "public_release_table_snapshot"
    if relative_path.startswith("tables/review-gate-snapshots/"):
        return "review_gate_table_snapshot"
    if relative_path.startswith("tables/manuscript-support/"):
        return "manuscript_support_table_snapshot"
    if relative_path.startswith("figures/inputs/"):
        return "figure_input_snapshot"
    if relative_path.startswith("figures/svg/"):
        return "figure_svg_or_visual_qa_snapshot"
    if relative_path.startswith("generated/"):
        return "generated_verification_output"
    return "subset_file"


def build_manifest(repo_root: Path, subset_root: Path) -> dict[str, Any]:
    subset_files = []
    for path in sorted(file for file in subset_root.rglob("*") if file.is_file()):
        relative_path = display_path(subset_root, path)
        if relative_path == "manifest.json" or relative_path.startswith("generated/"):
            continue
        subset_files.append(file_entry(subset_root, path, role=infer_role(relative_path)))

    release_anchor_paths = [
        ("CITATION.cff", "citation_metadata"),
        ("LICENSE", "repository_license"),
        ("README.md", "public_data_repository_readme"),
        ("docs/data-dictionary.md", "public_data_dictionary"),
        (f"releases/{RELEASE_ID}/release.json", "aggregate_release_metadata"),
        (f"releases/{RELEASE_ID}/batch-manifest.json", "aggregate_batch_manifest"),
        (f"releases/{RELEASE_ID}/integrity.json", "aggregate_integrity_manifest"),
        (
            f"archives/gene-disease-evidence-{RELEASE_ID}.zip",
            "downloadable_public_archive",
        ),
    ]
    release_anchors = [
        external_anchor_entry(repo_root, path, role=role)
        for path, role in release_anchor_paths
    ]
    return {
        "manifest_version": "public-reproducibility-subset-manifest-v1",
        "release_id": RELEASE_ID,
        "scope": (
            "Leak-audited public reproducibility subset for public-release "
            "table regeneration, figure/table snapshots, and checksum binding."
        ),
        "full_pipeline_public": False,
        "research_use_only": True,
        "subset_root": display_path(repo_root, subset_root),
        "release_anchors": release_anchors,
        "files": subset_files,
    }


def write_manifest(path: Path, manifest: dict[str, Any]) -> None:
    path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build reproducibility subset manifest.")
    parser.add_argument("--repo-root", type=Path, default=repo_root_from_script())
    parser.add_argument("--subset-root", type=Path, default=subset_root_from_script())
    parser.add_argument("--output", type=Path, default=subset_root_from_script() / "manifest.json")
    parser.add_argument("--check", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    repo_root = args.repo_root.resolve()
    subset_root = args.subset_root.resolve()
    output = args.output.resolve()
    manifest = build_manifest(repo_root, subset_root)
    if args.check:
        existing = json.loads(output.read_text(encoding="utf-8"))
        status = "ok" if existing == manifest else "mismatch"
        print(json.dumps({"status": status, "output": display_path(repo_root, output)}, indent=2))
        return 0 if status == "ok" else 1
    write_manifest(output, manifest)
    print(
        json.dumps(
            {
                "status": "ok",
                "output": display_path(repo_root, output),
                "file_count": len(manifest["files"]),
                "release_anchor_count": len(manifest["release_anchors"]),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
