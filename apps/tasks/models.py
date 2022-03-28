from datetime import timedelta

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum, QuerySet
from django.utils import timezone


class TaskQuerySet(QuerySet):
    def with_total_duration(self):
        return self.annotate(total_duration=Sum('task_timelog_set__duration'))


class Task(models.Model):
    objects = TaskQuerySet.as_manager()

    title = models.CharField(max_length=100, db_index=True)
    description = models.TextField()
    is_completed = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='created_task_set')
    assigned_to = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='assigned_task_set')


class Comment(models.Model):
    text = models.TextField()
    task = models.ForeignKey(Task, related_name="comments", on_delete=models.CASCADE)


class TimeLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_timelog_set')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='task_timelog_set')
    started_at = models.DateTimeField(null=True)
    duration = models.DurationField(default=timedelta)




class Timer(models.Model):
    class Meta:
        unique_together = [
            ('user', 'task')
        ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_timer_set')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='task_timer_set')
    is_started = models.BooleanField(default=False)
    started_at = models.DateTimeField(null=True)
    duration = models.DurationField(default=timedelta)

    @property
    def duration_now(self):
        now = timezone.now()
        return self.duration + (int(self.is_started) * (now - (self.started_at or now)))

    def start(self):
        if not self.is_started:
            now = timezone.now()

            self.is_started = True
            self.started_at = now
            self.save()

    def stop(self):
        if self.is_started:
            now = timezone.now()
            duration = now - self.started_at

            self.is_started = False
            self.duration += duration
            self.save()

            TimeLog.objects.create(
                user=self.user,
                task=self.task,
                started_at=self.started_at,
                duration=duration
            )
