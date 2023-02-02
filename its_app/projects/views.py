
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404

from rest_framework import permissions, viewsets, status
from rest_framework.authentication import SessionAuthentication
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

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
        # return user.project_set.all()
        return Project.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        project_obj = serializer.save()
        project_obj.users.add(user)

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
#         print('user_all_permissions = ', request.user.get_all_permissions())
#         print('args = ', args)
#         print('kwargs = ', kwargs)
#         # fait tout ce que tu souhaite ici
#         return super().get(request, *args, **kwargs)
