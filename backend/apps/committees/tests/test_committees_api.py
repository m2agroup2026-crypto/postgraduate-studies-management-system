from datetime import date, timedelta

import pytest
from rest_framework.test import APIClient

from apps.accounts.models import User
from apps.academics.models import Department
from apps.committees.models import DefenseCommittee, DefenseScheduleEvent
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
def theses(db, department, second_department):
    first_student = Student.objects.create(
        university_id="PG1001",
        name_ar="طالب أول",
        national_id="29901011234567",
        department=department,
    )
    second_student = Student.objects.create(
        university_id="PG1002",
        name_ar="طالب ثان",
        national_id="29802021234567",
        department=second_department,
    )
    first = Thesis.objects.create(
        student=first_student,
        title_ar="رسالة مناقشة أولى",
        status="FINAL_APPROVED",
    )
    second = Thesis.objects.create(
        student=second_student,
        title_ar="رسالة مناقشة ثانية",
        status="FINAL_APPROVED",
    )
    return first, second


@pytest.mark.django_db
def test_student_role_cannot_view_committee_workspace(client, theses):
    user = create_user("student_committee", User.Role.STUDENT)
    client.force_authenticate(user)

    response = client.get("/api/v1/committees/")

    assert response.status_code == 403


@pytest.mark.django_db
def test_reviewer_can_view_but_cannot_schedule(client, theses):
    user = create_user("reviewer_committee", User.Role.REVIEWER)
    client.force_authenticate(user)
    target_date = date.today() + timedelta(days=14)

    list_response = client.get("/api/v1/committees/")
    schedule_response = client.post(
        f"/api/v1/committees/{theses[0].id}/schedule/",
        {"defense_date": target_date.isoformat()},
        format="json",
    )

    assert list_response.status_code == 200
    assert list_response.data["capabilities"]["can_manage"] is False
    assert schedule_response.status_code == 403
    assert DefenseCommittee.objects.count() == 0


@pytest.mark.django_db
def test_legacy_manager_can_schedule_reschedule_and_clear_with_audit(client, theses):
    user = create_user("director_committee", User.Role.POSTGRADUATE_DIRECTOR)
    client.force_authenticate(user)
    first_date = date.today() + timedelta(days=10)
    second_date = date.today() + timedelta(days=20)

    scheduled = client.post(
        f"/api/v1/committees/{theses[0].id}/schedule/",
        {"defense_date": first_date.isoformat(), "notes": "موعد أول"},
        format="json",
    )
    rescheduled = client.post(
        f"/api/v1/committees/{theses[0].id}/schedule/",
        {"defense_date": second_date.isoformat(), "notes": "تعديل الموعد"},
        format="json",
    )
    cleared = client.post(
        f"/api/v1/committees/{theses[0].id}/schedule/",
        {"defense_date": None, "notes": "إلغاء الموعد مؤقتًا"},
        format="json",
    )

    committee = DefenseCommittee.objects.get(thesis=theses[0])
    events = list(DefenseScheduleEvent.objects.filter(committee=committee).order_by("id"))

    assert scheduled.status_code == 200
    assert rescheduled.status_code == 200
    assert cleared.status_code == 200
    assert committee.defense_date is None
    assert [event.event_type for event in events] == [
        DefenseScheduleEvent.EventType.SCHEDULED,
        DefenseScheduleEvent.EventType.RESCHEDULED,
        DefenseScheduleEvent.EventType.DATE_CLEARED,
    ]
    assert events[0].new_date == first_date
    assert events[1].old_date == first_date
    assert events[1].new_date == second_date
    assert events[2].old_date == second_date
    assert events[2].new_date is None


@pytest.mark.django_db
def test_schedule_filters_and_summary_are_database_backed(client, theses):
    user = create_user("committee_reader", User.Role.REVIEWER)
    upcoming_date = date.today() + timedelta(days=7)
    DefenseCommittee.objects.create(thesis=theses[0], defense_date=upcoming_date)
    client.force_authenticate(user)

    upcoming = client.get("/api/v1/committees/?schedule=upcoming")
    unscheduled = client.get("/api/v1/committees/?schedule=unscheduled")

    assert upcoming.status_code == 200
    assert upcoming.data["pagination"]["total"] == 1
    assert upcoming.data["results"][0]["thesis"]["id"] == theses[0].id
    assert upcoming.data["summary"] == {
        "total_theses": 2,
        "scheduled": 1,
        "upcoming": 1,
        "unscheduled": 1,
    }
    assert unscheduled.status_code == 200
    assert unscheduled.data["pagination"]["total"] == 1
    assert unscheduled.data["results"][0]["thesis"]["id"] == theses[1].id


@pytest.mark.django_db
def test_dynamic_manage_role_overrides_student_legacy_role(client, theses):
    user = create_user("dynamic_committee_manager", User.Role.STUDENT)
    view_permission = Permission.objects.create(
        code="committees.view",
        name_ar="عرض اللجان",
        name_en="View committees",
    )
    manage_permission = Permission.objects.create(
        code="committees.manage",
        name_ar="إدارة اللجان",
        name_en="Manage committees",
    )
    role = Role.objects.create(
        name="DEFENSE_COORDINATOR",
        name_ar="منسق المناقشات",
        name_en="Defense coordinator",
    )
    role.permissions.add(view_permission, manage_permission)
    user.roles.add(role)
    client.force_authenticate(user)
    target_date = date.today() + timedelta(days=30)

    response = client.post(
        f"/api/v1/committees/{theses[1].id}/schedule/",
        {"defense_date": target_date.isoformat()},
        format="json",
    )

    assert response.status_code == 200
    assert response.data["capabilities"]["can_manage"] is True
    assert response.data["record"]["defense"]["defense_date"] == target_date.isoformat()
    assert DefenseScheduleEvent.objects.filter(
        committee__thesis=theses[1],
        performed_by=user,
    ).exists()


@pytest.mark.django_db
def test_invalid_date_is_rejected_without_creating_committee(client, theses):
    user = create_user("staff_committee", User.Role.STAFF)
    client.force_authenticate(user)

    response = client.post(
        f"/api/v1/committees/{theses[0].id}/schedule/",
        {"defense_date": "2026-99-99"},
        format="json",
    )

    assert response.status_code == 400
    assert DefenseCommittee.objects.count() == 0
