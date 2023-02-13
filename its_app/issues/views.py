
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import PermissionRequiredMixin

from django.shortcuts import get_object_or_404

from rest_framework import permissions, status
from rest_framework.authentication import SessionAuthentication

from rest_framework.response import Response

from rest_framework.views import APIView

from rest_framework_simplejwt.authentication import JWTAuthentication

from its_app.issues.models import Issue
from its_app.issues.permissions import IsIssueOwner
from its_app.issues.serializer import IssueSerializer
from its_app.projects.models import Project


class IssueCreateReadUpdateDeleteAPIView(
    PermissionRequiredMixin, APIView, IsIssueOwner
):
    authentication_classes = [
        JWTAuthentication,
        SessionAuthentication,
    ]
    permission_classes = [
        permissions.IsAuthenticated
        &
        IsIssueOwner
    ]
    permission_required = (
        'projects.view_project',
        'projects.add_project',
    )

    def _get_project(self, request, pk):
        queryset = Project.objects.filter(
            users=request.user)
        project_obj = get_object_or_404(queryset, pk=pk)
        return project_obj

    def _get_user(self, user_pk):
        queryset = get_user_model().objects.all()
        user = get_object_or_404(queryset, pk=user_pk)
        return user

    def _get_issue(self, author_obj, project_obj, issue_pk):
        queryset = Issue.objects.filter(
            project=project_obj.pk,
            author=author_obj.pk
        )
        issue_obj = get_object_or_404(queryset, pk=issue_pk)
        return issue_obj

    def _fill_assignee(self, data, author):
        try:
            assignee_pk = data.pop('assignee')
            assignee = self._get_user(assignee_pk)
        except KeyError:
            assignee = author
        data['assignee'] = assignee.pk
        return data

    def get(self, request, project_pk=None, issue_pk=None):
        self._get_project(request, project_pk)
        project_issues = Issue.objects.filter(project=project_pk)
        serializer = IssueSerializer(project_issues, many=True)
        return Response(serializer.data)

    def post(self, request, project_pk=None, issue_pk=None):
        project_obj = self._get_project(request, project_pk)
        author_obj = request.user
        data = request.data.copy()
        data = self._fill_assignee(data, author_obj)
        serializer = IssueSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(
            project=project_obj,
            author=author_obj,
            assignee=author_obj
        )
        return Response(
            'Issue succesfully created',
            status=status.HTTP_201_CREATED
        )

    def put(self, request, project_pk=None, issue_pk=None):
        project_obj = self._get_project(request, project_pk)
        author_obj = request.user
        issue_obj = self._get_issue(author_obj, project_obj, issue_pk)
        self.check_object_permissions(request, issue_obj)
        data = request.data.copy()
        data = self._fill_assignee(data, author_obj)
        serializer = IssueSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        assignee_pk = data['assignee']
        assignee_obj = self._get_user(assignee_pk)
        data['assignee'] = assignee_obj
        serializer.update(issue_obj, data)
        return Response(
            'Issue succesfully updated',
            status=status.HTTP_201_CREATED
        )

    def delete(self, request, project_pk=None, issue_pk=None):
        project_obj = self._get_project(request, project_pk)
        author_obj = request.user
        issue_obj = self._get_issue(author_obj, project_obj, issue_pk)
        self.check_object_permissions(request, issue_obj)
        issue_obj.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )
