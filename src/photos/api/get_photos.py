from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers
from rest_framework.decorators import api_view

from photos.api.serializers import PhotoSerializer
from photos.api.utils.flow import flow, flow_schema_wrap
from photos.models import Photo


class Request_GetPhotosSerializer(serializers.Serializer):
    class Meta:
        ref_name = None


class Response_GetPhotosSerializer(serializers.ListSerializer):
    class Meta:
        ref_name = None
    child = PhotoSerializer()


@swagger_auto_schema(
    method='get',
    operation_description="Получение списка изображений",
    responses={
        200: openapi.Response('Список изображений', flow_schema_wrap(Request_GetPhotosSerializer, Response_GetPhotosSerializer)),
    },
    tags=['Photos']
)
@api_view(['GET'])
@flow(Request_GetPhotosSerializer, Response_GetPhotosSerializer)
def get_photos(request, serializer: Request_GetPhotosSerializer):
    return Photo.objects.by_user(request.user).all()
