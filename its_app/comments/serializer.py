from rest_framework.serializers import ModelSerializer
from its_app.comments.models import Comment


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'description', 'issue', 'author']
