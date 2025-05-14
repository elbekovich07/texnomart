from django.urls import path, include
from rest_framework.routers import DefaultRouter

from app.views import *

router = DefaultRouter()
router.register('category', CategoryViewSet, basename='category')
router.register('product', ProductViewSet, basename='product')
router.register('liked', LikedViewSet, basename='liked')
router.register('favorite', FavoriteViewSet, basename='favorite'),
router.register('comment', CommentViewSet, basename='comment'),
router.register('cart', CartViewSet, basename='cart'),
router.register('cart-item', CartItemViewSet, basename='cart-item'),

urlpatterns = [
    path('', include(router.urls)),
    # Users
    path('auth/register/', UserRegisterJWTView.as_view(), name='jwt_register'),
    path('auth/me/', UserMeView.as_view(), name='user_me'),
    path('auth/update/', UserUpdateView.as_view(), name='user_update'),
]
