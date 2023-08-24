from django.db import models

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    login_attempts = models.PositiveIntegerField(default=0)
    is_customer = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)

    def __str__(self):
        return self.username


