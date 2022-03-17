from django.contrib.auth.models import User
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from drf_util.decorators import serialize_decorator

from apps.tasks.serializers import UserSerializer,  UserListSerializer


class RegisterUserView(GenericAPIView):
    serializer_class = UserSerializer

    permission_classes = (AllowAny,)
    authentication_classes = ()

    @serialize_decorator(UserSerializer)
    def post(self, request):
        validated_data = request.serializer.validated_data

        user = User.objects.create(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            username=validated_data['email'],
            is_superuser=True,
            is_staff=True
        )
        user.set_password(validated_data['password'])
        user.save()

        return Response(UserSerializer(user).data)


class UserListViewSet(ListModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = UserListSerializer
    queryset = User.objects.all()
