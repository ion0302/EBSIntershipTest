from rest_framework.serializers import ModelSerializer

from apps.tasks.models import Task, Comment


class TaskSerializer(ModelSerializer):

    # def create(self, validated_data):
    #     validated_data['created_by'] = self.context['request'].user
    #     instance = super(TaskSerializer, self).create(validated_data)
    #     if instance.assigned_to:
    #         instance.assigned_to.email_user()
    #     return instance

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


