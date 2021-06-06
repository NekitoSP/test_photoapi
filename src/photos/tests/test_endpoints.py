import json
from pathlib import Path

from django.contrib.auth.models import User
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from rest_framework.test import APIClient

from photos.models import Photo, UserPhoto


# TODO: по аналогии с существующими тестами можно еще проверить такие сценарии:
#  1) эндпоинт update_photo
#      - сценарий успешного обновления комментария
#  2) эндпоинт get_photos
#      - сценарий успешной загрузки фото + есть ли изображение в последующем результате от get_photos
#      - сценарии безуспешной загрузки (нет права или невалидное изображение) + отсутствует ли оно в get_photos
#      - сценарий обновления комментария + обновился ли комментарий в get_photos
#      - ... либо в этих сценариях принудительно создавать фото в базе через Photo.objects.create(),
#        так тесты останутся модульными и менее зависимыми от эндпоинта загрузки, что упростит последующий рефакторинг эндпоинта upload_photo


class TestAuthenticateEndpoint(TestCase):
    def setUp(self) -> None:
        self.user_1 = User.objects.create_user(username='user_1', password='1')

    def test_credentials_valid(self):
        """
        Проверяет аутентификацию при корректно указанных username/password
        """
        # Arrange
        client = APIClient()
        request = {
            'username': 'user_1',
            'password': '1',
        }

        # Act
        response = client.post('/api/photos/authenticate/', request, format='json')

        # Assert
        self.assertEqual(200, response.status_code, 'Код ответа не совпадает с ожидаемым')

        is_success = json.loads(response.content)['success']
        self.assertTrue(is_success, 'response.success не совпадает с ожидаемым')

    def test_credentials_invalid(self):
        """
        Проверяет аутентификацию при ошибочных username/password
        """
        # Arrange
        client = APIClient()
        request = {
            'username': 'invalid_username',  # учетные данные, которых точно нет в БД
            'password': 'invalid_password',
        }

        # Act
        response = client.post('/api/photos/authenticate/', request, format='json')

        # Assert
        self.assertEqual(200, response.status_code, 'Код ответа не совпадает с ожидаемым')

        is_success = json.loads(response.content)['success']
        self.assertFalse(is_success, 'response.success не совпадает с ожидаемым')


class TestUploadPhotoEndpoint(TestCase):
    def setUp(self) -> None:
        self.user_not_permission = User.objects.create_user(username='nopermission', password='1')
        self.user_1 = User.objects.create_user(username='user_1', password='1')
        UserPhoto.objects.create(user=self.user_1, can_add_photo=True)
        self.files_dir = Path(__file__).resolve().parent / 'files'

    def test_upload_valid(self):
        """
        Тест загрузки изображений: сценарий успешной загрузки
        """
        # Arrange
        client = APIClient()
        photo = File(open(self.files_dir / 'file_valid_2.png', 'rb'))
        photo_file = SimpleUploadedFile('file_valid_2.png', photo.read(), content_type='multipart/form-data')
        request = {
            'photo': photo_file,
            'comment': 'test',
        }

        # Act
        client.login(username='user_1', password='1')
        response = client.post(
            '/api/photos/uploadPhoto/',
            request,
        )

        # Assert
        self.assertEqual(200, response.status_code, 'Код ответа не совпадает с ожидаемым')

        response_json = json.loads(response.content)
        is_success = response_json['success']
        self.assertTrue(is_success, 'response.success не совпадает с ожидаемым')
        photo_id = response_json['result']['id']
        found_photo = Photo.objects.get(id=photo_id)
        self.assertEqual('test', found_photo.comment, 'Состояние загруженного изображения не совпадает с ожидаемым')
        self.assertEqual(self.user_1, found_photo.user, 'Состояние загруженного изображения не совпадает с ожидаемым')

    def test_upload_invalid(self):
        """
        Тест загрузки изображений: сценарий неуспешной загрузки (неподходящий файл)
        """
        # Arrange
        client = APIClient()
        photo = File(open(self.files_dir / 'file_invalid_1.png', 'rb'))
        photo_file = SimpleUploadedFile('file_invalid_1.png', photo.read(), content_type='multipart/form-data')
        request = {
            'photo': photo_file,
            'comment': 'test_invalid',
        }

        # Act
        client.login(username='user_1', password='1')
        response = client.post(
            '/api/photos/uploadPhoto/',
            request,
        )

        # Assert
        self.assertEqual(200, response.status_code, 'Код ответа не совпадает с ожидаемым')

        response_json = json.loads(response.content)
        is_success = response_json['success']
        self.assertFalse(is_success, 'response.success не совпадает с ожидаемым')
        found_photo = Photo.objects.filter(comment='test_invalid').first()
        self.assertIsNone(found_photo, 'Изображение не должно было сохраниться в БД')

    def test_upload_nopermission(self):
        """
        Тест загрузки изображений: сценарий неуспешной загрузки (отсутствует право на загрузку файлов)
        """
        # Arrange
        client = APIClient()
        photo = File(open(self.files_dir / 'file_valid_2.png', 'rb'))
        photo_file = SimpleUploadedFile('file_valid_2.png', photo.read(), content_type='multipart/form-data')
        request = {
            'photo': photo_file,
            'comment': 'test_nopermission',
        }

        # Act
        client.login(username='nopermission', password='1')
        response = client.post(
            '/api/photos/uploadPhoto/',
            request,
        )

        # Assert
        self.assertEqual(403, response.status_code, 'Код ответа не совпадает с ожидаемым')

        found_photo = Photo.objects.filter(comment='test_nopermission').first()
        self.assertIsNone(found_photo, 'Изображение не должно было сохраниться в БД')
