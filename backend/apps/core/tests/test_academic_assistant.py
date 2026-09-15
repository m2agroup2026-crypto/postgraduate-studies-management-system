from datetime import date, timedelta

import pytest
from django.core.management import call_command
from rest_framework.test import APIClient

from apps.academics.models import Department
from apps.accounts.models import User
from apps.committees.models import DefenseCommittee
from apps.students.models import Student
from apps.theses.models import Thesis


@pytest.fixture
def academic_records():
    department = Department.objects.create(
        code="AI-MED",
        name_ar="الباطنة",
        name_en="Internal Medicine",
    )
    student = Student.objects.create(
        university_id="LEGACY-1",
        name_ar="طالب المساعد",
        department=department,
    )
    thesis = Thesis.objects.create(
        student=student,
        title_ar="رسالة ذكاء أكاديمي",
        status="DIRECTOR_APPROVED",
    )
    DefenseCommittee.objects.create(
        thesis=thesis,
        defense_date=date.today() + timedelta(days=7),
        status="SCHEDULED",
    )
    return student, thesis


def account(username, role):
    user = User.objects.create(username=username, role=role)
    user.set_unusable_password()
    user.save(update_fields=["password"])
    return user


@pytest.mark.django_db
def test_assistant_get_requires_authentication_and_scopes_brief(academic_records):
    client = APIClient()
    assert client.get("/api/v1/assistant/").status_code == 401

    vice_dean = account("assistant_vice_dean", User.Role.VICE_DEAN_POSTGRADUATE)
    call_command("seed_roles")
    vice_dean.roles.set([vice_dean.roles.model.objects.get(name="VICE_DEAN_POSTGRADUATE")])
    client.force_authenticate(vice_dean)

    response = client.get("/api/v1/assistant/")

    assert response.status_code == 200
    assert response.data["source"] == "live_academic_data"
    assert response.data["brief"]["metrics"] == {
        "students": 1,
        "theses": 1,
        "committees": 1,
    }


@pytest.mark.django_db
def test_assistant_post_routes_student_and_workflow_intelligence(academic_records):
    vice_dean = account("assistant_vice_dean", User.Role.VICE_DEAN_POSTGRADUATE)
    call_command("seed_roles")
    vice_dean.roles.set([vice_dean.roles.model.objects.get(name="VICE_DEAN_POSTGRADUATE")])
    client = APIClient()
    client.force_authenticate(vice_dean)

    student_response = client.post(
        "/api/v1/assistant/",
        {"message": "Find student LEGACY-1"},
        format="json",
    )
    workflow_response = client.post(
        "/api/v1/assistant/",
        {"message": "ما الطلبات التي تنتظر قراري؟"},
        format="json",
    )

    assert student_response.status_code == 200
    assert student_response.data["intent"] == "students"
    assert student_response.data["data"]["university_id"] == "LEGACY-1"
    assert "LEGACY-1" in student_response.data["answer"]
    assert workflow_response.status_code == 200
    assert workflow_response.data["intent"] == "workflow"
    assert workflow_response.data["data"] == {
        "status": "DIRECTOR_APPROVED",
        "count": 1,
    }


@pytest.mark.django_db
def test_assistant_does_not_leak_student_data_without_permission(academic_records):
    student_user = account("assistant_student", User.Role.STUDENT)
    client = APIClient()
    client.force_authenticate(student_user)

    response = client.post(
        "/api/v1/assistant/",
        {"message": "Find student LEGACY-1"},
        format="json",
    )

    assert response.status_code == 200
    assert response.data["intent"] == "students"
    assert response.data["data"] == {"authorized": False}
    assert "LEGACY-1" not in response.data["answer"]
