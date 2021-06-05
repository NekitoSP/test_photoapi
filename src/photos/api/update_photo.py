from rest_framework import serializers
from rest_framework.decorators import api_view

from photos.api.serializers import PhotoSerializer
from photos.api.utils.flow import flow
from photos.api.utils.mixins import UserMixin
from photos.models import Photo


class Request_UpdatePhotoSerializer(UserMixin, serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ('id', 'comment',)
        extra_kwargs = {
            'id': {
                'read_only': False,
            }
        }

    def validate(self, attrs):
        try:
            photo_id = attrs['id']
            self.instance = Photo.objects.by_user(self.user).get(id=photo_id)
        except Photo.DoesNotExist:
            raise serializers.ValidationError({
                'id': 'Изображение не найдено'
            })
        return attrs


class Response_UpdatePhotoSerializer(PhotoSerializer):
    ...


@api_view(['POST'])
@flow(Request_UpdatePhotoSerializer, Response_UpdatePhotoSerializer)
def update_photo(request, serializer: Request_UpdatePhotoSerializer):
    return serializer.save()
