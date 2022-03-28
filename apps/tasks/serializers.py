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
    total_time = serializers.DurationField()

    class Meta:
        model = Task
        fields = ['id', 'title', 'total_time']


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


