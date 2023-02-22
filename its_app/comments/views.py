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
from its_app.projects.models import Project


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

    @method_decorator(permission_required(
        'projects.view_project',
        raise_exception=True
    ))
    def get(self, request, project_pk=None, issue_pk=None, comment_pk=None):
        """
            List one comment detail
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
        comment_obj = Comment.objects.get_comment(request, comment_pk)
        if comment_obj is None:
            return Response(
                'Comment not found',
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = CommentSerializer(comment_obj)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @method_decorator(permission_required(
        'projects.view_project',
        raise_exception=True
    ))
    def put(self, request, project_pk=None, issue_pk=None, comment_pk=None):
        """
            Update one comment on issue
            Only comment owner can do it
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
        comment_obj = Comment.objects.get_comment(request, comment_pk)
        if comment_obj is None:
            return Response(
                'Comment not found',
                status=status.HTTP_404_NOT_FOUND
            )
        self.check_object_permissions(request, comment_obj)
        data = request.data
        data['issue'] = comment_obj.issue.pk
        data['author'] = comment_obj.author.pk
        serializer = CommentSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.update(comment_obj, serializer.validated_data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    @method_decorator(permission_required(
        'projects.view_project',
        raise_exception=True
    ))
    def delete(self, request, project_pk=None, issue_pk=None, comment_pk=None):
        """
            Delete one comment on issue
            Only comment owner can do it
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
        comment_obj = Comment.objects.get_comment(request, comment_pk)
        if comment_obj is None:
            return Response(
                'Comment not found',
                status=status.HTTP_404_NOT_FOUND
            )
        self.check_object_permissions(request, comment_obj)
        comment_obj.delete()
        return Response(
            'Comment succesfully deleted',
            status=status.HTTP_204_NO_CONTENT
        )
