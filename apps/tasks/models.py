from django.contrib.auth.models import User
from django.db import models


class Task(models.Model):
    title = models.CharField(max_length=100, db_index=True)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
