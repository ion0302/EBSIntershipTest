from django.contrib.auth.models import User
from rest_framework import serializers

from apps.tasks.serializers import TaskSerializer


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "password",)


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', "first_name", "last_name"]


# class UserLogsSerializer(serializers.ModelSerializer):
#     work_time = serializers.SerializerMethodField()
#
#     def work_time :
#         cod

# class UsersTasksSerializer(serializers.ModelSerializer):
#     tasks = TaskSerializer(many=True)
#
#     class Meta:
#         model = User
#         fields = ['tasks']
