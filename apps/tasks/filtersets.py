from django_filters.rest_framework import FilterSet, filters

from apps.tasks.models import Task


class TaskFilterSet(FilterSet):
    class Meta:
        model = Task
        fields = ['is_completed', 'created_by', 'assigned_to']
