from django.contrib.auth.models import User
from django.db import models


class UserPhoto(models.Model):
    """
    Модель-расширение стандартного User для проверки возможности загрузки изображений.


    Альтернативные решения:

    1) замена существующей модели и настройка AUTH_USER_MODEL
    2) т.к. задача схожа с проверкой прав доступа, при наличии системы прав доступа в проекте
        можно было добавить permission типа "can_add_photo" и проверять его наличие при работе с фотографиями
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    can_add_photo = models.BooleanField("Возможность загружать фотографии", default=True, blank=False, null=False)
