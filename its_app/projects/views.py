
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import Group
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404

from rest_framework import permissions, viewsets, status
from rest_framework.authentication import SessionAuthentication
from rest_framework.generics import (
    ListCreateAPIView, ListAPIView, CreateAPIView,
)
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_simplejwt.authentication import JWTAuthentication

from its_app.projects.models import Project, Contributor
from its_app.projects.serializers import ProjectSerializer, UserSerializer
from its_app.users.models import MyUser
from its_app.projects.permissions import IsProjectOwner


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
                'You are not project owner',
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
                'You are not project owner',
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
):  #
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

    def _get_project(self, request, pk):
        queryset = Project.objects.filter(
            users=request.user)
        project_obj = get_object_or_404(queryset, pk=pk)
        return project_obj

    def _check_user_role(self, user, project_obj):
        user_role = user.contributor_set.get(project=project_obj).role
        print('user role = ', user_role)
        print('Contributor.OWNER', Contributor.OWNER)
        if user_role != Contributor.OWNER:
            return False
        return True

    def _find_contributors(self, pk):
        project_contributors = [
            record.user
            for
            record in Contributor.objects.filter(project=pk)
        ]
        return project_contributors

    def get(self, request, project_pk=None, user_pk=None):
        print('project_pk = ', project_pk)
        project_obj = self._get_project(request, project_pk)
        self.check_object_permissions(request, project_obj)
        user = request.user
        if self._check_user_role(user, project_obj) is False:
            return Response(
                'You are not project owner',
                status=status.HTTP_403_FORBIDDEN
            )
        project_contributors = self._find_contributors(project_pk)
        print('contributors_users = ', project_contributors)
        serializer = UserSerializer(project_contributors, many=True)
        return Response(serializer.data)

    def post(self, request, project_pk=None, user_pk=None):
        project_obj = self._get_project(request, project_pk)
        user = request.user
        if self._check_user_role(user, project_obj) is False:
            return Response(
                'You are not project owner',
                status=status.HTTP_403_FORBIDDEN
            )
        print('project_obj = ', project_obj)
        print('request.data = ', request.data)
        username = request.data['username']
        print('username = ', username)
        user_obj = get_object_or_404(MyUser, username=username)
        print('user_obj =', user_obj)
        project_contributors = self._find_contributors(project_pk)
        if user_obj in project_contributors:
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
        project_obj = self._get_project(request, project_pk)
        user = request.user
        if self._check_user_role(user, project_obj) is False:
            return Response(
                'You are not project owner',
                status=status.HTTP_403_FORBIDDEN
            )
        user_to_remove = get_object_or_404(MyUser, pk=user_pk)
        print("user to remove = ", user_to_remove)
        if not user_to_remove:
            return Response(
                'User does not exist',
                status=status.HTTP_404_NOT_FOUND
            )
        project_contributors = self._find_contributors(project_pk)
        if user_to_remove not in project_contributors:
            return Response(
                'This user is not a contributor for this project',
                status=status.HTTP_404_NOT_FOUND
            )
        project_obj.users.remove(user_to_remove)
        return Response(
            'User succesfully removed',
            status=status.HTTP_204_NO_CONTENT
        )
