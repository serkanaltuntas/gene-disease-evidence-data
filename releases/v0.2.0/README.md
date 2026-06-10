# v0.2.0

Public-candidate release for the Alzheimer disease scope of the Gene-Disease Evidence
Index, carrying the de-doubled ClinVar `source_record_id` format.

This release is research-use only. It is not medical advice, diagnosis, treatment
guidance, patient risk prediction, clinical decision support, clinical certainty, or a
claim of complete biomedical knowledge.

This release carries the ClinVar gene-condition `source_record_id` normalized to a single
MONDO namespace (`ClinVarGeneCondition:...:MONDO:<id>`, previously
`...:MONDO:MONDO:<id>`). It is built from `v0.1.1` with the ClinVar gene-condition records
re-normalized into a new immutable snapshot
(`snapshot:clinvar:gene-condition:alzheimer-mondo-0004975:2026-06-07-srid2`, the same
2026-06-07 ClinVar fetch in corrected format). Relative to `v0.1.1`, ClinVar evidence-row
ids are rotated; genes, diseases, Open Targets evidence, scores, and association membership
are unchanged. It includes:

- 1 disease: Alzheimer disease (`MONDO:0004975`)
- 5 genes: APP, APOE, PSEN1, PSEN2, GRIN1
- 4 sources: HGNC, MONDO, Open Targets Platform, ClinVar
- 2 evidence types: target-disease association and clinical variant/condition context
- source manifests, source snapshots, evidence-backed associations, review artifacts,
  and release changelog metadata
- source and source-snapshot freshness metadata for public-candidate transparency

Source-use boundaries remain active:

- MONDO is used for disease identity/context under CC BY 4.0, not as gene-disease evidence.
- Open Targets scores are source-attributed evidence signals, not truth, clinical validity,
  or a combined confidence score.
- ClinVar rows are variant/condition context and must not be used for diagnosis,
  treatment guidance, patient risk prediction, clinical decision support, clinical
  certainty, or medical interpretation advice.
- Source names identify provenance only and do not imply endorsement.

`v0.1.0` and `v0.1.1` — including their published public-data-repo tags and the original
`...:2026-06-07` ClinVar snapshot — retain the prior doubled-namespace format and are left
unchanged.

Do not cite this draft as a manuscript-grade biomedical dataset. A future paper-grade
snapshot will need a fixed public archive, integrity verification, rendered-page sync,
and additional review/error analysis.
