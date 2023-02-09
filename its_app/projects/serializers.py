from rest_framework.serializers import ModelSerializer
from its_app.projects.models import Project
from its_app.users.models import MyUser


class ProjectSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type', 'users']


class UserSerializer(ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['id','username']
