from django.db import models
from django.contrib.auth import get_user_model


class Contributor(models.Model):
    user_id = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    project_id = models.ForeignKey('Project', on_delete=models.CASCADE)
    role = models.CharField(max_length=20)


class Project(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=1024)
    type = models.CharField(max_length=255)
    users = models.ManyToManyField(
        get_user_model(),
        through=Contributor,
        # through_fields=('project_id', 'user_id')
    )
