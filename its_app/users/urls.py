from django.urls import path

from its_app.users.views import user_create, user_login

urlpatterns = [
    # path("login/", obtain_auth_token, name='user_login')
    path("login/", user_login, name='user_login'),
    path("signup/", user_create, name='user_create')
]
