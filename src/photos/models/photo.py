from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q
from django.utils.datetime_safe import datetime


class PhotoQuerySet(models.QuerySet):
    def is_published(self):
        """
        Фильтрует опубликованные изображения
        """
        return self.filter(deleted_date=None)

    def is_deleted(self):
        """
        Фильтрует удаленные изображения
        """
        return self.filter(~Q(deleted_date=None))

    def by_user(self, user: User):
        """
        Фильтрует изображения по указанному пользователю
        :param user: пользователь
        :return:
        """
        return self.filter(user=user)


class Photo(models.Model):
    """
    Модель загруженного изображения пользователя


    т.к. фотография может быть удалена - есть альтернативные решения:

    1) текущее - deleted_date - позволяет отследить дату удаления изображения
    2) is_deleted = models.BooleanField() - то же самое, только без возможности проверки даты удаления
    3) дополнительная модель PhotoState с полями (state, date)
        - добавление нового изображения добавляет в БД строку PhotoState(state=created),
        - удаление - добавляет строку PhotoState(state=deleted)
        - такое решение позволяет более гибко управлять состояниями изображения, когда их более чем 2
        (например - ручная модерация загрузок) и отслеживать всю историю изменений
    """
    objects = PhotoQuerySet.as_manager()

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='photos')
    photo = models.ImageField("Изображение", upload_to="photos/")
    comment = models.TextField("Комментарий", blank=True, null=True)
    created_date = models.DateTimeField("Дата создания", auto_now=True)
    deleted_date = models.DateTimeField("Дата удаления", auto_now=False, default=None, blank=True, null=True)

    def soft_delete(self):
        self.deleted_date = datetime.now()

    @property
    def is_deleted(self):
        return self.deleted_date is not None
