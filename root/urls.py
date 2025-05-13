from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from app.custom_oauth_token import CustomAuthToken, LogoutAPIView, LogoutView, LoginAPIView
from root import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('app.urls')),
    path('api-auth/', include('rest_framework.urls')),
                  path('api-token-auth/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
                  path('api-token-refresh/', TokenRefreshView.as_view(), name='token_refresh'),
                  # DRF TokenAuthentication
                  path('api/token-login/', CustomAuthToken.as_view(), name='token_login'),
                  path('api/token-logout/', LogoutAPIView.as_view(), name='token_logout'),

                  # JWT Authentication
                  path('api/jwt-login/', LoginAPIView.as_view(), name='jwt_login'),
                  path('api/jwt-logout/', LogoutView.as_view(), name='jwt_logout'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += debug_toolbar_urls()
