from django.contrib.auth.validators import UnicodeUsernameValidator

from rest_framework.serializers import (
    CharField, Serializer, ModelSerializer, SerializerMethodField)

from its_app.projects.models import Project
from its_app.users.models import MyUser


class ProjectSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type', 'users']


class UserSerializer(ModelSerializer):
    user_role = SerializerMethodField()

    def get_user_role(self, user):
        return user.contributor_set.get(project=self.context.id).role

    class Meta:
        model = MyUser
        fields = ['id', 'username', 'user_role']


class AddUserSerializer(Serializer):
    username_validator = UnicodeUsernameValidator()
    username = CharField(
        max_length=150,
        help_text=(
            """Required. 150 characters or fewer. Letters,
 digits and @/./+/-/_ only."""
        ),
        validators=[username_validator],
    )
