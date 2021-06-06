from django.contrib.auth.models import User
from rest_framework.request import Request


class UserMixin:
    user: User

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)


class RequestMixin:
    request: Request

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
