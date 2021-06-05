from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import UserPhoto


class UserPhotoInline(admin.StackedInline):
    model = UserPhoto
    can_delete = False


class UserAdmin(BaseUserAdmin):
    inlines = (UserPhotoInline,)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
