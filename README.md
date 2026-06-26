# Gene-Disease Evidence Data

Public data distribution repository for the Gene-Disease Evidence Index.

The production pipeline is private. This repository is intended to contain only public
downloadable release artifacts, schemas, changelogs, and citation metadata.

## Current Status

`top120-public-preview-v0.1.3` is the current public aggregate release for the
Gene-Disease Evidence Index. It packages twelve disease-scoped 120-association
preview releases into one research-use distribution with public integrity
metadata, archive checksums, and release-gate summaries.

The aggregate contains 12 diseases, 1,440 candidate associations, 1,138 unique
genes, 1,505 evidence rows, 24 source snapshots, and 5,760 advisory review
artifacts. It passed the private paper-grade gate for public-preview release, but
it remains a research-use candidate association resource, not clinical evidence,
clinical guidance, or external peer-reviewed curation.

The `*-top120-v0.1.1-preview` directories are the current disease-scoped
components of the aggregate. Earlier releases such as
`top120-public-preview-v0.1.2`, `top120-public-preview-v0.1.1`,
`*-top120-v0.1.0-preview`, `v0.2.0`, `v0.1.1`, and `v0.1.0` remain available as
historical development/public-candidate artifacts.

## Public Resource

Rendered home: <https://serkan.ai/gene-disease-evidence/>

Current GitHub release:
<https://github.com/serkanaltuntas/gene-disease-evidence-data/releases/tag/top120-public-preview-v0.1.3>

Public reproducibility subset:
`docs/reproducibility/top120-public-preview-v0.1.3/`

The subset contains checksum instructions, public-only helper scripts, generated
table and figure snapshots, and a manifest for inspecting how manuscript-support
artifacts are bound to the fixed public release. It is not the full private
production pipeline.

## Package Layout

```text
schemas/
  association.schema.json
  release.schema.json
releases/
  top120-public-preview-v0.1.3/
    release.json
    batch-manifest.json
    integrity.json
    archives/
      gene-disease-evidence-top120-public-preview-v0.1.3.zip
  <disease>-top120-v0.1.1-preview/
    release.json
    genes.json
    diseases.json
    sources.json
    associations.json
    evidence_rows.jsonl
    review_artifacts.jsonl
archives/
  downloadable release bundles
docs/
  data-dictionary.md
  reproducibility/
    top120-public-preview-v0.1.3/
      README.md
      manifest.json
      scripts/
```

## Integrity

Each release directory contains an `integrity.json` sidecar manifest with SHA-256
checksums for the release files and its downloadable archive. The sidecar manifest is the
canonical integrity record; zip archives are deterministic downloadable bundles and do not
need to contain their own `integrity.json` file.

## Research-Use Boundary

These artifacts are research-use resources. They are not medical advice, diagnostic
guidance, treatment guidance, patient data, or clinical decision support.

## Citation

Use release-specific citation metadata and fixed archive checksums. The current
`top120-public-preview-v0.1.3` aggregate is public-preview research-use data with
paper-grade release gates passed in the private pipeline. It should still be
described as source-attributed candidate association data, not clinical evidence.
See `CITATION.cff`.

## License

The released data (`releases/` and the referenced `data/source_snapshots/`
payloads) is made available under **CC BY 4.0** — see `LICENSE` for the full
terms, attribution requirements, and per-source notices. CC BY 4.0 is the
binding floor because MONDO (used for disease identity) is CC BY 4.0; HGNC and
Open Targets are CC0, and ClinVar/NCBI is public data (attribution requested).
Redistribution is permitted with attribution and without implying endorsement.
`-dev` releases are development artifacts and must not be cited as scientific
evidence.
