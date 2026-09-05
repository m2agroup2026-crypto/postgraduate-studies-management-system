from django.urls import path

from .views import (
    ThesisSubmitView,
    ThesisReviewView,
    ThesisDirectorApproveView,
    ThesisViceDeanApproveView,
    ThesisDeanApproveView,
    ThesisFinalApproveView,
)


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
        "<int:pk>/director-approve/",
        ThesisDirectorApproveView.as_view(),
        name="thesis-director-approve",
    ),

    path(
        "<int:pk>/vice-dean-approve/",
        ThesisViceDeanApproveView.as_view(),
        name="thesis-vice-dean-approve",
    ),

    path(
        "<int:pk>/dean-approve/",
        ThesisDeanApproveView.as_view(),
        name="thesis-dean-approve",
    ),

    path(
        "<int:pk>/final-approve/",
        ThesisFinalApproveView.as_view(),
        name="thesis-final-approve",
    ),
]
