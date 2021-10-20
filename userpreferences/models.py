from django.db import models

from django.contrib.auth.models import User


class UserPreference(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    currency = models.CharField(max_length=1000, blank=True)

    def __str__(self):
        return f"{self.user.username}'s preferences"
