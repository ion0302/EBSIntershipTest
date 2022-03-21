from django.contrib.auth.models import User
from django.core.mail import send_mail
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from apps.tasks import serializers
from apps.tasks.filtersets import TaskFilterSet
from apps.tasks.models import Task, Comment
from apps.tasks.serializers import TaskSerializer, CommentSerializer
from config import settings


def task_mail_send(self, user):
    subject = 'Task Notification'
    message = f'Hi {user.username}, a new task is attached to you.'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user.email]
    send_mail(subject, message, email_from, recipient_list, fail_silently=False)


def comment_mail_send(self, user):
    subject = 'Task Notification'
    message = f'Hi {user.username}, a new comment is attached to your task.'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user.email]
    send_mail(subject, message, email_from, recipient_list, fail_silently=False)


class TaskViewSet(ModelViewSet):
    serializer_class = TaskSerializer
    queryset = Task.objects.all().order_by('id')
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields = ['title']
    ordering_fields = ['pk']
    filterset_class = TaskFilterSet

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.TaskListSerializer
        if self.action == 'update' or self.action == 'partial_update':
            return serializers.TaskUpdateSerializer
        if self.action == 'assign_to':
            return serializers.TaskAssignToSerializer
        if self.action == 'complete':
            return Serializer

        return TaskSerializer

    def perform_create(self, serializer):
        user = User.objects.get(pk=self.request.data['assigned_to'])
        task_mail_send(self, user)
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['POST'], serializer_class=Serializer)
    def complete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_completed = True
        instance.save()
        serializer = self.get_serializer(instance)

        comments = Comment.objects.filter(task=instance.id)
        user = instance.assigned_to
        if comments.count() > 0:
            subject = 'Task Notification'
            message = f'Hi {user.username}, your task is completed.'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [user.email]
            send_mail(subject, message, email_from, recipient_list, fail_silently=False)

        return Response(data=serializer.data)

    @action(detail=True, methods=['POST'])
    def assign_to(self, request, *args, **kwargs):
        instance = self.get_object()
        user = User.objects.get(pk=self.request.data['assigned_to'])
        instance.assigned_to = user
        instance.save()
        task_mail_send(self, user)
        serializer = self.get_serializer(instance)

        return Response(data=serializer.data)

    @action(detail=True, methods=['GET'], serializer_class=Serializer)
    def comments(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = CommentSerializer(instance.comments, many=True)
        return Response(data=serializer.data)


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields = ['title']
    ordering_fields = ['pk']

    def perform_create(self, serializer):
        task_id = self.request.data['task']
        task = Task.objects.get(pk=task_id)
        user = task.assigned_to
        comment_mail_send(self, user)
        serializer.save()

