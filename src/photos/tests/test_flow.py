from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.test import APIRequestFactory
from rest_framework.utils import json

from photos.api.utils.flow import flow


class TestFlowRequestSerializer(serializers.Serializer):
    value = serializers.IntegerField(required=True)

    def validate_value(self, value):
        if value % 2:
            raise ValidationError('even')
        return value


class TestFlowResponseSerializer(serializers.Serializer):
    output = serializers.IntegerField(required=True)


@api_view(['POST'])
@permission_classes([AllowAny])
@flow(TestFlowRequestSerializer, TestFlowResponseSerializer)
def test_flow(request, serializer: TestFlowRequestSerializer = None):
    value = serializer.validated_data['value']
    return {
        'output': value * 2
    }


class TestFlow(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username='test', password='1')

    def test_flow_success(self):
        # Arrange
        factory = APIRequestFactory()
        request = factory.post('/', {'value': 2}, format='json')

        # Act
        response = test_flow(request)

        # Assert
        actual_response = json.loads(response.content)
        expected_response = {
            'success': True,
            'result': {
                'output': 4,
            },
            'errors': None
        }
        self.assertDictEqual(expected_response, actual_response, 'Ответ от test_flow не совпадает с ожидаемым')

    def test_flow_failure_validation(self):
        # Arrange
        factory = APIRequestFactory()
        request = factory.post('/', {'value': 1}, format='json')

        # Act
        response = test_flow(request)

        # Assert
        actual_response = json.loads(response.content)
        expected_response = {
            'success': False,
            'result': None,
            'errors': {
                'value': ['even']
            }
        }
        self.assertDictEqual(expected_response, actual_response, 'Ответ от test_flow не совпадает с ожидаемым')

    def test_flow_failure_invalid_data(self):
        # Arrange
        factory = APIRequestFactory()
        request = factory.post('/', None, format='json')

        # Act
        response = test_flow(request)

        # Assert
        actual_response = json.loads(response.content)
        expected_response = {
           'success': False,
           'result': None,
           'errors': {
               'value': ['This field is required.']
           }
        }
        self.assertDictEqual(expected_response, actual_response, 'Ответ от test_flow не совпадает с ожидаемым')

    def test_flow_failure_invalid_http_method(self):
        # Arrange
        factory = APIRequestFactory()
        request = factory.get('/', None, format='json')

        # Act
        response = test_flow(request)

        # Assert

        # actual_response = json.loads(response.content)
        # expected_response = {
        #    'success': False,
        #    'result': None,
        #    'errors': {
        #        'value': ['This field is required.']
        #    }
        # }
        self.assertEqual(405, response.status_code, 'Код ответа сервера не соответствует ожидаемому')
        # self.assertDictEqual(expected_response, actual_response, 'Ответ от test_flow не совпадает с ожидаемым')
