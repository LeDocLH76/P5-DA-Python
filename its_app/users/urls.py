from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.routers import SimpleRouter
# from its_app.users.views import UserViewset

# router = SimpleRouter()
# router.register(r'users', UserViewset)

urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name='token_obtain'),
    path("token/refresh/", TokenRefreshView.as_view(), name='token_refresh'),
    # path("", include(router.urls)),
]
