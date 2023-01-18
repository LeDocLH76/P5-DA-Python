from django.urls import path, include
# from rest_framework import routers

# from its_app.projects.views import ProjectViewset
# from its_app.projects.views import project_list_or_create
from its_app.projects.views import (
    RetrieveUpdateDestroyAPIView,
    ProjectListCreateAPIView
)


# router = routers.SimpleRouter()

# router.register("projects", ProjectViewset, basename='projects')


urlpatterns = [
    # path("", include(router.urls)),
    # path("projects/", project_list_or_create, name='projects'),
    path(
        "projects/<int:pk>/",
        RetrieveUpdateDestroyAPIView.as_view(),
        name='projects_detail_update_delete'
    ),
    path(
        "projects/",
        ProjectListCreateAPIView.as_view(),
        name='projects_list_create'
    ),
]
