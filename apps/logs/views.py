from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.logs.models import Log
from apps.logs.serializers import LogSerializer, LogPostSerializer


class LogViewSet(ModelViewSet):
    serializer_class = LogSerializer
    queryset = Log.objects.all()
    permission_classes = [IsAuthenticated]

    # def get_serializer_class(self):
    #     if self.action == 'create':
    #         return LogPostSerializer
    #     return LogSerializer

    @action(detail=False, methods=['POST'], serializer_class=LogPostSerializer, url_path='add-log')
    def add_log(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)

        duration = serializer.validated_data['duration']
        start = serializer.validated_data['start']
        stop = duration + start
        task = serializer.validated_data['task']
        log = Log.objects.create(user=self.request.user, stop=stop, task=task, start=start)

        if task.work_time is not None:
            task.work_time += duration
        else:
            task.work_time = duration
        task.save()

        return Response(LogSerializer(log).data)
