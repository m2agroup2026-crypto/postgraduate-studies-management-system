# Official Postgraduate Reference — Faculty of Medicine, Assiut University

Verified snapshot: **2026-09-08**

This directory is the project’s authoritative working reference for postgraduate academic rules and program data. It is intentionally kept separate from runtime code so regulations can be reviewed, versioned, and then implemented through configurable platform data rather than hard-coded business logic.

## Source precedence

When sources differ, use this precedence and record the effective date before changing production rules:

1. **Current Faculty of Medicine postgraduate bylaw / credit-hours regulations and attached official documents.**
2. **Current Faculty of Medicine postgraduate pages** for Master’s, Doctorate, department-specific programs, forms, and examination guidance.
3. **Assiut University Postgraduate Studies & Research Sector** for university-wide rules: enrollment documents, research registration, language requirements, suspension/cancellation, supervision, thesis committees, and the official Faculty of Medicine program catalog.
4. Older faculty/archive pages are supporting evidence only. They must not override a newer regulation without verification.

## Implementation rule

Do **not** hard-code a rule into Django/React merely because it appears in this snapshot. The platform is intended to scale across faculties and universities. Rules that can vary by institution, regulation version, degree, program, nationality, or date must be represented as configurable data with effective dates.

Examples that must remain configurable:

- admission requirements and required documents;
- degree/program availability;
- program approval status;
- credit hours and course requirements;
- minimum/maximum enrollment periods;
- language requirements;
- research/publication requirements;
- workflow and approval steps;
- fees, dates, schedules, and currently responsible officials.

## Files

- `diplomas.md` — professional/postgraduate diploma rules and Faculty of Medicine professional diploma catalog.
- `masters.md` — Master’s admission, duration, research, publication, and thesis rules.
- `doctorate.md` — Doctorate admission, duration, qualifying/research, publication, and thesis rules.
- `academic-programs.json` — machine-readable official 33-row academic program catalog from the university postgraduate sector.
- `shared-rules.md` — common enrollment, language, research registration, suspension/cancellation, supervision and committee rules.
- `sources.json` — official source manifest and verification metadata.

## Important catalog note

The university postgraduate-sector page publishes a **33-row Faculty of Medicine academic program catalog** based on Ministerial Decree **1098 dated 24/05/2011**, with later programs marked where ministerial approval is still pending. The current Faculty of Medicine departments page may show a different/current departmental structure because departments and services evolve over time. The application must therefore separate:

- `Department` (current organizational structure),
- `Program` (degree-granting academic program), and
- `ProgramApproval/RegulationVersion` (legal/academic authority and effective dates).

Do not assume that every current department automatically has every degree, or that a catalog entry marked “pending ministerial decision” is active.
