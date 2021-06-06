from rest_framework import permissions

from photos.models import UserPhoto


class CanAddPhotoPermission(permissions.BasePermission):
    message = 'Проверяет право загрузки изображений user.photos_settings.can_add_photo'

    def has_permission(self, request, view):
        try:
            return request.user.photos_settings and request.user.photos_settings.can_add_photo
        except UserPhoto.DoesNotExist:
            return False
