from rest_framework.serializers import ModelSerializer
from its_app.issues.models import Issue


class IssueSerializer(ModelSerializer):
    class Meta:
        model = Issue
        fields = [
            'id', 'title', 'description', 'tag', 'priority',
            'status', 'assignee'
        ]
