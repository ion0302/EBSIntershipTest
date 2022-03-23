from abc import ABC

from django.db import models
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from apps.logs.models import Log


class LogSerializer(ModelSerializer):

    class Meta:
        model = Log
        fields = '__all__'
        extra_kwargs = {
            'user': {'read_only': True},
            'stop': {'read_only': True},

        }


class LogPostSerializer(ModelSerializer):

    duration = serializers.DurationField()

    # def create(self, validated_data):
    #     validated_data['user'] = self.context['request'].user
    #     validated_data['stop'] = validated_data['start'] + validated_data['duration']
    #     instance = LogSerializer.create()
    #     task = instance.task
    #     task.work_time = task.work_time + validated_data['duration']
    #     return instance

    class Meta:
        model = Log
        fields = '__all__'
        extra_kwargs = {
            'user': {'read_only': True},
            'stop': {'read_only': True},
            'duration': {'write_only': True},
        }

