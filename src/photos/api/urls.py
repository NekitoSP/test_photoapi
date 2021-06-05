from django.urls import path

from photos.api.authenticate import authenticate_view
from photos.api.get_photos import get_photos
from photos.api.update_photo import update_photo
from photos.api.upload_photo import upload_photo

urlpatterns = [
    path('uploadPhoto/', upload_photo),
    path('authenticate/', authenticate_view),
    path('getPhotos/', get_photos),
    path('updatePhoto/', update_photo),
]
