import pytest
from rest_framework.test import APIClient

from apps.academics.models import Department
from apps.accounts.models import User
from apps.core.models import ApprovalAction, Permission, Role
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
def theses(db, department, second_department):
    first_student = Student.objects.create(
        university_id="PG0001",
        name_ar="أحمد علي",
        department=department,
    )
    second_student = Student.objects.create(
        university_id="PG0002",
        name_ar="منى حسن",
        department=second_department,
    )
    first = Thesis.objects.create(
        student=first_student,
        title_ar="دراسة تجريبية في الباطنة",
        status="REGISTERED",
    )
    second = Thesis.objects.create(
        student=second_student,
        title_ar="دراسة جراحية متقدمة",
        status="COMPLETED",
    )
    return first, second


@pytest.mark.django_db
def test_student_role_cannot_list_theses(client):
    user = create_user("student_thesis_reader", User.Role.STUDENT)
    client.force_authenticate(user)

    response = client.get("/api/v1/theses/")

    assert response.status_code == 403


@pytest.mark.django_db
def test_search_department_and_status_filters(client, theses, department):
    user = create_user("reviewer_thesis_reader", User.Role.REVIEWER)
    client.force_authenticate(user)

    response = client.get(
        "/api/v1/theses/",
        {
            "q": "تجريبية",
            "department": department.id,
            "status": "REGISTERED",
        },
    )

    assert response.status_code == 200
    assert response.data["pagination"]["total"] == 1
    assert response.data["results"][0]["student"]["university_id"] == "PG0001"
    assert response.data["results"][0]["status"] == "REGISTERED"


@pytest.mark.django_db
def test_staff_can_submit_thesis_and_audit_is_created(client, theses):
    user = create_user("staff_submitter", User.Role.STAFF)
    client.force_authenticate(user)

    response = client.post(
        f"/api/v1/theses/{theses[0].id}/actions/",
        {"action": "SUBMIT", "notes": "تم استكمال الملف"},
        format="json",
    )

    theses[0].refresh_from_db()
    audit = ApprovalAction.objects.get(request_type="Thesis", object_id=theses[0].id)

    assert response.status_code == 200
    assert theses[0].status == "SUBMITTED"
    assert audit.action == "SUBMIT"
    assert audit.from_status == "REGISTERED"
    assert audit.to_status == "SUBMITTED"
    assert audit.notes == "تم استكمال الملف"
    assert response.data["workflow"]["history"][0]["action"] == "SUBMIT"


@pytest.mark.django_db
def test_reviewer_can_move_submitted_thesis_under_review(client, theses):
    thesis = theses[0]
    thesis.status = "SUBMITTED"
    thesis.save(update_fields=["status"])
    user = create_user("workflow_reviewer", User.Role.REVIEWER)
    client.force_authenticate(user)

    response = client.post(
        f"/api/v1/theses/{thesis.id}/actions/",
        {"action": "REVIEW"},
        format="json",
    )

    thesis.refresh_from_db()
    assert response.status_code == 200
    assert thesis.status == "UNDER_REVIEW"


@pytest.mark.django_db
def test_reject_and_return_follow_current_approval_stage(client, theses):
    thesis = theses[0]
    thesis.status = "UNDER_REVIEW"
    thesis.save(update_fields=["status"])

    vice_dean = create_user("vice_dean_rejector", User.Role.VICE_DEAN_POSTGRADUATE)
    client.force_authenticate(vice_dean)
    denied = client.post(
        f"/api/v1/theses/{thesis.id}/actions/",
        {"action": "RETURN"},
        format="json",
    )

    director = create_user("director_returner", User.Role.POSTGRADUATE_DIRECTOR)
    client.force_authenticate(director)
    allowed = client.post(
        f"/api/v1/theses/{thesis.id}/actions/",
        {"action": "RETURN", "notes": "استكمال المستندات"},
        format="json",
    )

    thesis.refresh_from_db()
    assert denied.status_code == 403
    assert allowed.status_code == 200
    assert thesis.status == "RETURNED"


@pytest.mark.django_db
def test_active_dynamic_roles_override_legacy_workflow_role(client, theses):
    user = create_user("dynamic_workflow_user", User.Role.DEAN)
    view_permission = Permission.objects.create(
        code="theses.view",
        name_ar="عرض الرسائل العلمية",
        name_en="View theses",
    )
    staff_role = Role.objects.create(
        name="STAFF",
        name_ar="موظف ديناميكي",
        name_en="Dynamic staff",
    )
    staff_role.permissions.add(view_permission)
    user.roles.add(staff_role)
    client.force_authenticate(user)

    detail = client.get(f"/api/v1/theses/{theses[0].id}/")
    forbidden = client.post(
        f"/api/v1/theses/{theses[0].id}/actions/",
        {"action": "DEAN_APPROVE"},
        format="json",
    )
    submitted = client.post(
        f"/api/v1/theses/{theses[0].id}/actions/",
        {"action": "SUBMIT"},
        format="json",
    )

    assert detail.status_code == 200
    assert detail.data["workflow"]["available_actions"] == ["SUBMIT"]
    assert forbidden.status_code == 403
    assert submitted.status_code == 200
    assert submitted.data["thesis"]["status"] == "SUBMITTED"
