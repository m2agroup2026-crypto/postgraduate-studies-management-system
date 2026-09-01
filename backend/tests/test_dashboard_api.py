import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from apps.accounts.models import User


@pytest.mark.django_db
def test_dashboard_requires_authentication():
    response = APIClient().get(reverse("dashboard"))
    assert response.status_code == 401


@pytest.mark.django_db
def test_arabic_is_default_and_dean_identity_is_exact():
    user = User.objects.create_user(username="dean", password="secret", role=User.Role.DEAN)
    client = APIClient()
    client.force_authenticate(user)
    response = client.get(reverse("dashboard"))
    assert response.status_code == 200
    assert response.data["identity"]["name"] == "الأستاذ الدكتور علاء عطية"
    assert user.preferred_language == "ar"
