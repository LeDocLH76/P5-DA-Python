from django.urls import path
from its_app.comments.views import (
    CommentCreateReadAPIView,
    CommentReadUpdateDeleteAPIView
)


urlpatterns = [
    path(
        "projects/<int:project_pk>/issues/<int:issue_pk>/comments/",
        CommentCreateReadAPIView.as_view(),
        name='project_issue_comments'
    ),
    path(
        "projects/<int:project_pk>/issues/<int:issue_pk>/comments/<int:comment_pk>",
        CommentReadUpdateDeleteAPIView.as_view(),
        name='project_issue_comment_details'
    ),
]
