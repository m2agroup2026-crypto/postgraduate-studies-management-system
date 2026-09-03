from django.urls import path

from .views import ThesisSubmitView


urlpatterns = [
    path(
        "<int:pk>/submit/",
        ThesisSubmitView.as_view(),
        name="thesis-submit",
    ),
]
