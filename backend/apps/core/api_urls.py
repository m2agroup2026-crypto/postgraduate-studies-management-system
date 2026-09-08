from django.urls import include, path

from .api_views import (
    AssistantView,
    DashboardConfigurationView,
    DashboardView,
    MeView,
)

urlpatterns = [
    path("me/", MeView.as_view(), name="me"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("dashboard/configuration/", DashboardConfigurationView.as_view(), name="dashboard-configuration"),
    path("assistant/", AssistantView.as_view(), name="assistant"),
    path("theses/", include("apps.theses.api.urls")),
]
