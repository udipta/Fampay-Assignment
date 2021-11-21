"""This module contains serializers for Video and VideoThumbNail models."""

from rest_framework import serializers
from .models import *


class VideoSerializer(serializers.ModelSerializer):
    """ Serializer for Video Model. """
    thumbnails = serializers.SerializerMethodField()

    @staticmethod
    def get_thumbnails(obj):
        """
        Returns all thumbnails of the video.
        ---
        Returns:
            list: List of thumbnails dict.
        """
        return [VideoThumbNailSerializer(thumbnail).data for thumbnail in VideoThumbNail.objects.filter(video=obj)]

    class Meta:
        model = Video
        fields = '__all__'


class VideoThumbNailSerializer(serializers.ModelSerializer):
    """ Serializer for VideoThumbNail Model. """

    class Meta:
        model = VideoThumbNail
        fields = '__all__'


class APIKeySerializer(serializers.ModelSerializer):
    """ Serializer for APIKey Model. """

    class Meta:
        model = APIKey
        fields = '__all__'
