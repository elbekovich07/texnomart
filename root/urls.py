from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from rest_framework_simplejwt.views import TokenRefreshView

from app.custom_oauth_token import (
    CustomAuthToken,
    LogoutAPIView,
    LoginAPIView,
    LogoutView
)
from root import settings

urlpatterns = [
    path("admin/", admin.site.urls),
                  path("", include("app.urls")),
                  path("api-auth/", include("rest_framework.urls")),

                  # JWT Authentication
                  path("api/jwt-login/", LoginAPIView.as_view(), name="jwt_login"),
                  path("api/jwt-logout/", LogoutView.as_view(), name="jwt_logout"),
                  path("api/token-refresh/", TokenRefreshView.as_view(), name="token_refresh"),

                  # DRF TokenAuthentication
                  path("api/token-login/", CustomAuthToken.as_view(), name="token_login"),
                  path("api/token-logout/", LogoutAPIView.as_view(), name="token_logout"),

                  # Swagger & ReDoc
                  path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
                  path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
                  path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Debug toolbar
urlpatterns += debug_toolbar_urls()
