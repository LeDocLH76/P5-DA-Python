from django.db import models


class Project(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=1024)
    type = models.CharField(max_length=255)
