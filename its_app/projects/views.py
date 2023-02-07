
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import Group
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404

from rest_framework import permissions, viewsets, status
from rest_framework.authentication import SessionAuthentication
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from its_app.projects.models import Project, Contributor
from its_app.projects.serializers import ProjectSerializer


class RetrieveUpdateDestroyViewset(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [
        JWTAuthentication,
        SessionAuthentication,
    ]

    @method_decorator(permission_required(
        'projects.view_project',
        raise_exception=True
    ))
    def retrieve(self, request, pk=None):
        queryset = Project.objects.filter(
            users=request.user)
        project = get_object_or_404(queryset, pk=pk)
        serializer = ProjectSerializer(project)
        return Response(serializer.data)

    @method_decorator(permission_required(
        [
            'projects.change_project',
        ],
        raise_exception=True
    ))
    def update(self, request, pk=None):
        user = self.request.user
        queryset = Project.objects.filter(
            users=request.user)
        project_obj = get_object_or_404(queryset, pk=pk)
        user_contributor = user.contributor_set.get(project=project_obj)
        user_role = user_contributor.role
        if user_role != Contributor.OWNER:
            return Response(
                data='You are not project owner',
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
        queryset = Project.objects.filter(
            users=request.user)
        project_obj = get_object_or_404(queryset, pk=pk)
        user_contributor = user.contributor_set.get(project=project_obj)
        user_role = user_contributor.role
        if user_role != Contributor.OWNER:
            return Response(
                data='You are not project owner',
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
        # return user.project_set.all() Dont use this
        # Use filter is owner or is contributor
        queryset = Project.objects.filter(
            users=self.request.user)
        return queryset

    def perform_create(self, serializer):
        user = self.request.user
        project_obj = serializer.save()
        # Add owner in serializer
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
