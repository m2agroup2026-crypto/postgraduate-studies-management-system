from django.urls import path

from .api_views import StudentCollectionView, StudentDetailView

urlpatterns = [
    path("", StudentCollectionView.as_view(), name="student-list"),
    path("<int:student_id>/", StudentDetailView.as_view(), name="student-detail"),
]
