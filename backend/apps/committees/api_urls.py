from django.urls import path

from .api_views import CommitteeCollectionView, CommitteeDetailView, CommitteeScheduleView

urlpatterns = [
    path("", CommitteeCollectionView.as_view(), name="committee-collection"),
    path("<int:thesis_id>/", CommitteeDetailView.as_view(), name="committee-detail"),
    path("<int:thesis_id>/schedule/", CommitteeScheduleView.as_view(), name="committee-schedule"),
]
