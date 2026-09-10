from io import StringIO

import pytest
from django.core.management import call_command
from openpyxl import Workbook
from rest_framework.test import APIClient

from apps.academic_history.models import AcademicHistoryEvent
from apps.accounts.models import User
from apps.committees.models import DefenseCommittee
from apps.data_migration.models import LegacyImportBatch, LegacyImportRow
from apps.students.models import AcademicEnrollment, Student
from apps.theses.models import Thesis

HEADERS = [
    "ID",
    "الاسم",
    "الدرجة",
    "القسم",
    "Department",
    "تاريخ القيد(مجلس كلية)",
    "عنوان البحث باللغة العربية",
    "تاريخ المناقشة",
    "تاريخ المنح",
    "تجميد قيد؟",
    "الغاء قيد؟",
]


def make_workbook(path, rows):
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Digitalization November  2022"
    sheet.append(HEADERS)
    for row in rows:
        sheet.append(row)
    workbook.save(path)


@pytest.mark.django_db
def test_dry_run_reconciles_rows_without_mutating_database(tmp_path):
    source = tmp_path / "legacy.xlsx"
    make_workbook(
        source,
        [
            [1, "طالب أول", "ماجستير", "الباطنة", "Internal Medicine"],
            [2, "طالب بلا قسم", "دكتوراه", None, None],
            [1, "طالب مكرر", "ماجستير", "الجراحة", "Surgery"],
        ],
    )
    output = StringIO()

    call_command("import_legacy_students", source=str(source), stdout=output)

    assert '"mode": "dry-run"' in output.getvalue()
    assert '"read": 3' in output.getvalue()
    assert '"valid": 1' in output.getvalue()
    assert Student.objects.count() == 0
    assert LegacyImportBatch.objects.count() == 0


@pytest.mark.django_db
def test_committed_import_is_idempotent_and_visible_to_vice_dean(tmp_path):
    source = tmp_path / "legacy.xlsx"
    make_workbook(
        source,
        [
            [
                101,
                "أحمد طالب حقيقي",
                "ماجستير",
                "الباطنة",
                "Internal Medicine",
                "2022-10-10",
                "عنوان رسالة حقيقية",
                "2026-06-15",
                None,
                False,
                False,
            ],
            [
                102,
                "منى طالبة حقيقية",
                "دكتوراه",
                "الجراحة",
                "Surgery",
                "2021-09-01",
                "عنوان رسالة دكتوراه",
                "2025-05-01",
                "2025-08-01",
                False,
                False,
            ],
        ],
    )

    call_command("import_legacy_students", source=str(source), commit=True)
    first_history_count = AcademicHistoryEvent.objects.count()
    call_command("import_legacy_students", source=str(source), commit=True)

    assert Student.objects.count() == 2
    assert Thesis.objects.count() == 2
    assert DefenseCommittee.objects.count() == 2
    assert AcademicEnrollment.objects.count() == 2
    assert LegacyImportBatch.objects.count() == 1
    assert LegacyImportRow.objects.count() == 2
    assert AcademicHistoryEvent.objects.count() == first_history_count
    assert Thesis.objects.get(student__university_id="LEGACY-102").status == "COMPLETED"

    vice_dean = User.objects.create(username="vice_dean", role=User.Role.VICE_DEAN_POSTGRADUATE)
    vice_dean.set_unusable_password()
    vice_dean.save(update_fields=["password"])
    call_command("seed_roles")
    client = APIClient()
    client.force_authenticate(vice_dean)

    search = client.get("/api/v1/students/", {"q": "أحمد طالب"})
    dashboard = client.get("/api/v1/dashboard/")

    assert search.status_code == 200
    assert search.data["pagination"]["total"] == 1
    assert search.data["results"][0]["university_id"] == "LEGACY-101"
    assert dashboard.status_code == 200
    assert dashboard.data["metrics"]["students"] == 2
    assert dashboard.data["metrics"]["theses"] == 2
