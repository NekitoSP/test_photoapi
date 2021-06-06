from random import randrange

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework.parsers import MultiPartParser

from photos.api.serializers import PhotoSerializer
from photos.api.utils.flow import flow, flow_schema_wrap
from photos.models import Photo
from photos.permissions import CanAddPhotoPermission


class Request_UploadPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        ref_name = None
        model = Photo
        fields = ('photo', 'comment')

    def validate_photo(self, value):
        # было проблематично создать такие изображения, хеш которых бы различался по модулю 2, поэтому оставил хеш от имени файла (последний символ)
        # content = value.file.read()
        # value.file.seek(0)
        # _hash = hash(content)
        # _hash = randrange(10)
        _hash = hash(int(value.name.split('.')[0][-1]))
        if _hash % 2 == 0:
            return value

        raise ValidationError('Фотография не может быть загружена!')


class Response_UploadPhotoSerializer(PhotoSerializer):
    class Meta(PhotoSerializer.Meta):
        ref_name = None


@swagger_auto_schema(
    method='post',
    operation_description="Загрузка изображения",
    request_body=Request_UploadPhotoSerializer,
    responses={
        200: openapi.Response('Результат загрузки изображения', flow_schema_wrap(Request_UploadPhotoSerializer, Response_UploadPhotoSerializer)),
    },
    tags=['Photos']
)
@api_view(['POST'])
@permission_classes([CanAddPhotoPermission])
@parser_classes([MultiPartParser])
@flow(Request_UploadPhotoSerializer, Response_UploadPhotoSerializer)
def upload_photo(request, serializer: Request_UploadPhotoSerializer):
    instance = Photo.objects.create(
        user=request.user,
        photo=serializer.validated_data['photo'],
        comment=serializer.validated_data['comment']
        # или просто **serializer.validated_data
    )
    return instance
