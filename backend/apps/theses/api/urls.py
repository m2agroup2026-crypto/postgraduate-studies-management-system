from django.urls import path

from .views import ThesisSubmitView, ThesisReviewView


urlpatterns = [
    path(
        "<int:pk>/submit/",
        ThesisSubmitView.as_view(),
        name="thesis-submit",
    ),

    path(
        "<int:pk>/review/",
        ThesisReviewView.as_view(),
        name="thesis-review",
    ),
]
