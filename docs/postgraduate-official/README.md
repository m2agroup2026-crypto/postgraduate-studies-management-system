# Official Postgraduate Reference — Faculty of Medicine, Assiut University

Verified snapshot: **2026-09-08**

This directory is the project’s authoritative working reference for postgraduate academic rules and program data. It is intentionally kept separate from runtime code so regulations can be reviewed, versioned, and then implemented through configurable platform data rather than hard-coded business logic.

## Source precedence

When sources differ, use this precedence and record the effective date before changing production rules:

1. **Current Faculty of Medicine postgraduate bylaw / credit-hours regulations and attached official documents.**
2. **Current Faculty of Medicine postgraduate pages** for Master’s, Doctorate, department-specific programs, forms, and examination guidance.
3. **Assiut University Postgraduate Studies & Research Sector** for university-wide rules: enrollment documents, research registration, language requirements, suspension/cancellation, supervision, thesis committees, and the official Faculty of Medicine program catalog.
4. **Current official University/Faculty announcements and council news** may prove that a program is operational, enrollment opened, results were approved, or a current count changed. They do not replace a ministerial/university approval decision when that legal evidence is required.
5. Older faculty/archive pages are supporting evidence only. They must not override a newer regulation without verification.

## Implementation rule

Do **not** hard-code a rule into Django/React merely because it appears in this snapshot. The platform is intended to scale across faculties and universities. Rules that can vary by institution, regulation version, degree, program, nationality, or date must be represented as configurable data with effective dates.

Examples that must remain configurable:

- admission requirements and required documents;
- degree/program availability;
- program approval and operational status;
- credit hours and course requirements;
- minimum/maximum enrollment periods;
- language requirements;
- research/publication requirements;
- supervision and committee validation rules;
- workflow and approval steps;
- fees, dates, schedules, and currently responsible officials.

## Files

- `diplomas.md` — professional/postgraduate diploma rules, catalog snapshot, and current-status reconciliation.
- `professional-diplomas.json` — machine-readable professional diploma catalog, operational evidence, and reconciliation against the current official count.
- `masters.md` — Master’s admission, duration, research, publication, thesis and exam requirements.
- `doctorate.md` — Doctorate admission, duration, qualifying/research, publication, thesis and committee requirements.
- `degree-rules.json` — machine-readable degree-level admission, duration, research, language and publication requirements.
- `academic-programs.json` — machine-readable official 33-row / 94-program Master’s and Doctorate catalog from the university postgraduate sector.
- `departments-reconciliation.md` — distinction and reconciliation between current organizational departments and historical academic catalog rows.
- `regulation-versions.json` — machine-readable regulation/version registry, including the 2011 program-catalog authority and the credit-hours regulation applied from October 2024.
- `faculty-postgraduate-hub-snapshot.json` — current Faculty postgraduate portal domains and their mapping to configurable platform modules.
- `shared-rules.md` — common enrollment, documents, language, research registration, suspension/cancellation, supervision, publication and committee rules.
- `official-decisions.json` — machine-readable key University decisions with dates and implementation mapping.
- `current-2026-updates.md` — current operational evidence and changes that are newer than older regulation/catalog snapshots.
- `sources.json` — official source manifest and verification metadata.
- `implementation-mapping.md` — mapping from official requirements to configurable platform entities and implementation order.

## Current regulation note

The Faculty of Medicine published that its **new postgraduate credit-hours regulation was approved and began application from October 2024**. The Faculty also maintains a current postgraduate hub that, as verified on 2026-09-08, exposes separate areas for the credit-hours regulation, points-based regulation, professional diplomas, Master’s, Doctorate, study schedules, postgraduate surveys, research and the scientific journal.

For implementation this means:

- every `AcademicEnrollment` must preserve the `RegulationVersion` that governed that student;
- historic enrollments must not be silently migrated to a later regulation;
- curricula, course requirements, assessment rules and degree requirements must be versioned;
- a published navigation item or regulation link is evidence of a domain, not permission to hard-code it as a universal module for every future faculty.

See `regulation-versions.json` and `faculty-postgraduate-hub-snapshot.json`.

## Important academic catalog note

The university postgraduate-sector page publishes a **33-row Faculty of Medicine academic program catalog** based on Ministerial Decree **1098 dated 24/05/2011**. The machine-readable transcription currently contains **94 Master’s/Doctorate programs**, including programs explicitly marked as waiting for ministerial approval.

The current Faculty of Medicine departments pages may show a different/current departmental structure because departments and services evolve over time. The application must therefore separate:

- `Department` — current organizational structure;
- `Program` — degree-granting academic program;
- `ProgramApproval` — legal/academic approval evidence and status;
- `RegulationVersion` — governing bylaw/rule version and effective dates.

Do not assume that every current department automatically has every degree, or that a catalog entry marked “pending ministerial decision” is active.

## Important professional-diploma reconciliation note

The enumerated postgraduate-sector catalog snapshot contains **17 named professional diploma entries**. A newer official Assiut University announcement dated **2026-09-08** states that the Faculty of Medicine reaches **24 professional diplomas** with the new academic year after activation of four new diplomas during the year.

Because that current announcement does not enumerate all 24 names, the project intentionally does **not** invent missing program names. `professional-diplomas.json` preserves the older named catalog, records newer program-level evidence, stores the current total count, and marks the remaining difference for official reconciliation.

## Production-data rule

Reference files are evidence/input, not an automatic production seed. Before a program or rule becomes active in production:

1. identify the applicable institution/faculty/program;
2. identify the governing regulation/decision and effective date;
3. preserve the source/evidence;
4. review conflicting/newer sources;
5. import through configurable platform data;
6. log the administrative approval in the audit trail.

This prevents a future regulation update, faculty rollout, or university rollout from requiring a code rewrite.
