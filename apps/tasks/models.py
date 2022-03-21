from django.contrib.auth.models import User
from django.db import models


class Task(models.Model):
    title = models.CharField(max_length=100, db_index=True)
    description = models.TextField()
    is_completed = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='created_task_set')
    assigned_to = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='assigned_task_set')


class Comment(models.Model):
    text = models.TextField()
    task = models.ForeignKey(Task, related_name="comments", on_delete=models.CASCADE)


class Log(models.Model):
    start = models.DateTimeField(null=True)
    stop = models.DateTimeField(null=True)
    duration = models.DurationField(null=True)
    task = models.ForeignKey(Task, related_name='task_log_set', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='user_log_set', on_delete=models.CASCADE)
