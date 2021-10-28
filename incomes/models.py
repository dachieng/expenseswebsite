from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class UserIncome(models.Model):
    amount = models.FloatField()
    date = models.DateField(default=timezone.now)
    description = models.CharField(max_length=1000)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    source = models.CharField(max_length=200)

    def __str__(self):
        return self.source

    class Meta:
        ordering = ['-date']

    def get_absolute_url(self):
        return reverse("income-detail", kwargs={"pk": self.pk})


class Source(models.Model):
    name = models.CharField(max_length=300)

    class Meta:
        verbose_name_plural = 'Sources'

    def __str__(self):
        return self.name
