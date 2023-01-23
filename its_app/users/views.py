from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from its_app.users.serializers import UserSignupSerializer, UserLoginSerializer
