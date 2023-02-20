from django.contrib.auth.models import AbstractUser
from django.db import models


class MyUserManager(models.Manager):
    def get_user(self, user_pk=None, username=None):
        """
            Find a user by username or pk
            Return user_obj or None
        """
        if user_pk:
            try:
                user_obj = self.all().get(pk=user_pk)
            except MyUser.DoesNotExist:
                user_obj = None
            return user_obj
        if username:
            try:
                user_obj = self.all().get(username=username)
            except MyUser.DoesNotExist:
                user_obj = None
            return user_obj
        return None


class MyUser(AbstractUser):
    """Model for its_app users
    username, password, first_name, last_name, email
    are already defined in AbstractUser
    """
    first_name = models.CharField(max_length=150, blank=False)
    last_name = models.CharField(max_length=150, blank=False)
    email = models.EmailField(blank=False)
    objects = MyUserManager()
