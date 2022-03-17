from django.contrib.auth.models import User
from django.db import models


class Task(models.Model):
    class StatusChoise(models.TextChoices):
        completed = 'completed'
        not_completed = 'not_completed'

    title = models.CharField(max_length=100, db_index=True)
    description = models.TextField()
    status = models.CharField(max_length=200, choices=StatusChoise.choices,
                              default=StatusChoise.not_completed)
    user = models.ForeignKey(User, related_name="tasks", on_delete=models.CASCADE)
