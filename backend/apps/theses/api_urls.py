from django.urls import path

from .api_views import ThesisActionView, ThesisCollectionView, ThesisDetailView

urlpatterns = [
    path("", ThesisCollectionView.as_view(), name="thesis-list"),
    path("<int:thesis_id>/", ThesisDetailView.as_view(), name="thesis-detail"),
    path("<int:thesis_id>/actions/", ThesisActionView.as_view(), name="thesis-action"),
]
