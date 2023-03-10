from django.contrib.auth import get_user_model, login
from django.contrib.auth.models import Group

from rest_framework import permissions, status
from rest_framework.authentication import SessionAuthentication
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.response import Response

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from its_app.users.serializers import (
    UserSerializer,
    RegisterSerializer,
    LoginSerialiser
)


class RegisterAPIView(GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.create(serializer.data)
        group = Group.objects.get(name='BasicUsers')
        user.groups.add(group)
        response = {
            'message': 'User succesfully created',
            'data': {
                "id": user.pk,
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
            }
        }
        return Response(data=response, status=status.HTTP_201_CREATED)


class UserListAPIView(ListAPIView):
    authentication_classes = [
        JWTAuthentication,
        SessionAuthentication,
    ]
    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all().order_by('username')


class UserLoginAPIView(GenericAPIView):
    serializer_class = LoginSerialiser

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        tokens = self.get_tokens_for_user(user)
        login(request, user)
        return Response(
            data={
                'message': 'Bonjour, connection r??ussie',
                'access': tokens['access'],
                'refresh': tokens['refresh']
            },
            status=status.HTTP_200_OK
        )

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
