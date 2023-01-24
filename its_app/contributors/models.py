from django.db import models
from its_app.projects.models import Project
from django.contrib.auth import get_user_model


class Contributor(models.Model):
    User = get_user_model()
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    role = models.CharField(max_length=20)
