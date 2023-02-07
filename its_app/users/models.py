from django.contrib.auth.models import AbstractUser
from django.db import models


class MyUser(AbstractUser):
    """Model for its_app users
    username, password, first_name, last_name, email
    are already defined in AbstractUser
    """
    first_name = models.CharField(max_length=150, blank=False)
    last_name = models.CharField(max_length=150, blank=False)
    email = models.EmailField(blank=False)
