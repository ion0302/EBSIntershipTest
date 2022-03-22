from django.db import models
from rest_framework.serializers import ModelSerializer

from apps.logs.models import Log


class LogSerializer(ModelSerializer):


    # def create(self, validated_data):
    #     validated_data['user'] = self.context['request'].user
    #     validated_data['stop'] = validated_data['start'] + validated_data['duration']
    #     instance = super(LogSerializer, self).create(validated_data)
    #
    #     return instance

    class Meta:
        model = Log
        fields = '__all__'
        extra_kwargs = {
            'user': {'read_only': True},
            'stop': {'read_only': True},
        }
