from rest_framework.serializers import ModelSerializer

from apps.tasks.models import Task, Comment


class TaskSerializer(ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


class TaskPostSerializer(ModelSerializer):
    class Meta:
        model = Task
        read_only_fields = ['id', 'user']
        fields = ['id', 'title', 'description', 'status', 'user']


class TaskListSerializer(ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title']


class TaskPatchSerializer(ModelSerializer):
    class Meta:
        model = Task
        fields = ['user']


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

