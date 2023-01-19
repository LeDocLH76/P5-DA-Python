from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token

from its_app.users.serializers import UserSignupSerializer, UserLoginSerializer


@api_view(['POST'])
def user_create(request, *args, **kwargs):

    serialiser = UserSignupSerializer(data=request.data)
    if serialiser.is_valid(raise_exception=True):
        data = serialiser.data
        print('data in = ', data)
        user = get_user_model().objects.create_user(**data)
        print('user = ', user)
        token, created = Token.objects.get_or_create(user=user)
        print('token = ', token)
        data['token'] = token.key
        print('data out = ', data)
        return Response(data)
    return Response({"invalid": "not good data"}, status=400)


@api_view(['POST'])
def user_login(request, *args, **kwargs):
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        data = serializer.data
        user = data['username'].lower()
        password = data['password']
        print('data in = ', data)
        print('user = ', user)
        print('password = ', password)

        user = get_object_or_404(get_user_model(), username=user)
        print('user obj = ', user)
        print('user.username = ', user.username)
        print('user.email = ', user.email)
        print('user.password = ', user.password)
        print('user.first_name = ', user.first_name)
        print('user.last_name = ', user.last_name)
        print('user.date_joined = ', user.date_joined)

        return Response(data)
