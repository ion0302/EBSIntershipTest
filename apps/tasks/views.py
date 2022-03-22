from django.contrib.auth.models import User
from django.core.mail import send_mail
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
import datetime

from apps.logs.models import Log
from apps.logs.serializers import LogSerializer
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
        if self.action == 'complete' or self.action == 'start_log' or self.action == 'stop_log':
            return Serializer

        return TaskSerializer

    def perform_create(self, serializer):
        instance = serializer.save(created_by=self.request.user)
        user = instance.assigned_to
        if instance.assigned_to:
            task_mail_send(self, user)

    @action(detail=True, methods=['POST'])
    def complete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_completed = True
        instance.save()
        serializer = self.get_serializer(instance)

        return Response(data=serializer.data)

    @action(detail=True, methods=['POST'], url_path='assign-to')
    def assign_to(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data, instance=self.get_object())
        serializer.is_valid(raise_exception=True)
        task = serializer.save()
        task_mail_send(self, task.assigned_to)
        return Response(data=serializer.data)

    @action(detail=True, methods=['GET'])
    def comments(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = CommentSerializer(instance.comments, many=True)
        return Response(data=serializer.data)

    @action(detail=True, methods=['POST'], url_path='start-log')
    def start_log(self, request, *args, **kwargs):

        instance = self.get_object()
        test_log = Log.objects.filter(task=instance).last()
        if test_log.stop == "":
            return Response({"Error": "already started a log for this task"}, status=status.HTTP_400_BAD_REQUEST)

        log = Log.objects.create(
            start=datetime.datetime.now(),
            task=instance,
            user=request.user
        )
        log.save()
        serializer = self.get_serializer(log)
        return Response(data=serializer.data)

    @action(detail=True, methods=['POST'], url_path='stop-log')
    def stop_log(self, request, *args, **kwargs):
        instance = self.get_object()
        log = Log.objects.filter(task=instance).last()
        if log.stop != "":
            return Response({"Error": "this log is already stopped"}, status=status.HTTP_400_BAD_REQUEST)
        log.stop = datetime.datetime.now()
        log.duration = datetime.timedelta(hours=log.stop.hour - log.start.hour,
                                          minutes=log.stop.minute - log.start.minute,
                                          seconds=log.stop.second - log.start.second)
        log.save()
        serializer = self.get_serializer(log)
        return Response(data=serializer.data)


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields = ['title']
    ordering_fields = ['pk']

    def perform_create(self, serializer):
        instance = serializer.save()
        task = instance.task
        user = task.assigned_to
        if user:
            comment_mail_send(self, user)

        if task.is_completed:
            user = self.request.user
            subject = 'Task Notification'
            message = f'Hi {user.username}, you added a comment to completed task.'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [user.email]
            send_mail(subject, message, email_from, recipient_list, fail_silently=False)
