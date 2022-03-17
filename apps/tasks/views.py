from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet
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
