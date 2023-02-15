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

    @classmethod
    def get_user(cls, user_pk=None, username=None):
        if user_pk:
            try:
                user_obj = cls.objects.all().get(pk=user_pk)
            except cls.DoesNotExist:
                user_obj = None
            print('user_pk')
            return user_obj

        if username:
            try:
                user_obj = cls.objects.all().get(username=username)
            except cls.DoesNotExist:
                user_obj = None

            print('username')
            return user_obj

        return None
