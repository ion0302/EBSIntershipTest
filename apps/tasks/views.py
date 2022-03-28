# @swagger_auto_schema(request_body=TimeLogSerializer)
from datetime import datetime
from django.db.models import Sum, Q, Exists, OuterRef

from django.core.mail import send_mail
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from apps.tasks import serializers
from apps.tasks.filtersets import TaskFilterSet, TimeLogFilterSet
from apps.tasks.models import Task, Comment, Timer, TimeLog
from apps.tasks.serializers import TaskSerializer, CommentSerializer, TaskListSerializer, TimeLogSerializer, \
    TimerSerializer, TaskAssignToSerializer
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
    queryset = Task.objects.with_total_duration()
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields = ['title']
    ordering_fields = ['pk']
    filterset_class = TaskFilterSet

    def get_serializer_class(self):
        if self.action in ['list']:
            return serializers.TaskListSerializer

        if self.action in ['update', 'partial_update']:
            return serializers.TaskUpdateSerializer

        if self.action == 'assign_to':
            return serializers.TaskAssignToSerializer

        if self.action in ['complete', 'timer_start', 'timer_stop']:
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

    @action(detail=True, methods=['GET'])
    def logs(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = TimeLogSerializer(instance.task_timelog_set, many=True)
        return Response(data=serializer.data)

    @action(detail=True, methods=['POST'])
    def timer_start(self, request, *args, **kwargs):
        instance, created = Timer.objects.get_or_create(user=self.request.user, task=self.get_object())
        instance.start()
        serializer = TimerSerializer(instance)

        return Response(data=serializer.data)

    @action(detail=True, methods=['POST'])
    def timer_stop(self, request, *args, **kwargs):
        instance = Timer.objects.get(task=self.get_object(), user=self.request.user)
        instance.stop()
        serializer = TimerSerializer(instance)

        return Response(data=serializer.data)

    @action(detail=False, methods=['GET'], url_path='top-20')
    def top_20_tasks(self, request, *args, **kwargs):
        last_month = timezone.now().month
        queryset = Task.objects.annotate(
            total_duration=Sum(
                'task_timelog_set__duration',
                filter=Q(
                    task_timelog_set__started_at__month=last_month
                )
            )
        ).filter(
            Exists(
                TimeLog.objects.filter(
                    task=OuterRef('pk')
                )
            )
        ).order_by('-total_duration')[:20]

        return Response(data=TaskListSerializer(queryset, many=True).data)


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


class TimeLogViewSet(ModelViewSet):
    serializer_class = TimeLogSerializer
    queryset = TimeLog.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['pk']
    filterset_class = TimeLogFilterSet

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
