from django.db import models
from its_app.users.models import MyUser


class Project(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=1024)
    type = models.CharField(max_length=255)
    users = models.ManyToManyField(
        MyUser,
        through='Contributor',
        # through_fields=('project_id', 'user_id')
    )
