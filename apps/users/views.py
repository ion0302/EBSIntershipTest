from django.contrib.auth.models import User
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from apps.users.serializers import UserSerializer, UserListSerializer


class RegisterUserView(GenericAPIView):
    serializer_class = UserSerializer

    permission_classes = [AllowAny]
    authentication_classes = ()

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User.objects.create(
            first_name=serializer.validated_data['first_name'],
            last_name=serializer.validated_data['last_name'],
            email=serializer.validated_data['email'],
            username=serializer.validated_data['email'],
            is_superuser=False,
            is_staff=False
        )
        user.set_password(serializer.validated_data['password'])
        user.save()

        return Response(data=UserSerializer(user).data)


class UserListViewSet(ListModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = UserListSerializer
    queryset = User.objects.all()
