from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator

from rest_framework import permissions, status
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_simplejwt.authentication import JWTAuthentication

from its_app.comments.models import Comment
from its_app.comments.permissions import IsCommentOwner
from its_app.comments.serializer import CommentSerializer
from its_app.issues.models import Issue
from its_app.issues.permissions import IsIssueOwnerOrAssignee
from its_app.projects.models import Project
from its_app.projects.permissions import IsProjectOwner


class CommentCreateReadAPIView(APIView):
    """
        Create one and read all issue comments
    """
    authentication_classes = [
        JWTAuthentication,
        SessionAuthentication,
    ]
    permission_classes = [permissions.IsAuthenticated]

    @method_decorator(permission_required(
        'projects.view_project',
        raise_exception=True
    ))
    def get(self, request, project_pk=None, issue_pk=None):
        """
            List issue comments
            Only issue owner and assignee can do it
        """
        project_obj = Project.objects.get_project(request, project_pk)
        if project_obj is None:
            return Response(
                'Project not found',
                status=status.HTTP_404_NOT_FOUND
            )
        issue_obj = Issue.objects.get_issue(request, project_obj, issue_pk)
        if issue_obj is None:
            return Response(
                'Issue not found',
                status=status.HTTP_404_NOT_FOUND
            )
        issue_comments = Comment.objects.filter(issue=issue_obj)

        serializer = CommentSerializer(issue_comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @method_decorator(permission_required(
        'projects.view_project',
        raise_exception=True
    ))
    def post(self, request, project_pk=None, issue_pk=None):
        """
            Create one comment on issue
            Only issue owner or assignee can do it
        """
        project_obj = Project.objects.get_project(request, project_pk)
        if project_obj is None:
            return Response(
                'Project not found',
                status=status.HTTP_404_NOT_FOUND
            )
        issue_obj = Issue.objects.get_issue(request, project_obj, issue_pk)
        if issue_obj is None:
            return Response(
                'Issue not found',
                status=status.HTTP_404_NOT_FOUND
            )
        data = request.data
        data['issue'] = issue_obj.pk
        data['author'] = request.user.pk
        serializer = CommentSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )


class CommentReadUpdateDeleteAPIView(APIView, IsCommentOwner):
    """
        Read update delete one comment
    """
    authentication_classes = [
        JWTAuthentication,
        SessionAuthentication,
    ]
    permission_classes = [
        permissions.IsAuthenticated
        &
        IsCommentOwner
    ]
    ...
