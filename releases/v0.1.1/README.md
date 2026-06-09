# v0.1.1

Public-candidate metadata refresh for the Alzheimer disease scope of the Gene-Disease
Evidence Index.

This release is research-use only. It is not medical advice, diagnosis, treatment
guidance, patient risk prediction, clinical decision support, clinical certainty, or a
claim of complete biomedical knowledge.

This draft is derived from `v0.1.0` and adds source/snapshot freshness metadata for
the public renderer and export gate. The association content remains the same public
candidate scope. It includes:

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

Do not cite this draft as a manuscript-grade biomedical dataset. A future paper-grade
snapshot will need a fixed public archive, integrity verification, rendered-page sync,
and additional review/error analysis.
