from rest_framework.serializers import ModelSerializer

from apps.logs.models import Log


class LogSerializer(ModelSerializer):
    class Meta:
        model = Log
        fields = '__all__'
