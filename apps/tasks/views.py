from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.permissions import IsAuthenticated

from apps.tasks import serializers
from apps.tasks.models import Task
from apps.tasks.serializers import TaskSerializer, TaskPostSerializer


class TaskViewSet(ModelViewSet):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [
        SearchFilter,
        OrderingFilter
    ]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TaskPostSerializer
        if self.action == 'list':
            return serializers.TaskListSerializer
        return serializers.TaskSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        user = self.request.user
        if self.action in ['my']:
            return super().get_queryset().filter(user=user)
        if self.action in ['completed']:
            return super().get_queryset().filter(status='completed')
        return super().get_queryset()

    @action(detail=False, methods=['GET'])
    def my(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @action(detail=False, methods=['GET'])
    def completed(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


