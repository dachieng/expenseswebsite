from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Expense(models.Model):
    amount = models.FloatField()
    date = models.DateField(default=timezone.now)
    description = models.CharField(max_length=1000)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=200)

    def __str__(self):
        return self.category

    class Meta:
        ordering = ['-date']


class Category(models.Model):
    name = models.CharField(max_length=300)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name
