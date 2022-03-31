
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models import Sum
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.serializers import Serializer
from rest_framework.viewsets import GenericViewSet

from apps.tasks.models import TimeLog
from apps.users.serializers import UserSerializer, UserListSerializer


class RegisterUserView(GenericAPIView):
    serializer_class = UserSerializer

    permission_classes = [AllowAny]
    authentication_classes = ()

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['username'] = serializer.validated_data['email']
        password = serializer.validated_data.pop('password')
        user = serializer.save()
        user.set_password(password)
        user.save()

        return Response(data=UserSerializer(user).data)


class UserListViewSet(ListModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = UserListSerializer
    queryset = User.objects.all()

    @action(detail=False, methods=['GET'], url_path='last-month-logs', serializer_class=Serializer)
    def last_month_logs(self, request, *args, **kwargs):
        user = self.request.user
        last_month = timezone.now().month

        logs = TimeLog.objects.filter(user=user, started_at__month=last_month).aggregate(Sum('duration'))
        minutes = None
        if logs['duration__sum']:
            minutes = logs['duration__sum'].total_seconds()/60

            return Response({"work time": int(minutes)}, status=status.HTTP_200_OK)
        else:
            return Response({"work time": None}, status=status.HTTP_200_OK)
