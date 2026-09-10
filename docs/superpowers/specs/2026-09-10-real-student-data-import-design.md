# Real Student Data Import Design

## Goal

Import the supplied `Digitalization_Data` workbook into the postgraduate platform so authorized users, including the Vice Dean, can search real student records and see database-backed dashboard summaries. Preserve the original workbook and every source row without silently discarding unsupported fields.

## Source Decision

- `Digitalization_Data(1).xlsx` is the authoritative import source: one worksheet, 4,084 rows, 110 fields, and a unique non-empty `ID` column.
- `222222(6).xlsx` is a legacy search/report workbook containing formulas, sparse helper sheets, and empty templates. It is not imported as an authoritative student source.

## Architecture

### Import batch and raw archive

Extend the migration domain with a row-level archive model. Each archived row stores the batch, sheet name, source row number, stable source identifier, a checksum, the complete JSON-normalized source payload, validation state, error details, and the linked student when imported. A unique constraint on batch/source identifier and checksum-based comparison make reruns deterministic and auditable.

The source file itself is never modified. Imports create or update application records only through a management command and a database transaction.

### Canonical mapping

The first release maps fields supported by current domain models:

- `ID` -> `Student.university_id`, namespaced as the stable legacy identifier.
- `الاسم` -> `Student.name_ar`.
- `القسم` / `Department` -> normalized `Department` records.
- `الدرجة` / `Degree` and enrollment dates -> `AcademicDegree`, `Program`, `AcademicYear`, and `AcademicEnrollment` where values are valid.
- Arabic thesis title and the latest supported title change -> `Thesis.title_ar`.
- defense date -> `DefenseCommittee.defense_date`.
- freeze, reinstatement, cancellation, extension, thesis-title change, and committee milestones -> `AcademicHistoryEvent` entries where a source value provides evidence.

Unsupported source fields remain available in the raw archive. They are not forced into unrelated columns.

### Status derivation

Statuses are derived only from explicit source evidence. Grant dates take precedence over defense dates; defense/committee evidence takes precedence over thesis registration; cancellation evidence marks the enrollment history but does not delete the student. Ambiguous rows are flagged for review rather than assigned a misleading status.

## Command and safety controls

Provide an `import_legacy_students` command with:

- dry-run as the default behavior;
- explicit `--commit` required for database writes;
- `--source` path and optional `--sheet`;
- batch checksum and duplicate detection;
- row-level validation and bounded error reporting;
- atomic commit for accepted records;
- summary counts for read, valid, imported, updated, skipped, duplicate, and failed rows.

Existing students are matched by the namespaced source `ID`. The importer never matches by name alone and never deletes records. Rerunning the same file does not duplicate students, theses, defenses, enrollments, or history events.

## Dashboard and search

The current students, theses, committees, and executive dashboard APIs continue to read application tables, not Excel at request time. This keeps search fast and permission-aware. After a committed import:

- the Vice Dean can search students by name or university/source identifier;
- thesis and committee searches use imported records;
- KPI counts and recent student records update from the database;
- incomplete reports and platform settings remain hidden.

No raw phone number, email, or unsupported personal field is exposed through the dashboard API.

## Testing and acceptance

Tests cover source analysis, dry-run non-mutation, committed import, idempotent rerun, duplicate IDs, missing required values, status derivation, history creation, and Vice Dean search/dashboard visibility. Acceptance requires reconciliation between the 4,084 source rows and the command summary, with every source row classified as imported, updated, skipped, duplicate, or failed.

## Operational rollout

1. Run dry-run against a database backup/staging copy.
2. Review reconciliation and validation failures.
3. Run the committed import on the approved database.
4. Execute API smoke tests as `vice_dean`.
5. Retain the batch and row archive for audit and future mapping of the remaining fields.

Production rollout must not enable `PGMS_SEED_DEMO`.
