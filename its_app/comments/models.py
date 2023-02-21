from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

from its_app.issues.models import Issue


class Comment(models.Model):
    description = models.TextField(blank=False, null=False)
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE
    )
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    created_time = models.DateTimeField(default=timezone.now)
