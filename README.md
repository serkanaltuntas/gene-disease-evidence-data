# Gene-Disease Evidence Data

Public data distribution repository for the Gene-Disease Evidence Index.

The production pipeline is private. This repository is intended to contain only public
downloadable release artifacts, schemas, changelogs, and citation metadata.

## Current Status

The `*-top120-v0.1.0-preview` releases are a 12-disease public preview batch for
research-use inspection of the package shape, provenance, source boundaries, and
review-gated evidence records. They are `draft` releases, not manuscript-grade
biomedical evidence.

`v0.2.0` is the current Alzheimer disease public-candidate research-use export
(it de-doubles the ClinVar `source_record_id` format used in the v0.1.x line).
These public-candidate releases validate the public data package, integrity
manifest, and rendered resource sync before a paper-grade snapshot. They should
not be cited as a manuscript-grade biomedical dataset. Earlier tags (`v0.1.0`,
`v0.1.1`) remain available as historical artifacts.

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
  v0.2.0/
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
`v0.2.0` export is public-candidate research-use data, not manuscript-grade
evidence. See `CITATION.cff`.

## License

The released data (`releases/` and the referenced `data/source_snapshots/`
payloads) is made available under **CC BY 4.0** — see `LICENSE` for the full
terms, attribution requirements, and per-source notices. CC BY 4.0 is the
binding floor because MONDO (used for disease identity) is CC BY 4.0; HGNC and
Open Targets are CC0, and ClinVar/NCBI is public data (attribution requested).
Redistribution is permitted with attribution and without implying endorsement.
`-dev` releases are development artifacts and must not be cited as scientific
evidence.
