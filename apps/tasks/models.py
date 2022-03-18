from django.contrib.auth.models import User
from django.db import models


class Task(models.Model):
    class Status(models.TextChoices):
        COMPLETED = 'completed'
        NOT_COMPLETED = 'not_completed'

    title = models.CharField(max_length=100, db_index=True)
    description = models.TextField()
    status = models.CharField(max_length=200, choices=Status.choices,
                              default=Status.NOT_COMPLETED)
    user = models.ForeignKey(User, related_name="tasks", on_delete=models.CASCADE)


class Comment(models.Model):

    text = models.TextField()
    task = models.ForeignKey(Task, related_name="comments", on_delete=models.CASCADE)
