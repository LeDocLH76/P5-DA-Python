from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# from its_app.users.views import user_create, user_login

urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name='token_obtain'),
    path("token/refresh/", TokenRefreshView.as_view(), name='token_refresh'),
    # path("login/", user_login, name='user_login'),
    # path("signup/", user_create, name='user_create')
]
