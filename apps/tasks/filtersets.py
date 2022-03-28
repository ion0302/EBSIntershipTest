
from django_filters.rest_framework import FilterSet, filters

from apps.tasks.models import Task, TimeLog


class TaskFilterSet(FilterSet):
    class Meta:
        model = Task
        fields = ['is_completed', 'created_by', 'assigned_to']


class TimeLogFilterSet(FilterSet):
    started_at = filters.DateFromToRangeFilter()

    class Meta:
        model = TimeLog
        fields = ['task', 'user', 'started_at']
