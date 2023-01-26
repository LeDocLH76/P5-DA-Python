from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from its_app.users.views import (
    RegisterAPIView,
    UserListAPIView,
    UserLoginAPIView
)

urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name='token_obtain'),
    path("token/refresh/", TokenRefreshView.as_view(), name='token_refresh'),
    path("signup/", RegisterAPIView.as_view(), name='user_signup'),
    path('users/', UserListAPIView.as_view(), name='user_list'),
    path('login/', UserLoginAPIView.as_view(), name='user_login'),
]
