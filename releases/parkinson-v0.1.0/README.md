# parkinson-v0.1.0

Public-candidate research-use draft for the Parkinson disease scope of the Gene-Disease
Evidence Index — the second disease alongside the Alzheimer line.

This release is research-use only. It is not medical advice, diagnosis, treatment
guidance, patient risk prediction, clinical decision support, clinical certainty, or a
claim of complete biomedical knowledge.

It was built by applying the reviewed Parkinson Open Targets and ClinVar candidates to a
Parkinson-scoped release shell, using the clean single-MONDO ClinVar `source_record_id`
format (`ClinVarGeneCondition:...:MONDO:<id>`). It includes:

- 1 disease: Parkinson disease (`MONDO:0005180`)
- 6 genes: SNCA, LRRK2, PRKN, PINK1, PARK7, GBA1
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

Per ADR 0004, the two-disease pilot (Alzheimer + Parkinson) is a de-risk gate for the
scaled archive, not the manuscript dataset. Do not cite this draft as a manuscript-grade
biomedical dataset.
