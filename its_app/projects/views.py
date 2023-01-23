# from rest_framework.decorators import api_view
# from rest_framework.response import Response
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework import authentication, permissions
from its_app.projects.models import Project
from its_app.projects.serializers import ProjectSerializer


class RetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    def get_queryset(self):
        return Project.objects.all()
    serializer_class = ProjectSerializer
    # authentication_classes = [
    #     authentication.SessionAuthentication,
    #     authentication.TokenAuthentication,
    # ]
    # permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        print('request = ', request)
        print('user = ', request.user)
        print('user.username = ', request.user.username)
        print('user.email = ', request.user.email)
        print('user.password = ', request.user.password)
        print('user.first_name = ', request.user.first_name)
        print('user.last_name = ', request.user.last_name)
        print('user.date_joined = ', request.user.date_joined)
        # print('user_all_permissions = ', request.user.get_all_permissions())
        print('args = ', args)
        print('kwargs = ', kwargs)
        # fait tout ce que tu souhaite ici
        return super().get(request, *args, **kwargs)


class ProjectListCreateAPIView(ListCreateAPIView):
    def get_queryset(self):
        return Project.objects.all()
    serializer_class = ProjectSerializer
    # authentication_classes = [
    #     authentication.SessionAuthentication,
    #     authentication.TokenAuthentication,
    # ]
    # permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # serializer.save(user=self.request.user)
        # print('serializer = ', serializer)
        # print('serializer.validated_data = ', serializer.validated_data)
        title = serializer.validated_data.get('title')
        type = serializer.validated_data.get('type')
        # title += " added before save"
        # type += " added before save"
        serializer.save(title=title, type=type)
        # return super().perform_create(serializer)


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
