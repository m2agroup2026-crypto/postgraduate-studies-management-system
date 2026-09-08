from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/auth/token/", TokenObtainPairView.as_view(), name="token"),
    path("api/v1/auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/v1/students/", include("apps.students.api_urls")),
    path("api/v1/theses/", include("apps.theses.api_urls")),
    path("api/v1/committees/", include("apps.committees.api_urls")),
    path("api/v1/", include("apps.core.api_urls")),
    path("health/", include("apps.core.urls")),
]
