from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny

from photos.api.utils.flow import flow
from photos.api.utils.mixins import RequestMixin


class Request_AuthenticateSerializer(RequestMixin, serializers.Serializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    user: User

    def validate(self, attrs):
        username = attrs['username']
        password = attrs['password']
        self.user = authenticate(self.request, username=username, password=password)
        if self.user is None:
            raise ValidationError('Invalid credentials')
        return attrs


class Response_AuthenticateSerializer(serializers.Serializer):
    ...


@api_view(['POST'])
@permission_classes([AllowAny])
@flow(Request_AuthenticateSerializer, Response_AuthenticateSerializer)
def authenticate_view(request, serializer: Request_AuthenticateSerializer):
    login(request, serializer.user)
