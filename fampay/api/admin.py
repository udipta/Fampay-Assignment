from django.contrib import admin

from .models import *


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Video._meta.fields]
    search_fields = ('published', 'video_id', 'channel_id', 'title', 'id')
    list_filter = ('published',)


@admin.register(VideoThumbNail)
class VideoThumbNailAdmin(admin.ModelAdmin):
    list_display = [field.name for field in VideoThumbNail._meta.fields]
    search_fields = ('video__title', 'video__channel_id', 'video__video_id', 'video__published', 'video__id', 'id')
    list_filter = ('video', 'screen_size')


@admin.register(APIKey)
class APIKeyAdmin(admin.ModelAdmin):
    list_display = [field.name for field in APIKey._meta.fields]
