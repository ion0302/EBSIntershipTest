from rest_framework.serializers import ModelSerializer

from apps.tasks.models import Task, Comment, Log


class TaskSerializer(ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        extra_kwargs = {
            'created_by': {'read_only': True},
            'is_completed': {'read_only': True},
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
        }


class TaskListSerializer(ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title']


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class LogSerializer(ModelSerializer):
    class Meta:
        model = Log
        fields = '__all__'

