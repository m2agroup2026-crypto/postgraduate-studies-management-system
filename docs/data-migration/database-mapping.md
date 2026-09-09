# Legacy Database Mapping

## Purpose

Mapping legacy academic records into the Enterprise Postgraduate Studies Management Platform.

## Domains

- Student
- Academic Enrollment
- Thesis
- Supervision
- Committees
- Documents
- Academic History


## Migration Principles

- Preserve original legacy identifiers.
- Never overwrite historical information.
- Normalize duplicated data.
- Convert status columns into timeline events.
- Validate before database import.
- Keep legacy source traceability.


## Student Mapping

| Legacy Field | Target Model | Target Field |
|---|---|---|
| ID | Student | legacy_id |
| الاسم | Student | name_ar |
| Full Name | Student | name_en |
| النوع | Student | gender |
| رقم التليفون | Student | phone |
| البريد الالكترونى | Student | email |
| الجنسية | Student | nationality |


## Academic Enrollment Mapping

| Legacy Field | Target Model | Target Field |
|---|---|---|
| الدرجة | AcademicDegree | degree |
| القسم | Department | department |
| تاريخ القيد(مجلس كلية) | AcademicEnrollment | registration_date |
| عام القيد | AcademicEnrollment | academic_year |


## Thesis Mapping

| Legacy Field | Target Model | Target Field |
|---|---|---|
| عنوان البحث باللغة العربية | Thesis | title_ar |
| عنوان البحث باللغة الانجليزية | Thesis | title_en |
| IRB Number | Thesis | irb_number |


## Academic History Mapping

| Legacy Field | Event |
|---|---|
| تجميد قيد | ENROLLMENT_FROZEN |
| إعادة قيد | ENROLLMENT_REACTIVATED |
| إلغاء قيد | ENROLLMENT_CANCELLED |
| تغيير عنوان البحث | THESIS_TITLE_CHANGED |
| تعديل لجنة الإشراف | SUPERVISION_UPDATED |
