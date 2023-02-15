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

    class Meta:
        constraints = [
            models.constraints.UniqueConstraint(
                fields=['user', 'project'],
                name='contributor_user_project'
            )
        ]


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
    description = models.TextField(blank=False)
    type = models.CharField(max_length=4, choices=PROJECT_TYPES)
    users = models.ManyToManyField(
        get_user_model(),
        through=Contributor,
    )

    @classmethod
    def get_project(cls, request, project_pk=None):
        if project_pk:
            try:
                project_obj = cls.objects.filter(
                    users=request.user
                ).get(pk=project_pk)
            except cls.DoesNotExist:
                project_obj = None
            return project_obj
        return None

    @property
    def get_contributors(self):
        project_contributors = [
            record.user
            for
            record in Contributor.objects.filter(project=self.pk)
        ]
        return project_contributors
