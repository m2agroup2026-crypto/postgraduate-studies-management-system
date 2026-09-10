import pytest
from rest_framework.test import APIClient

from apps.accounts.models import User
from apps.core.models import DashboardMetricCard, DashboardNavigationItem, Permission, Role


@pytest.fixture
def client():
    return APIClient()


def create_test_user(username, role):
    user = User.objects.create(username=username, role=role)
    user.set_unusable_password()
    user.save(update_fields=["password"])
    return user


@pytest.fixture
def manager(db):
    user = create_test_user(
        username="dashboard_manager",
        role=User.Role.POSTGRADUATE_DIRECTOR,
    )
    permission = Permission.objects.create(
        code="dashboard.manage",
        name_ar="إدارة المنصة",
        name_en="Manage platform",
    )
    role = Role.objects.create(
        name="PLATFORM_ADMIN",
        name_ar="مدير المنصة",
        name_en="Platform administrator",
    )
    role.permissions.add(permission)
    user.roles.add(role)
    return user


@pytest.fixture
def academic_director(db):
    return create_test_user(
        username="academic_director",
        role=User.Role.POSTGRADUATE_DIRECTOR,
    )


@pytest.fixture
def regular_user(db):
    return create_test_user(
        username="dashboard_reader",
        role=User.Role.STUDENT,
    )


@pytest.mark.django_db
def test_regular_user_cannot_manage_dashboard_configuration(client, regular_user):
    client.force_authenticate(regular_user)

    response = client.get("/api/v1/dashboard/configuration/")

    assert response.status_code == 403


@pytest.mark.django_db
def test_academic_director_cannot_manage_platform_configuration(client, academic_director):
    client.force_authenticate(academic_director)

    response = client.get("/api/v1/dashboard/configuration/")

    assert response.status_code == 403


@pytest.mark.django_db
def test_manager_can_update_dashboard_configuration(client, manager):
    client.force_authenticate(manager)
    navigation = list(
        DashboardNavigationItem.objects.values(
            "key",
            "label_ar",
            "label_en",
            "route",
            "icon",
            "required_permission",
            "sort_order",
            "is_active",
        )
    )
    metrics = list(
        DashboardMetricCard.objects.values(
            "key",
            "label_ar",
            "label_en",
            "icon",
            "sort_order",
            "is_active",
        )
    )

    overview = next(item for item in navigation if item["key"] == "overview")
    overview["label_ar"] = "لوحة القيادة"
    overview["sort_order"] = 5

    students = next(item for item in metrics if item["key"] == "students")
    students["label_ar"] = "إجمالي الطلاب"

    response = client.patch(
        "/api/v1/dashboard/configuration/",
        {"navigation": navigation, "metrics": metrics},
        format="json",
    )

    assert response.status_code == 200
    assert DashboardNavigationItem.objects.get(key="overview").label_ar == "لوحة القيادة"
    assert DashboardNavigationItem.objects.get(key="overview").sort_order == 5
    assert DashboardMetricCard.objects.get(key="students").label_ar == "إجمالي الطلاب"


@pytest.mark.django_db
def test_settings_navigation_is_hidden_from_regular_users(client, regular_user):
    client.force_authenticate(regular_user)

    response = client.get("/api/v1/dashboard/")

    assert response.status_code == 200
    keys = [item["key"] for item in response.data["ui"]["navigation"]]
    assert "settings" not in keys


@pytest.mark.django_db
def test_manager_receives_configurable_metric_metadata(client, manager):
    client.force_authenticate(manager)

    response = client.get("/api/v1/dashboard/")

    assert response.status_code == 200
    metric_keys = [item["key"] for item in response.data["ui"]["metrics"]]
    assert metric_keys == ["students", "theses", "defenses", "pending"]
