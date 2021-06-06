from rest_framework import serializers

from photos.models import Photo


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        ref_name = None
        model = Photo
        fields = ('id', 'photo', 'comment', 'created_date')