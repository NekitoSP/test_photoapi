from django.http import HttpResponse
from rest_framework.exceptions import APIException, NotAuthenticated

from photos.api.utils.flow import FlowJsonResponse


def custom_exception_handler(exc, context):
    if isinstance(exc, NotAuthenticated):
        return HttpResponse(status=401)
    if isinstance(exc, APIException):
        return FlowJsonResponse.error({
            'code': exc.status_code,
            'detail': exc.detail,
        })
    else:
        return HttpResponse(exc, status=500)
