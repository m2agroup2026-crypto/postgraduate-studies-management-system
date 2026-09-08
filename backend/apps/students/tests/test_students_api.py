import pytest
from rest_framework.test import APIClient

from apps.academics.models import Department
from apps.accounts.models import User
from apps.core.models import Permission, Role
from apps.students.models import Student
from apps.theses.models import Thesis


@pytest.fixture
def client():
    return APIClient()


def create_user(username, role):
    user = User.objects.create(username=username, role=role)
    user.set_unusable_password()
    user.save(update_fields=["password"])
    return user


@pytest.fixture
def department(db):
    return Department.objects.create(
        code="MED",
        name_ar="الباطنة",
        name_en="Internal Medicine",
    )


@pytest.fixture
def second_department(db):
    return Department.objects.create(
        code="SURG",
        name_ar="الجراحة",
        name_en="Surgery",
    )


@pytest.fixture
def students(db, department, second_department):
    first = Student.objects.create(
        university_id="PG0001",
        name_ar="أحمد علي",
        national_id="29901011234567",
        department=department,
    )
    second = Student.objects.create(
        university_id="PG0002",
        name_ar="منى حسن",
        national_id="29802021234567",
        department=second_department,
    )
    Thesis.objects.create(
        student=first,
        title_ar="رسالة أحمد",
        status="REGISTERED",
    )
    Thesis.objects.create(
        student=second,
        title_ar="رسالة منى",
        status="COMPLETED",
    )
    return first, second


@pytest.mark.django_db
def test_student_role_cannot_list_postgraduate_records(client):
    user = create_user("student_reader", User.Role.STUDENT)
    client.force_authenticate(user)

    response = client.get("/api/v1/students/")

    assert response.status_code == 403


@pytest.mark.django_db
def test_legacy_manager_can_list_and_view_sensitive_detail(client, students):
    user = create_user("director_reader", User.Role.POSTGRADUATE_DIRECTOR)
    client.force_authenticate(user)

    list_response = client.get("/api/v1/students/")
    detail_response = client.get(f"/api/v1/students/{students[0].id}/")

    assert list_response.status_code == 200
    assert list_response.data["capabilities"]["can_manage"] is True
    assert "national_id" not in list_response.data["results"][0]
    assert list_response.data["results"][0]["national_id_masked"] == "29**********67"
    assert detail_response.status_code == 200
    assert detail_response.data["student"]["national_id"] == "29901011234567"


@pytest.mark.django_db
def test_search_department_and_thesis_status_filters(client, students, department):
    user = create_user("reviewer_reader", User.Role.REVIEWER)
    client.force_authenticate(user)

    response = client.get(
        "/api/v1/students/",
        {
            "q": "أحمد",
            "department": department.id,
            "thesis_status": "REGISTERED",
        },
    )

    assert response.status_code == 200
    assert response.data["pagination"]["total"] == 1
    assert response.data["results"][0]["university_id"] == "PG0001"
    assert response.data["results"][0]["thesis"]["status"] == "REGISTERED"


@pytest.mark.django_db
def test_dynamic_role_permissions_are_authoritative(client, students):
    user = create_user("dynamic_reader", User.Role.STUDENT)
    view_permission = Permission.objects.create(
        code="students.view",
        name_ar="عرض الطلاب",
        name_en="View students",
    )
    role = Role.objects.create(
        name="STUDENT_RECORD_READER",
        name_ar="قارئ سجلات الطلاب",
        name_en="Student record reader",
    )
    role.permissions.add(view_permission)
    user.roles.add(role)
    client.force_authenticate(user)

    response = client.get("/api/v1/students/?page_size=1&page=2")

    assert response.status_code == 200
    assert response.data["pagination"] == {
        "page": 2,
        "page_size": 1,
        "total": 2,
        "pages": 2,
    }
    assert response.data["capabilities"]["can_manage"] is False
    assert response.data["results"][0]["university_id"] == "PG0002"
