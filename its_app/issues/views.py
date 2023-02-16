
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.decorators import method_decorator

from rest_framework import permissions, status
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_simplejwt.authentication import JWTAuthentication

from its_app.issues.models import Issue
from its_app.issues.permissions import IsIssueOwner
from its_app.issues.serializer import IssueSerializer
from its_app.projects.models import Project
from its_app.projects.permissions import IsProjectOwner


class IssueCreateReadUpdateDeleteAPIView(APIView, IsIssueOwner):
    authentication_classes = [
        JWTAuthentication,
        SessionAuthentication,
    ]
    permission_classes = [
        permissions.IsAuthenticated
        &
        IsIssueOwner
    ]

    def _get_assignee(self, data, author_obj):
        try:
            assignee_pk = data.pop('assignee')
            assignee_obj = get_user_model().get_user(user_pk=assignee_pk)
            if assignee_obj is None:
                # not exist
                return None
        except KeyError:
            # by default
            assignee_obj = author_obj
        return assignee_obj

    @method_decorator(permission_required(
        'projects.view_project',
        raise_exception=True
    ))
    def get(self, request, project_pk=None, issue_pk=None):
        """
            List project issues
            Only contributors can do it
        """
        project_obj = Project.get_project(request, project_pk)
        if project_obj is None:
            return Response(
                'Project not found',
                status=status.HTTP_404_NOT_FOUND
            )
        project_issues = Issue.objects.filter(project=project_pk)
        serializer = IssueSerializer(project_issues, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @method_decorator(permission_required(
        'projects.change_project',
        raise_exception=True
    ))
    def post(self, request, project_pk=None, issue_pk=None):
        """
            Add project issue
            Only project owner can do it
        """
        author_obj = request.user
        project_obj = Project.get_project(request, project_pk)
        if project_obj is None:
            return Response(
                'Project not found',
                status=status.HTTP_404_NOT_FOUND
            )
        # Must be project owner to continue
        instance = IsProjectOwner()
        perm = instance.has_object_permission(request, self, project_obj)
        if perm is False:
            return Response(
                'You are not project owner for this project',
                status=status.HTTP_403_FORBIDDEN
            )
        data = request.data.copy()
        assignee_obj = self._get_assignee(data, author_obj)
        if assignee_obj is None:
            return Response(
                'User to assign not found',
                status=status.HTTP_404_NOT_FOUND
            )
        if assignee_obj not in project_obj.get_contributors:
            return Response(
                'User to assign must be contributor before',
                status=status.HTTP_400_BAD_REQUEST
            )

        data['assignee'] = assignee_obj.pk
        serializer = IssueSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(
            project=project_obj,
            author=author_obj,
        )
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    @method_decorator(permission_required(
        'projects.change_project',
        raise_exception=True
    ))
    def put(self, request, project_pk=None, issue_pk=None):
        """
            Update project issue
            Only issue owner can do it
        """
        author_obj = request.user
        project_obj = Project.get_project(request, project_pk)
        if project_obj is None:
            return Response(
                'Project not found',
                status=status.HTTP_404_NOT_FOUND
            )
        issue_obj = Issue.get_issue(request, project_obj, issue_pk)
        if issue_obj is None:
            return Response(
                'Issue not found',
                status=status.HTTP_404_NOT_FOUND
            )
        self.check_object_permissions(request, issue_obj)
        data = request.data.copy()
        assignee_obj = self._get_assignee(data, author_obj)
        if assignee_obj is None:
            return Response(
                'User to assign not found',
                status=status.HTTP_404_NOT_FOUND
            )
        if assignee_obj not in project_obj.get_contributors:
            return Response(
                'User to assign must be contributor before',
                status=status.HTTP_400_BAD_REQUEST
            )
        data['assignee'] = assignee_obj.pk
        serializer = IssueSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        data['assignee'] = assignee_obj
        serializer.update(issue_obj, data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    @method_decorator(permission_required(
        'projects.change_project',
        raise_exception=True
    ))
    def delete(self, request, project_pk=None, issue_pk=None):
        """
            Delete project issue
            Only issue owner can do it
        """
        project_obj = Project.get_project(request, project_pk)
        if project_obj is None:
            return Response(
                'Project not found',
                status=status.HTTP_404_NOT_FOUND
            )
        issue_obj = Issue.get_issue(request, project_obj, issue_pk)
        if issue_obj is None:
            return Response(
                'Issue not found',
                status=status.HTTP_404_NOT_FOUND
            )
        self.check_object_permissions(request, issue_obj)
        issue_obj.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )
