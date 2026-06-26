# Reproducibility and data availability note

Release: `top120-public-preview-v0.1.3`

This note describes the public reproducibility subset bundled in this repository.
It is scoped to already-public release artifacts and manuscript-supporting
snapshots. It does not publish the private production pipeline.

## Fixed public release

| Field | Value |
| --- | --- |
| Release id | `top120-public-preview-v0.1.3` |
| Public data repository | `github.com/serkanaltuntas/gene-disease-evidence-data` |
| Public resource | `https://serkan.ai/gene-disease-evidence/` |
| GitHub Release | `https://github.com/serkanaltuntas/gene-disease-evidence-data/releases/tag/top120-public-preview-v0.1.3` |
| Archive path | `archives/gene-disease-evidence-top120-public-preview-v0.1.3.zip` |
| Archive SHA-256 | `5e7d379a16ba8d862fca49129d7e3c640735387914df40d33ad0bcad4edea33b` |

## Release scale

| Measure | Count |
| --- | ---: |
| Disease-scoped releases | 12 |
| Candidate associations | 1,440 |
| Unique HGNC genes | 1,138 |
| Evidence rows | 1,505 |
| Source snapshots | 24 |
| Advisory review artifacts | 5,760 |

## Public verification commands

Run from the public data repository root.

Verify the archive checksum:

```bash
shasum -a 256 archives/gene-disease-evidence-top120-public-preview-v0.1.3.zip
```

Rebuild public-only methods tables and compare them with the subset snapshots:

```bash
python3 docs/reproducibility/top120-public-preview-v0.1.3/scripts/rebuild_public_methods.py
```

Verify the subset manifest:

```bash
python3 docs/reproducibility/top120-public-preview-v0.1.3/scripts/build_subset_manifest.py --check
```

## Code boundary

The public helper logic rebuilds only tables that can be derived from public
release files. Review-gate snapshots and the manuscript candidate contract table
are included for manuscript-support transparency, but they are not claimed to be
rebuildable from the public release alone.

## Use boundary

The release is research-use only. It contains source-attributed candidate
association records and review artifacts for validation and provenance
assessment. It is not diagnostic, therapeutic, clinical decision support,
patient risk prediction, clinical validity, or clinical utility material.
