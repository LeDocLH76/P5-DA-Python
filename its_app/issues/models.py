from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

from its_app.projects.models import Project


class Issue(models.Model):
    BUG = 'BG'
    IMPROVEMENT = 'IP'
    TASK = 'TD'
    LOW = 'LW'
    MEDIUM = 'MD'
    HIGHT = 'HI'
    TODO = 'TD'
    ONGOING = 'OG'
    COMPLETED = 'CP'

    ISSUE_TAG = [
        (BUG, 'Bug'),
        (IMPROVEMENT, 'Improvement')
        (TASK, 'Task'),
    ]

    ISSUE_PRIORITY = [
        (LOW, 'Low'),
        (MEDIUM, 'Medium')
        (HIGHT, 'Hight'),
    ]

    ISSUE_STATUS = [
        (TODO, 'Todo'),
        (ONGOING, 'Ongoing')
        (COMPLETED, 'Completed'),
    ]

    title = models.CharField(max_length=255, blank=False)
    description = models.CharField(max_length=1024, blank=False)
    tag = models.CharField(max_length=4, choices=ISSUE_TAG)
    priority = models.CharField(max_length=4, choices=ISSUE_PRIORITY)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    status = models.CharField(max_length=4, choices=ISSUE_STATUS)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    assignee = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    created_time = models.DateTimeField(default=timezone.now)
