from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
# from rest_framework.viewsets import ModelViewSet
from its_app.users.serializers import UserSerializer


# class UserViewset(ModelViewSet):
#     queryset = get_user_model().objects.all()
#     serializer_class = UserSerializer
