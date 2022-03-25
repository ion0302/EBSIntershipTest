from datetime import datetime, timezone, timedelta
from django.db.models import Sum

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer


from apps.tasks.models import Task, Comment


class TaskSerializer(ModelSerializer):

    class Meta:
        model = Task
        fields = '__all__'
        extra_kwargs = {
            'created_by': {'read_only': True},
            'is_completed': {'read_only': True},
            'work_time:': {'read_only': True},
        }


class TaskAssignToSerializer(ModelSerializer):
    class Meta:
        model = Task
        fields = ['assigned_to']


class TaskUpdateSerializer(ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        extra_kwargs = {
            'created_by': {'read_only': True},
            'is_completed': {'read_only': True},
            'assigned_to': {'read_only': True},
            'work_time:': {'read_only': True},
        }


class TaskListSerializer(ModelSerializer):

    class Meta:
        model = Task
        fields = ['id', 'title']


class TaskTop20Serializer(ModelSerializer):

    log_time = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ['id', 'title', 'log_time']

    def get_log_time(self):
        last_month = datetime.now(tz=timezone.utc) - timedelta(days=30)
        t = Task.objects.filter(task_log_set__stop__gte=last_month).annotate(
            time=Sum('task_log_set__stop' + 'task_log_set__start'))



class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


