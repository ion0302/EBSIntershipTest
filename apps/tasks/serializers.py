from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from apps.tasks.models import Task


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "password",)


class UserListSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', "first_name", "last_name"]


class TaskSerializer(ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

