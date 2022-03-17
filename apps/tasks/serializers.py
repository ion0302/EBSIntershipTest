from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "password",)


class UserListSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', "first_name", "last_name"]

