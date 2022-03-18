from drf_util.decorators import serialize_decorator
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.permissions import IsAuthenticated

from apps.tasks import serializers
from apps.tasks.models import Task
from apps.tasks.serializers import TaskSerializer, TaskPostSerializer, TaskPatchSerializer


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
        if self.request.method == 'PATCH':
            return TaskPatchSerializer
        if self.action == 'list':
            return serializers.TaskListSerializer
        return serializers.TaskSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        user = self.request.user
        if self.action in ['my']:
            return super().get_queryset().filter(user=user)
        if self.action in ['status_completed']:
            return super().get_queryset().filter(status='completed')
        return super().get_queryset()

    @action(detail=False, methods=['GET'])
    def my(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @action(detail=False, methods=['GET'])
    def status_completed(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)



    # @action(detail=True, methods=['GET'])
    # @serialize_decorator('TaskSerializer')
    # def completed(self, request, *args, **kwargs):
    #     task = Task.objects.filter(pk=request.valid.get('pk')).first()
    #     task.status = Task.StatusChoise.completed
    #     task.save()
    #     return Response({'succes': True, 'detail': f'task {task.title} status change to completed'})


