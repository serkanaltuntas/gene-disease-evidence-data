# Data Dictionary

This repository distributes release artifacts for Gene-Disease Evidence Index.
Fields are validated against the JSON Schemas under `schemas/`; this document is a
reader-facing summary of the public data model.

## Release Files

Each release directory under `releases/<release-id>/` contains:

- `release.json`: release id, schema version, generation timestamp, status, and
  research-use boundary flags.
- `genes.json`: gene identity rows.
- `diseases.json`: disease identity rows.
- `sources.json`: included public source metadata, license/terms/citation
  metadata, access dates, and public-release approval flags.
- `source_snapshots.json`: immutable source snapshot manifests referenced by
  evidence rows.
- `associations.json`: normalized gene-disease association rows.
- `evidence_rows.jsonl`: source-attributed evidence rows backing associations.
- `review_artifacts.jsonl`: structured review and gate artifacts.
- `changelog.json`: release-to-release changes.
- `integrity.json`: SHA-256 checksums for files and downloadable archives.

## Gene Rows

`genes.json` rows describe identity, not disease evidence.

- `id`: stable gene identifier, currently HGNC id.
- `symbol`: approved gene symbol.
- `name`: approved gene name.
- `aliases`: alternate symbols or names included in the release.
- `source_provenance`: sources used for gene identity and context.

## Disease Rows

`diseases.json` rows describe disease identity, not gene-disease evidence.

- `id`: stable disease identifier, currently MONDO id.
- `label`: disease label.
- `source_provenance`: sources used for disease identity and context.

## Source Rows

`sources.json` rows describe the included sources and their reuse boundaries.

- `id`: stable source identifier used throughout the release.
- `name`: public source name.
- `version`: source version or access-specific version label.
- `accessed_at`: date the source was accessed for this release.
- `license`, `license_url`, `terms_url`: reuse metadata.
- `citation`, `citation_url`, `recommended_citations`: attribution metadata.
- `approved_for_public_release`: whether the source metadata passed the release
  source-use gate.
- `notes`: source-specific public rendering or interpretation boundaries.

Source names identify provenance only and do not imply endorsement by upstream
sources.

## Association Rows

`associations.json` rows are the central normalized records.

- `id`: deterministic association id derived from gene id and disease id.
- `gene_id`: id of the associated gene row.
- `disease_id`: id of the associated disease row.
- `status`: release status of the association. This is not a clinical status.
- `support_tier`: source-support tier, such as `single_source_observed` or
  `multi_source_observed`.
- `evidence_row_ids`: evidence rows supporting or contextualizing the association.
- `source_coverage.supporting_source_ids`: sources with supporting evidence rows.
- `source_coverage.silent_source_ids`: included release sources that did not
  contribute supporting or conflicting evidence for this association.
- `source_coverage.conflicting_source_ids`: sources with conflicting evidence rows.
- `source_coverage.source_independence_note`: release-generated note about source
  support and independence limits.
- `review_state`: current review state. Automated or agent-assisted review states
  do not imply human scientific validation.
- `caveats`: public caveats for interpretation and rendering.

## Evidence Rows

`evidence_rows.jsonl` rows are source-attributed observations. They are not
combined into a clinical confidence score.

- `id`: deterministic evidence row id.
- `association_id`: associated gene-disease row id.
- `snapshot_id`: immutable source snapshot id.
- `gene_id`, `disease_id`, `source_id`: normalized entity and provenance ids.
- `source_record_id`: source-specific record identifier.
- `evidence_type`: normalized evidence category.
- `direction`: whether the row is supporting or conflicting in this release.
- `statement`: source-attributed statement or rendering text.
- `source_metrics`: source-native metrics, when present. These are rendered as
  source signals, not truth scores or clinical validity scores.
- `created_for`: pipeline stage or purpose that created the row.

## Review Artifacts

`review_artifacts.jsonl` rows record gate findings and advisory checks.

- `id`: deterministic review artifact id.
- `association_id`: association under review.
- `reviewer_role`: review role, such as claim boundary, evidence grounding, source
  independence, or release readiness.
- `severity`: review severity label.
- `finding`: review finding text.
- `disposition`: current disposition.

LLM or agent-assisted review artifacts are advisory. They do not replace human
scientific review or clinical validation.

## Research-Use Boundary

The data package is for research use only. It is not medical advice, diagnosis,
treatment guidance, patient risk prediction, clinical decision support, clinical
certainty, or a complete statement of biomedical knowledge.
