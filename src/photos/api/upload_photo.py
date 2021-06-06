from random import randrange

from rest_framework import serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError, PermissionDenied

from photos.api.serializers import PhotoSerializer
from photos.api.utils.flow import flow
from photos.models import Photo
from photos.permissions import CanAddPhotoPermission


class Request_UploadPhotoSerializer(serializers.ModelSerializer):
    class Meta:
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
    ...


@api_view(['POST'])
@permission_classes([CanAddPhotoPermission])
@flow(Request_UploadPhotoSerializer, Response_UploadPhotoSerializer)
def upload_photo(request, serializer: Request_UploadPhotoSerializer):
    instance = Photo.objects.create(
        user=request.user,
        photo=serializer.validated_data['photo'],
        comment=serializer.validated_data['comment']
        # или просто **serializer.validated_data
    )
    return instance
