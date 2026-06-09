# Gene-Disease Evidence Data

Public data distribution repository for the Gene-Disease Evidence Index.

The production pipeline is private. This repository is intended to contain only public
downloadable release artifacts, schemas, changelogs, and citation metadata.

## Current Status

`v0.1.0` is the first Alzheimer disease public-candidate research-use export. It
is intended to validate the public data package, integrity manifest, and rendered
resource sync before a paper-grade snapshot. It should not be cited as a
manuscript-grade biomedical dataset.

## Public Resource

Planned rendered home:

```text
https://serkan.ai/gene-disease-evidence/
```

## Package Layout

```text
schemas/
  association.schema.json
  release.schema.json
releases/
  v0.1.0/
    release.json
    genes.json
    diseases.json
    sources.json
    associations.json
    evidence_rows.jsonl
    review_artifacts.jsonl
    integrity.json
archives/
  downloadable release bundles
```

## Research-Use Boundary

These artifacts are research-use resources. They are not medical advice, diagnostic
guidance, treatment guidance, patient data, or clinical decision support.

## Citation

Use release-specific citation metadata and fixed archive checksums. The current
`v0.1.0` export is public-candidate research-use data, not manuscript-grade
evidence.
