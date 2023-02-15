from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404

from rest_framework import permissions, viewsets, status
from rest_framework.authentication import SessionAuthentication
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_simplejwt.authentication import JWTAuthentication

from its_app.projects.models import Project, Contributor
from its_app.projects.permissions import IsProjectOwner
from its_app.projects.serializers import (
    ProjectSerializer,
    UserSerializer,
    AddUserSerializer,
)


class ProjectRetrieveUpdateDestroyViewset(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [
        JWTAuthentication,
        SessionAuthentication,
    ]

    def _get_project(self, request, pk):
        queryset = Project.objects.filter(
            users=request.user)
        # print('QS = ', queryset)
        project = get_object_or_404(queryset, pk=pk)
        return project

    def _check_user_role(self, user, project_obj):
        user_role = user.contributor_set.get(project=project_obj).role
        print('user role = ', user_role)
        print('Contributor.OWNER', Contributor.OWNER)
        if user_role != Contributor.OWNER:
            return False
        return True

    @method_decorator(permission_required(
        'projects.view_project',
        raise_exception=True
    ))
    def retrieve(self, request, pk=None):
        project_obj = self._get_project(request, pk)
        serializer = ProjectSerializer(project_obj)
        return Response(serializer.data)

    @method_decorator(permission_required(
        [
            'projects.change_project',
        ],
        raise_exception=True
    ))
    def update(self, request, pk=None):
        user = self.request.user
        project_obj = self._get_project(request, pk)
        if self._check_user_role(user, project_obj) is False:
            return Response(
                'Should never appear - You are not project owner',
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = ProjectSerializer(project_obj, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @method_decorator(permission_required(
        [
            'projects.delete_project',
        ],
        raise_exception=True
    ))
    def delete(self, request, pk=None):
        user = self.request.user
        project_obj = self._get_project(request, pk)
        if self._check_user_role(user, project_obj) is False:
            return Response(
                'Should never appear - You are not project owner',
                status=status.HTTP_403_FORBIDDEN
            )
        project_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProjectListCreateAPIView(PermissionRequiredMixin, ListCreateAPIView):
    authentication_classes = [
        JWTAuthentication,
        SessionAuthentication,
    ]
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    permission_required = (
        'projects.add_project',
        'projects.view_project',
    )
    serializer_class = ProjectSerializer

    def get_queryset(self):
        print('user = ', self.request.user)
        print('user user_permissions = ',
              self.request.user.get_user_permissions())
        print('user group_permissions = ',
              self.request.user.get_group_permissions())
        queryset = Project.objects.filter(
            users=self.request.user)
        return queryset

    def perform_create(self, serializer):
        user = self.request.user
        project_obj = serializer.save()
        project_obj.users.add(
            user,
            through_defaults={'role': Contributor.OWNER}
        )
        group = Group.objects.get(name='ProjectOwner')
        user.groups.add(group)
        user_contributor = user.contributor_set.get(project=project_obj)
        print('Name of project = ', project_obj.title)
        print('User = ', user)
        print('user role = ', user_contributor.role)


class ContributorCreateReadDeleteAPIView(
    PermissionRequiredMixin, APIView, IsProjectOwner
):
    authentication_classes = [
        JWTAuthentication,
        SessionAuthentication,
    ]
    permission_classes = [
        permissions.IsAuthenticated
        &
        IsProjectOwner,
    ]
    permission_required = (
        'projects.view_project',
        'projects.add_project',
        'projects.delete_project',
    )

    def get(self, request, project_pk=None, user_pk=None):
        project_obj = Project.get_project(request, project_pk)
        if project_obj is None:
            return Response(
                'Project not found',
                status=status.HTTP_404_NOT_FOUND
            )
        self.check_object_permissions(request, project_obj)
        project_contributors = project_obj.get_contributors
        serializer = UserSerializer(project_contributors, many=True)
        return Response(serializer.data)

    def post(self, request, project_pk=None, user_pk=None):
        project_obj = Project.get_project(request, project_pk)
        if project_obj is None:
            return Response(
                'Project not found',
                status=status.HTTP_404_NOT_FOUND
            )
        self.check_object_permissions(request, project_obj)
        serializer = AddUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        user_obj = get_user_model().get_user(username=username)
        if user_obj is None:
            return Response(
                'User does not exist',
                status=status.HTTP_404_NOT_FOUND
            )
        if user_obj in project_obj.get_contributors:
            return Response(
                'This user is already added',
                status=status.HTTP_400_BAD_REQUEST
            )
        project_obj.users.add(
            user_obj,
            through_defaults={'role': Contributor.CONTRIBUTOR}
        )
        return Response(
            'User succesfully added',
            status=status.HTTP_201_CREATED
        )

    def delete(self, request, project_pk=None, user_pk=None):
        project_obj = Project.get_project(request, project_pk)
        if project_obj is None:
            return Response(
                'Project not found',
                status=status.HTTP_404_NOT_FOUND
            )
        self.check_object_permissions(request, project_obj)
        user_to_remove = get_user_model().get_user(user_pk=user_pk)
        if user_to_remove is None:
            return Response(
                'User does not exist',
                status=status.HTTP_404_NOT_FOUND
            )
        if user_to_remove not in project_obj.get_contributors:
            return Response(
                'This user is not a contributor for this project',
                status=status.HTTP_404_NOT_FOUND
            )
        project_obj.users.remove(user_to_remove)
        return Response(
            'User succesfully removed',
            status=status.HTTP_204_NO_CONTENT
        )
