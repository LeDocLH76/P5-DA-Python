from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.utils.decorators import method_decorator

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


class ProjectRetrieveUpdateDestroyViewset(viewsets.ViewSet, IsProjectOwner):
    permission_classes = [
        permissions.IsAuthenticated
        &
        IsProjectOwner
    ]
    authentication_classes = [
        JWTAuthentication,
        SessionAuthentication,
    ]

    @method_decorator(permission_required(
        'projects.view_project',
        raise_exception=True
    ))
    def retrieve(self, request, pk=None):
        project_obj = Project.get_project(request, pk)
        if project_obj is None:
            return Response(
                'Project not found',
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = ProjectSerializer(project_obj)
        return Response(serializer.data)

    @method_decorator(permission_required(
        [
            'projects.change_project',
        ],
        raise_exception=True
    ))
    def update(self, request, pk=None):
        project_obj = Project.get_project(request, pk)
        if project_obj is None:
            return Response(
                'Project not found',
                status=status.HTTP_404_NOT_FOUND
            )
        self.check_object_permissions(request, project_obj)
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
        project_obj = Project.get_project(request, pk)
        if project_obj is None:
            return Response(
                'Project not found',
                status=status.HTTP_404_NOT_FOUND
            )
        self.check_object_permissions(request, project_obj)
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
        serializer = UserSerializer(project_obj.get_contributors, many=True)
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
                'User is already added',
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
                'User is not a contributor for this project',
                status=status.HTTP_404_NOT_FOUND
            )
        project_obj.users.remove(user_to_remove)
        return Response(
            'User succesfully removed',
            status=status.HTTP_204_NO_CONTENT
        )
