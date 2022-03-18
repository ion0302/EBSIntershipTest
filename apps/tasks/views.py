from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from apps.tasks import serializers
from apps.tasks.models import Task, Comment
from apps.tasks.serializers import TaskSerializer, TaskPostSerializer, TaskPatchSerializer, CommentSerializer


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

    @action(detail=True, methods=['GET'])
    def to_completed(self, request, pk, *args, **kwargs):
        Task.objects.filter(id=pk).update(status='completed')
        return Response({'success': True, 'detail': f'task with id:{pk}  status change to completed'})


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticated]


    # def get_queryset(self):
    #     if self.action in ['tasks_comments']:
    #         return super().get_queryset().filter(user=user)
    #     return super().get_queryset()
    #
    # @action(detail=True, methods=['GET'])
    # def tasks_comments(self, request,  *args, **kwargs):
    #     return super().list(request, *args, **kwargs)
