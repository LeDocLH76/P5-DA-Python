from django.db import models
from django.contrib.auth import get_user_model


class Contributor(models.Model):
    OWNER = 'OW'
    CONTRIBUTOR = 'CO'

    USER_ROLES = [
        (OWNER, 'Owner'),
        (CONTRIBUTOR, 'Contributor'),
    ]
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    role = models.CharField(max_length=4, choices=USER_ROLES)

    # class Meta:
    #     unique_together = ('user', 'project')
    # UniqueConstraint(fields=['user','project'])


class Project(models.Model):
    BACKEND = 'BE'
    FRONTEND = 'FE'
    ANDROID = 'AD'
    IOS = 'IO'

    PROJECT_TYPES = [
        (BACKEND, 'Back-end'),
        (FRONTEND, 'Front-end'),
        (ANDROID, 'Android'),
        (IOS, 'iOS'),
    ]
    title = models.CharField(max_length=255, blank=False, )
    description = models.CharField(max_length=1024, blank=False)
    type = models.CharField(max_length=4, choices=PROJECT_TYPES)
    users = models.ManyToManyField(
        get_user_model(),
        through=Contributor,
    )
    # Add owner fk
