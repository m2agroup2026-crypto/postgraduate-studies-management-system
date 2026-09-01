from django.urls import path

from .api_views import AssistantView, DashboardView, MeView

urlpatterns = [
    path("me/", MeView.as_view(), name="me"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("assistant/", AssistantView.as_view(), name="assistant"),
]
