from rest_framework.serializers import ModelSerializer
from its_app.projects.models import Project


class ProjectSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type']
