from django.urls import path

from .api_views import DocumentCollectionView


urlpatterns = [
    path(
        "",
        DocumentCollectionView.as_view(),
        name="documents-collection",
    ),
]
