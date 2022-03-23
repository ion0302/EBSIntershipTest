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

    class Meta:
        model = Log
        fields = '__all__'
        extra_kwargs = {
            'user': {'read_only': True},
            'stop': {'read_only': True},
            'duration': {'write_only': True},
        }

