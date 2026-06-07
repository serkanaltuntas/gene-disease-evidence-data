# Gene-Disease Evidence Data

Public data distribution repository for the Gene-Disease Evidence Index.

The production pipeline is private. This repository is intended to contain only public
downloadable release artifacts, schemas, changelogs, and citation metadata.

## Current Status

`v0.0.1-dev` is a development fixture for validating the release package shape. It is
not a public scientific release and should not be cited as evidence.

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
  v0.0.1-dev/
    release.json
    genes.json
    diseases.json
    sources.json
    associations.json
    evidence_rows.jsonl
    review_artifacts.jsonl
archives/
  downloadable release bundles
```

## Research-Use Boundary

These artifacts are research-use resources. They are not medical advice, diagnostic
guidance, treatment guidance, patient data, or clinical decision support.

## Citation

Use the release-specific citation metadata once a paper-grade release is available.
The development fixture should not be cited as scientific evidence.

