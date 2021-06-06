"""photoapi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi

from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny

swagger_info = openapi.Info(
    title="PhotoApi",
    default_version='v1',
    description="""Проект текстового задания""",  # noqa
    contact=openapi.Contact(email="nekitosp@gmail.com"),
)

SchemaView = get_schema_view(
    # validators=['ssv', 'flex'],
    public=True,
    permission_classes=[AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('swagger/', SchemaView.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/photos/', include('photos.api.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
