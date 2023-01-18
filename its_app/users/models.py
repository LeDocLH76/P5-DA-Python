from django.db import models
from django.contrib.auth.models import AbstractUser


class MyUser(AbstractUser):
    """Model for its_app users
    username, password, first_name, last_name, email
    are already defined in AbstractUser
    """
