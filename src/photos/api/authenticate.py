from typing import Type

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny

from photos.api.utils.flow import flow, flow_schema_wrap
from photos.api.utils.mixins import RequestMixin


class Request_AuthenticateSerializer(RequestMixin, serializers.Serializer):
    class Meta:
        ref_name = None
    username = serializers.CharField(write_only=True, label="Юзернейм")
    password = serializers.CharField(write_only=True, label="Пароль")

    user: User

    def validate(self, attrs):
        username = attrs['username']
        password = attrs['password']
        self.user = authenticate(self.request, username=username, password=password)
        if self.user is None:
            raise ValidationError('Invalid credentials')
        return attrs


class Response_AuthenticateSerializer(serializers.Serializer):
    class Meta:
        ref_name = None
    ...


@swagger_auto_schema(
    method='post',
    operation_description="Аутентификация по юзернейму и паролю",
    request_body=Request_AuthenticateSerializer,
    responses={
        200: openapi.Response('Результат аутентификации', flow_schema_wrap(Request_AuthenticateSerializer, Response_AuthenticateSerializer)),
    },
    tags=['Photos']
)
@api_view(['POST'])
@permission_classes([AllowAny])
@flow(Request_AuthenticateSerializer, Response_AuthenticateSerializer)
def authenticate_view(request, serializer: Request_AuthenticateSerializer):
    login(request, serializer.user)
