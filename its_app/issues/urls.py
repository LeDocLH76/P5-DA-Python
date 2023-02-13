from django.urls import path
from its_app.issues.views import IssueCreateReadUpdateDeleteAPIView


urlpatterns = [
    path(
        "projects/<int:project_pk>/issues/",
        IssueCreateReadUpdateDeleteAPIView.as_view(),
        name='project_issues'
    ),
    path(
        "projects/<int:project_pk>/issues/<int:issue_pk>",
        IssueCreateReadUpdateDeleteAPIView.as_view(),
        name='project_issues_details'
    ),
]
