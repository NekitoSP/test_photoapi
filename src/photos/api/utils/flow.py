from typing import Callable, Any, Type
from typing import Dict

from django.http import JsonResponse
from rest_framework import serializers
from rest_framework.request import Request

from photos.api.utils.mixins import UserMixin, RequestMixin


class FlowJsonResponse(JsonResponse):
    def __init__(self, success: bool = True, result: Dict = None, errors: Dict = None):
        response = {
            "success": success,
            "result": result,
            "errors": errors,
        }
        JsonResponse.__init__(self, data=response, safe=False)

    @staticmethod
    def success(result: Dict = None):
        return FlowJsonResponse(success=True, result=result)

    @staticmethod
    def error(errors: Dict = None):
        return FlowJsonResponse(success=False, errors=errors)


def flow_schema_wrap(request_cls: Type[serializers.BaseSerializer], response_cls: Type[serializers.BaseSerializer]):
    class ResponseWrapper(serializers.Serializer):
        class Meta:
            ref_name = None
        success = serializers.BooleanField()
        result = response_cls()
        errors = request_cls()

    return ResponseWrapper


def flow(
        request_serializer_cls: Type[serializers.BaseSerializer],
        response_serializer_cls: Type[serializers.BaseSerializer] = None,
        pass_user: bool = False,
        pass_request: bool = False,
        data: Callable[[Request], Any] = None,
):
    """
    Декоратор для view, которые реализует флоу на двух сериализаторах. Входные данные вьюшки проходят через `request_serializer_cls`
    и попадают во вью в поле `serializer`. Выходные данные вьюшки сериализуются обратно на клиент через `response_serializer_cls`

    :param request_serializer_cls: класс входного сериализатора
    :param response_serializer_cls: класс выходного сериализатора
    :param pass_user: позволяет прокинуть request.user в конструктор сериализатора
    :param pass_request: позволяет прокинуть request в конструктор сериализатора
    :param data: фабрика для параметра data, которое прокидывается в конструктор request_serializer_cls
    :return:
    """

    def default_data(request: Request):
        return request.data

    if response_serializer_cls is None:
        response_serializer_cls = request_serializer_cls

    if data is None:
        data = default_data

    def decorator(func):
        def wrapper(request: Request, *args, **kwargs):
            serializer_kwargs = {}
            if pass_user or issubclass(request_serializer_cls, UserMixin):
                serializer_kwargs['user'] = request.user

            if pass_request or issubclass(request_serializer_cls, RequestMixin):
                serializer_kwargs['request'] = request

            request_serializer = request_serializer_cls(data=data(request), **serializer_kwargs)

            if request_serializer.is_valid():
                instance = func(request, request_serializer, *args, **kwargs)
                response_serializer = response_serializer_cls(instance)
                return FlowJsonResponse.success(response_serializer.data)
            return FlowJsonResponse.error(request_serializer.errors)

        return wrapper

    return decorator
