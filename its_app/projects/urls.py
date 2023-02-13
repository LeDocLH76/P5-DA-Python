from django.urls import path, include
from rest_framework import routers
from its_app.projects.views import ProjectRetrieveUpdateDestroyViewset
from its_app.projects.views import (
    ContributorCreateReadDeleteAPIView,
    ProjectListCreateAPIView,
)

router = routers.SimpleRouter()
router.register(
    r"projects", ProjectRetrieveUpdateDestroyViewset, basename='project'
)

urlpatterns = [
    path("", include(router.urls)),
    path(
        "projects/",
        ProjectListCreateAPIView.as_view(),
        name='projects_list_create'
    ),
    path(
        "projects/<int:project_pk>/users/",
        ContributorCreateReadDeleteAPIView.as_view(),
        name='project_users'
    ),
    path(
        "projects/<int:project_pk>/users/<int:user_pk>",
        ContributorCreateReadDeleteAPIView.as_view(),
        name='project_users_details'
    ),
]
