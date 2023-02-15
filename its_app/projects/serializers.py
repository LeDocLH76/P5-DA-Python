from django.contrib.auth.validators import UnicodeUsernameValidator

from rest_framework.serializers import CharField, Serializer, ModelSerializer

from its_app.projects.models import Project
from its_app.users.models import MyUser


class ProjectSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type', 'users']


class UserSerializer(ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['id', 'username']


class AddUserSerializer(Serializer):
    username_validator = UnicodeUsernameValidator()
    username = CharField(
        max_length=150,
        help_text=(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
    )
