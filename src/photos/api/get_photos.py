from rest_framework import serializers
from rest_framework.decorators import api_view

from photos.api.serializers import PhotoSerializer
from photos.api.utils.flow import flow
from photos.models import Photo


class Request_GetPhotosSerializer(serializers.Serializer):
    ...


class Response_GetPhotosSerializer(serializers.ListSerializer):
    child = PhotoSerializer()


@api_view(['GET'])
@flow(Request_GetPhotosSerializer, Response_GetPhotosSerializer)
def get_photos(request, serializer: Request_GetPhotosSerializer):
    return Photo.objects.by_user(request.user).all()
