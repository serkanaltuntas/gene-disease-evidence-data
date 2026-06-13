# Schema coverage

`manifest.json` maps each committed JSON schema to the artifact type it protects, example paths, and the validator or tests that enforce it.

The schema set covers three layers:

- Release payloads: `release`, `gene`, `disease`, `source`, `source-snapshot`, `association`, `evidence-row`, and `review-artifact`.
- Release candidate controls: checklist manifests, human review decisions, source recheck artifacts, and integrity manifests.
- Public export gates: source gate, source gate decision, final public export gate, and final public export gate decision.

Boundary fields such as `public_export_approval`, `paper_grade_approved`, `public_export_source_recheck_approved`, and `public_export_approved` are intentionally schema-bound so approval state cannot be implied by nearby development artifacts.
