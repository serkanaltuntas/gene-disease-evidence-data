# Data Dictionary

This repository distributes release artifacts for the Gene-Disease Evidence Index.
Fields are validated against the JSON Schemas under `schemas/`; this document is a
reader-facing, field-level summary of the public data model. It currently documents
`schema_version` **0.1.0**, shared by all current releases.

Controlled-vocabulary fields list their full allowed value set; a release typically uses a
subset.

## Release Files

Each release directory under `releases/<release-id>/` contains:

- `release.json`: release identity and research-use boundary metadata.
- `genes.json`: gene identity rows.
- `diseases.json`: disease identity rows.
- `sources.json`: included public source metadata (license/terms/citation, access dates,
  public-release approval, freshness).
- `source_snapshots.json`: immutable source snapshot manifests referenced by evidence rows.
- `associations.json`: normalized gene-disease association rows.
- `evidence_rows.jsonl`: source-attributed evidence rows backing associations.
- `review_artifacts.jsonl`: structured review and gate artifacts.
- `changelog.json`: release-to-release changes.
- `integrity.json`: SHA-256 checksums for repository files and downloadable archives.

## release.json

- `id`: release id (e.g. `v0.2.0`, `parkinson-v0.1.0`).
- `schema_version`: data-model version this release validates against (`0.1.0`).
- `generated_at`: ISO-8601 generation timestamp.
- `status`: one of `development_fixture`, `draft`, `public`, `paper_grade`. Public-candidate
  previews are `draft`; `development_fixture` (and any `-dev` release id) must not be cited
  as scientific evidence.
- `research_use_only`: boolean; always `true` for current releases.
- `notes`: release-scoped notes and boundaries.

## Gene Rows

`genes.json` rows describe identity, not disease evidence.

- `id`: stable gene identifier, currently HGNC id.
- `symbol`: approved gene symbol.
- `name`: approved gene name.
- `aliases`: alternate/previous symbols included in the release (drift hardening).
- `source_provenance`: sources used for gene identity and context.

## Disease Rows

`diseases.json` rows describe disease identity, not gene-disease evidence.

- `id`: stable disease identifier, currently MONDO id.
- `label`: disease label.
- `aliases`: alternate disease labels included in the release.
- `source_provenance`: sources used for disease identity and context.

## Source Rows

`sources.json` rows describe the included sources and their reuse boundaries.

- `id`: stable source identifier used throughout the release (e.g. `source:opentargets`).
- `name`: public source name.
- `version`, `accessed_at`: source version label and access date.
- `license`, `license_url`, `terms_url`: reuse metadata.
- `citation`, `citation_url`, `recommended_citations`: attribution metadata.
- `approved_for_public_release`: whether the source metadata passed the release source-use
  gate.
- `freshness`: source freshness object (see Freshness, below).
- `notes`: source-specific public rendering or interpretation boundaries.

Source names identify provenance only and do not imply endorsement by upstream sources.

## Source Snapshots

`source_snapshots.json` rows are immutable, content-addressed manifests of the exact source
material an evidence row was derived from.

- `id`: stable snapshot id (e.g.
  `snapshot:clinvar:gene-condition:alzheimer-mondo-0004975:2026-06-07`). A re-normalized
  snapshot of the same fetch gets a NEW id (snapshots are immutable once published).
- `source_ids`: source id(s) this snapshot belongs to.
- `path`: repo-relative path to the snapshot `records.jsonl` payload.
- `accessed_at`, `version`: when/what version of the source was captured.
- `license_note`: snapshot-specific reuse note.
- `record_count`: number of records in the snapshot payload.
- `sha256`: SHA-256 of the snapshot payload; recomputed and checked by `validate_release`.
- `freshness`: snapshot freshness object (see Freshness, below).

## Association Rows

`associations.json` rows are the central normalized records.

- `id`: deterministic association id derived from gene id and disease id.
- `gene_id`, `disease_id`: ids of the associated gene and disease rows.
- `status`: release status of the association (not a clinical status). One of
  `reviewed_brief`, `observed_unreviewed`, `single_source`, `below_threshold`,
  `source_absent`.
- `support_tier`: source-support tier. One of `multi_source_observed`,
  `single_source_observed`, `below_threshold`, `source_absent`. This is a count of
  independent supporting sources, not a confidence or truth score.
- `evidence_row_ids`: ids of evidence rows supporting or contextualizing the association.
- `source_coverage.supporting_source_ids`: sources with supporting evidence rows.
- `source_coverage.silent_source_ids`: included release sources that contributed no
  supporting or conflicting evidence for this association (silence is recorded, not hidden).
- `source_coverage.conflicting_source_ids`: sources with conflicting evidence rows.
- `source_coverage.source_independence_note`: release-generated note about support and
  independence limits.
- `review_state`: one of `not_reviewed`, `ai_reviewed`, `human_reviewed`. Automated or
  agent-assisted states do not imply human scientific validation.
- `caveats`: public caveats for interpretation and rendering.

## Evidence Rows

`evidence_rows.jsonl` rows are source-attributed observations. They are not combined into a
clinical confidence score.

- `id`: deterministic evidence row id, `ev:` + a hash of
  `source_id | source_record_id | association_id`.
- `association_id`: associated gene-disease row id.
- `snapshot_id`: immutable source snapshot id the row was derived from.
- `gene_id`, `disease_id`, `source_id`: normalized entity and provenance ids.
- `source_record_id`: source-specific record identifier. Canonical shapes:
  - Open Targets — `OT:<ensembl_gene_id>:<disease_local_id>`, e.g.
    `OT:ENSG00000145335:MONDO_0005180`.
  - ClinVar — `ClinVarGeneCondition:<ncbi_gene_id>:<gene_symbol>:<umls_concept_id>:<disease_curie>`,
    e.g. `ClinVarGeneCondition:6622:SNCA:C0030567:MONDO:0005180`. The disease namespace
    appears once (a `...:MONDO:MONDO:...` form in `v0.1.0`/`v0.1.1` is the prior,
    superseded encoding; see those releases' notes).
- `evidence_type`: one of `target_disease_association` (Open Targets) or
  `clinical_variant_context` (ClinVar).
- `direction`: one of `supporting`, `conflicting`, `context`.
- `statement`: source-attributed statement / rendering text.
- `source_metrics`: source-native metrics, when present (rendered as source signals, not
  truth or clinical-validity scores):
  - `open_targets_overall_score`: Open Targets' own aggregate score. Because its
    datasources can overlap with other sources' evidence, it is not an independent line of
    corroboration.
  - `open_targets_datatype_scores[]`, `open_targets_datasource_scores[]`: per-datatype /
    per-datasource `{ id, score }` entries. Labels such as `clinical` are Open Targets'
    own datatype/datasource names, not a clinical-use signal.
- `created_for`: pipeline stage or purpose that created the row.

## Review Artifacts

`review_artifacts.jsonl` rows record gate findings and advisory checks.

- `id`: deterministic review artifact id.
- `association_id`: association under review.
- `reviewer_role`: one of `evidence_grounding`, `source_independence`, `source_disagreement`,
  `claim_boundary`, `release_readiness`, `reader_usefulness`.
- `severity`: one of `info`, `warning`, `blocker`.
- `finding`: review finding text.
- `disposition`: one of `open`, `accepted`, `rejected`, `resolved`.

LLM or agent-assisted review artifacts are advisory. They do not replace human scientific
review or clinical validation.

## Freshness

Both `sources.json` rows and `source_snapshots.json` rows may carry a `freshness` object:

- `assessed_at`: date the freshness was assessed.
- `status`: one of `current`, `refresh_recommended`, `refresh_required`, `unknown`.
- `basis`: rationale for the status.
- `max_age_days`, `next_review_due`: recommended refresh window and next-review date.
- `paper_grade_blocker`: boolean; `true` means the condition is acceptable for a
  public-candidate preview but must be resolved before a paper-grade release.

## changelog.json

- `release_id`: release this changelog describes.
- `status`: release status (mirrors `release.json`).
- `changes[]`: ordered (oldest-first) change entries. Each has a `type` and `description`,
  plus type-specific fields (e.g. `source_release_id`, `scope_id`,
  `format_migration_commit`). Renderers treat the last entry as the headline change.

## integrity.json

A per-release manifest used to verify downloads.

- `manifest_version`: integrity manifest version (`release-integrity-v1`).
- `release_id`, `release_generated_at`, `release_status`, `schema_version`: release identity.
- `digest_algorithm`: `sha256`.
- `canonical_path_root`: root the `files[]` paths are relative to.
- `file_count`, `archive_count`: counts of verified entries.
- `files[]`: `{ path, bytes, sha256 }` for each released repository file.
- `archives[]`: `{ path, bytes, sha256 }` for each downloadable archive. The archive
  `sha256` is also matched against the GitHub Release asset digest.

## Glossary

These terms mirror the reader glossary on the rendered methods page
(`/gene-disease-evidence/methods/`) and are kept in sync with it.

- **Public-candidate** — A release suitable for public reader testing and traceability
  checks, but not yet paper-grade or externally peer reviewed.
- **Observed unreviewed** — A source-attributed signal exists in the included release data,
  but no reviewed brief or human scientific acceptance has been attached.
- **Automatic checks only** — The record passed deterministic or controlled referee checks.
  This is not the same as human scientific review.
- **Support tier** — A release-specific grouping by count of independent supporting sources.
  It is not a diagnosis, a clinical recommendation, or a universal truth score.
- **Source-reported score** — A score imported from an upstream source, such as Open
  Targets. It is rendered as provenance-bound source context, not as a combined confidence
  score for this resource.
- **Source silence** — An included source does not support an association in the current
  release. Silence is source- and release-specific; it is not evidence that no relationship
  exists.
- **Source disagreement** — Included sources conflict or provide materially different
  signals. The project exposes disagreement instead of blending it away.
- **Freshness status** — A release metadata field that says whether source or snapshot
  metadata is current, refresh-recommended, refresh-required, or unknown.
- **Paper-grade blocker** — A condition that may be acceptable for a public-candidate
  preview but must be resolved before a manuscript-grade or paper-grade release.

## Research-Use Boundary

The data package is for research use only. It is not medical advice, diagnosis, treatment
guidance, patient risk prediction, clinical decision support, clinical certainty, or a
complete statement of biomedical knowledge.
