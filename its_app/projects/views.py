
# from rest_framework.decorators import api_view
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator

from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from rest_framework import permissions, viewsets, status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.generics import (
    ListCreateAPIView,
    # RetrieveUpdateDestroyAPIView,
)
from its_app.projects.models import Project
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
        queryset = Project.objects.all()
        project = get_object_or_404(queryset, pk=pk)
        serializer = ProjectSerializer(project)
        return Response(serializer.data)

    @method_decorator(permission_required(
        [
            'projects.view_project',
            'projects.change_project',
            'projects.delete_project',
        ],
        raise_exception=True
    ))
    def update(self, request, pk=None):
        queryset = Project.objects.all()
        project_obj = get_object_or_404(queryset, pk=pk)
        serializer = ProjectSerializer(project_obj, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @method_decorator(permission_required(
        [
            'projects.view_project',
            'projects.change_project',
            'projects.delete_project',
        ],
        raise_exception=True
    ))
    def delete(self, request, pk=None):
        queryset = Project.objects.all()
        project = get_object_or_404(queryset, pk=pk)
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# class RetrieveUpdateDestroyAPIView(
#     PermissionRequiredMixin,
#     RetrieveUpdateDestroyAPIView
# ):

#     permission_required = (
#         'projects.change_project',
#         'projects.delete_project',
#         'projects.view_project',
#     )

#     permission_classes = [permissions.IsAuthenticated]

#     authentication_classes = [
#         JWTAuthentication,
#         SessionAuthentication,
#     ]

#     def get_queryset(self):
#         # user = self.request.user
#         # return user.project_set.all()
#         return Project.objects.all()

#     serializer_class = ProjectSerializer

#     def get(self, request, *args, **kwargs):
#         print('request = ', request)
#         print('user = ', request.user)
#         print('user.username = ', request.user.username)
#         print('user.email = ', request.user.email)
#         print('user.password = ', request.user.password)
#         print('user.first_name = ', request.user.first_name)
#         print('user.last_name = ', request.user.last_name)
#         print('user.date_joined = ', request.user.date_joined)
#         # print('user_all_permissions = ', request.user.get_all_permissions())
#         print('args = ', args)
#         print('kwargs = ', kwargs)
#         # fait tout ce que tu souhaite ici
#         return super().get(request, *args, **kwargs)


class ProjectListCreateAPIView(PermissionRequiredMixin, ListCreateAPIView):
    # class ProjectListCreateAPIView(ListCreateAPIView):

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

    def get_queryset(self):
        print('user = ', self.request.user)
        print('user user_permissions = ',
              self.request.user.get_user_permissions())
        print('user group_permissions = ',
              self.request.user.get_group_permissions())
        print('user all_perms = ', self.request.user.get_all_permissions())
        user = self.request.user
        print('has_perm add = ', user.has_perm('projects.add_project'))
        print('has_perm change = ', user.has_perm('projects.change_project'))
        print('has_perm delete = ', user.has_perm('projects.delete_project'))
        print('has_perm view = ', user.has_perm('projects.view_project'))
        # return user.project_set.all()
        return Project.objects.all()

    serializer_class = ProjectSerializer

    def perform_create(self, serializer):
        print('user = ', self.request.user)
        user = self.request.user
        project_obj = serializer.save()
        print('project obj = ', project_obj)
        project_obj.users.add(user)


# @api_view(['GET', 'POST'])
# def project_list_or_create(request, *args, **kwargs):
#     if request.method == 'GET':
#         instance = Project.objects.all().last()
#         data = {}
#         if instance:
#             data = ProjectSerializer(instance).data
#         return Response(data)
#     elif request.method == 'POST':
#         serialiser = ProjectSerializer(data=request.data)
#         if serialiser.is_valid(raise_exception=True):
#             data = serialiser.data
#             print('data in = ', data)
#             return Response(data)
#         return Response({"invalid": "not good data"}, status=400)
