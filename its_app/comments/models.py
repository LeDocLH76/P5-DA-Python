from django.db import models
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.utils import timezone

from its_app.issues.models import Issue


class CommentManager(models.Manager):
    def get_comment(self, request, comment_pk=None):
        """
            Return one comment if request.user is owner on it,
            None for other cases.
        """
        if comment_pk:
            try:
                comment_obj = self.get(author=request.user, pk=comment_pk)
            except Comment.DoesNotExist:
                comment_obj = None
            return comment_obj
        return None


class Comment(models.Model):
    description = models.TextField(blank=False, null=False)
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE
    )
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    created_time = models.DateTimeField(default=timezone.now)

    objects = CommentManager()
