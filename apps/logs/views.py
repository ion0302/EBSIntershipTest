from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.logs.models import Log
from apps.logs.serializers import LogSerializer


class LogViewSet(ModelViewSet):
    serializer_class = LogSerializer
    queryset = Log.objects.all()
    permission_classes = [IsAuthenticated]

    # def get_serializer_class(self):
    #     if self.action == 'create':
    #         return LogPostSerializer
    #     return LogSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


