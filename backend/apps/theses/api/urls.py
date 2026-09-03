from django.urls import path

from .views import ThesisSubmitView, ThesisReviewView, ThesisApproveView


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

    path(
        "<int:pk>/approve/",
        ThesisApproveView.as_view(),
        name="thesis-approve",
    ),
]
