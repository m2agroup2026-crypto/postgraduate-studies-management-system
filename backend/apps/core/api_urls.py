from django.urls import include, path

from .api_views import AssistantView, DashboardView, MeView

urlpatterns = [
    path("me/", MeView.as_view(), name="me"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("assistant/", AssistantView.as_view(), name="assistant"),
    path("theses/", include("apps.theses.api.urls")),
]
