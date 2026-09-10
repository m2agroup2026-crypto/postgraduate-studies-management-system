from datetime import date, timedelta
from pathlib import Path

import pytest
from django.core.management import call_command
from django.core.management.base import CommandError
from rest_framework.test import APIClient

from apps.academics.models import Department
from apps.accounts.models import User
from apps.committees.models import DefenseCommittee
from apps.core.authorization import has_permission
from apps.core.management.commands.seed_roles import PLATFORM_PERMISSIONS, ROLE_MATRIX
from apps.core.models import Permission, Role
from apps.students.models import Student
from apps.theses.models import Thesis


@pytest.fixture
def client():
    return APIClient()


def create_account(username, role=User.Role.STAFF):
    user = User.objects.create(username=username, role=role)
    user.set_unusable_password()
    user.save(update_fields=["password"])
    return user


@pytest.mark.django_db
def test_seed_roles_is_idempotent_and_replaces_stale_permissions():
    ahmed = create_account("ahmed")
    vice_dean = create_account("vice_dean", User.Role.VICE_DEAN_POSTGRADUATE)
    intruder = create_account("another_admin")

    call_command("seed_roles")
    platform = Role.objects.get(name="PLATFORM_ADMIN")
    stale = Permission.objects.create(code="legacy.stale", name_ar="قديمة", name_en="Legacy stale")
    platform.permissions.add(stale)
    intruder.roles.add(platform)

    call_command("seed_roles")

    platform.refresh_from_db()
    ahmed.refresh_from_db()
    vice_dean.refresh_from_db()
    intruder.refresh_from_db()
    assert set(platform.permissions.values_list("code", flat=True)) == PLATFORM_PERMISSIONS
    assert set(ahmed.roles.values_list("name", flat=True)) == {
        "PLATFORM_ADMIN",
        "PROGRAM_DIRECTOR",
    }
    assert set(vice_dean.roles.values_list("name", flat=True)) == {"VICE_DEAN_POSTGRADUATE"}
    assert not intruder.roles.filter(name="PLATFORM_ADMIN").exists()
    assert Role.objects.count() == len(ROLE_MATRIX)


@pytest.mark.django_db
def test_platform_permissions_do_not_leak_to_academic_roles():
    call_command("seed_roles")

    for role in Role.objects.exclude(name="PLATFORM_ADMIN"):
        assigned = set(role.permissions.values_list("code", flat=True))
        assert assigned.isdisjoint(PLATFORM_PERMISSIONS), role.name


@pytest.mark.django_db
def test_vice_dean_permission_matrix_and_api_access(client):
    vice_dean = create_account("vice_dean", User.Role.VICE_DEAN_POSTGRADUATE)
    call_command("seed_roles")
    vice_dean.refresh_from_db()
    client.force_authenticate(vice_dean)

    permissions = set(vice_dean.effective_permissions())
    assert {
        "students.view",
        "theses.view",
        "committees.view",
        "reports.view",
        "registration.approve",
        "committee.approve",
    }.issubset(permissions)
    assert permissions.isdisjoint(
        PLATFORM_PERMISSIONS | {"students.manage", "theses.manage", "committees.manage"}
    )
    assert client.get("/api/v1/students/").status_code == 200
    assert client.get("/api/v1/theses/").status_code == 200
    assert client.get("/api/v1/committees/").status_code == 200
    assert client.get("/api/v1/dashboard/configuration/").status_code == 403


@pytest.mark.django_db
def test_aliases_are_central_and_do_not_convert_workflow_approval_to_manage():
    alias_permission = Permission.objects.create(
        code="thesis.view", name_ar="عرض رسالة قديم", name_en="Legacy thesis view"
    )
    workflow_permission = Permission.objects.create(
        code="committee.approve", name_ar="اعتماد لجنة", name_en="Approve committee"
    )
    role = Role.objects.create(
        name="LEGACY_COMPAT", name_ar="توافق قديم", name_en="Legacy compatibility"
    )
    role.permissions.add(alias_permission, workflow_permission)
    user = create_account("legacy_alias")
    user.roles.add(role)

    assert has_permission(user, "theses.view")
    assert has_permission(user, "thesis.view")
    assert has_permission(user, "committee.approve")
    assert not has_permission(user, "committees.manage")


@pytest.mark.django_db
def test_me_and_navigation_are_backend_permission_aware(client):
    vice_dean = create_account("vice_dean", User.Role.VICE_DEAN_POSTGRADUATE)
    call_command("seed_roles")
    client.force_authenticate(vice_dean)

    me = client.get("/api/v1/me/")
    dashboard = client.get("/api/v1/dashboard/")

    assert me.status_code == 200
    assert me.data["roles"] == ["VICE_DEAN_POSTGRADUATE"]
    assert me.data["can_manage_dashboard"] is False
    assert "dashboard.manage" not in me.data["permissions"]
    keys = {item["key"] for item in dashboard.data["ui"]["navigation"]}
    assert {"overview", "students", "theses", "committees"}.issubset(keys)
    assert "settings" not in keys
    assert "reports" not in keys
    action_ids = {item["id"] for item in dashboard.data["assistant"]["quick_actions"]}
    assert {"students", "theses", "committees", "pending"}.issubset(action_ids)
    assert "reports" not in action_ids


@pytest.mark.django_db
def test_vice_dean_pending_kpi_uses_director_approved_records_only(client):
    vice_dean = create_account("vice_dean", User.Role.VICE_DEAN_POSTGRADUATE)
    call_command("seed_roles")
    department = Department.objects.create(
        code="MED-KPI", name_ar="قسم الاختبار", name_en="Test Department"
    )
    statuses = ["DIRECTOR_APPROVED", "DIRECTOR_APPROVED", "UNDER_REVIEW"]
    theses = []
    for index, status in enumerate(statuses, start=1):
        student = Student.objects.create(
            university_id=f"KPI-{index}",
            name_ar=f"طالب {index}",
            department=department,
        )
        theses.append(
            Thesis.objects.create(student=student, title_ar=f"رسالة {index}", status=status)
        )
    DefenseCommittee.objects.create(thesis=theses[0], defense_date=date.today() + timedelta(days=7))
    client.force_authenticate(vice_dean)

    response = client.get("/api/v1/dashboard/")

    assert response.status_code == 200
    assert response.data["metrics"] == {
        "students": 3,
        "theses": 3,
        "defenses": 1,
        "pending": 2,
    }
    assert response.data["metric_definitions"]["pending"] == ("thesis.status = DIRECTOR_APPROVED")
    assert len(response.data["recent_students"]) == 3
    assert response.data["recent_students"][0]["university_id"] == "KPI-3"
    assert response.data["recent_students"][0]["thesis_status"] == "UNDER_REVIEW"


def test_react_dashboard_has_no_numeric_kpi_fallbacks():
    repo_root = Path(__file__).resolve().parents[4]
    sources = "\n".join(
        path.read_text(encoding="utf-8") for path in (repo_root / "web" / "src").rglob("*.jsx")
    )
    assert "fallbackCards" not in sources
    assert "value: 1240" not in sources
    assert "value: 386" not in sources


@pytest.mark.django_db
def test_demo_seed_is_gated_and_does_not_reset_existing_password(monkeypatch):
    existing = User.objects.create_user(
        username="ahmed",
        password="original-secret",  # noqa: S106 - test credential
    )
    monkeypatch.delenv("PGMS_SEED_DEMO", raising=False)
    monkeypatch.delenv("PGMS_DEMO_PASSWORD", raising=False)

    call_command("seed_demo")
    existing.refresh_from_db()
    assert existing.check_password("original-secret")

    monkeypatch.setenv("PGMS_SEED_DEMO", "true")
    monkeypatch.setenv("PGMS_DEMO_PASSWORD", "environment-secret")
    call_command("seed_demo")
    existing.refresh_from_db()
    assert existing.check_password("original-secret")
    assert set(existing.roles.values_list("name", flat=True)) == {
        "PLATFORM_ADMIN",
        "PROGRAM_DIRECTOR",
    }


@pytest.mark.django_db
def test_demo_seed_requires_environment_password_when_enabled(monkeypatch):
    monkeypatch.setenv("PGMS_SEED_DEMO", "true")
    monkeypatch.delenv("PGMS_DEMO_PASSWORD", raising=False)

    with pytest.raises((CommandError, RuntimeError)):
        call_command("seed_demo")
