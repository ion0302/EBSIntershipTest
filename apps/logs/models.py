from django.contrib.auth.models import User
from django.db import models
from apps.tasks.models import Task


class Log(models.Model):
    start = models.DateTimeField(null=True)
    stop = models.DateTimeField(null=True)
    task = models.ForeignKey(Task, related_name='task_log_set', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='user_log_set', on_delete=models.CASCADE)
