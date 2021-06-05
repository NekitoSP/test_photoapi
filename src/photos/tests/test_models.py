from django.contrib.auth.models import User
from django.test import TestCase

from photos.models import Photo


class TestPhotos(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username='test', password='1')

    def test_photo_published(self):
        # Arrange & Act
        photo1 = Photo.objects.create(user=self.user, comment='photo_1')
        photo2 = Photo.objects.create(user=self.user, comment='photo_2')

        # Assert
        photos = self.user.photos.is_published()
        self.assertEqual(2, photos.count(), 'Конечное количество изображений не соответствует ожидаемому')

    def test_photo_delete(self):
        # Arrange & Act
        photo1 = Photo.objects.create(user=self.user, comment='photo_1')
        photo2 = Photo.objects.create(user=self.user, comment='photo_2')
        photo2.soft_delete()
        photo2.save()

        # Assert
        published_photos = self.user.photos.is_published()
        deleted_photos = self.user.photos.is_deleted()

        self.assertEqual(1, published_photos.count(), 'Конечное количество опубликованных изображений не соответствует ожидаемому')
        self.assertEqual(1, deleted_photos.count(), 'Конечное количество удаленных изображений не соответствует ожидаемому')

        found_published_photo = published_photos.first()
        self.assertEqual('photo_1', found_published_photo.comment, 'Состояние (comment) загруженного изображения не соответствует ожидаемому')
        self.assertFalse(found_published_photo.is_deleted, 'Состояние (is_deleted) загруженного изображения не соответствует ожидаемому')

        found_deleted_photo = deleted_photos.first()
        self.assertEqual('photo_2', found_deleted_photo.comment, 'Состояние (comment) удаленного изображения не соответствует ожидаемому')
        self.assertTrue(found_deleted_photo.is_deleted, 'Состояние (is_deleted) удаленного изображения не соответствует ожидаемому')
