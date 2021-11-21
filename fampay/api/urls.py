from django.urls import path, include

from .services import service_thread
from .views import APIKeyViewset, VideosViewset

from rest_framework import routers

router = routers.DefaultRouter()
router.register('add_key', APIKeyViewset, basename='add_key')
router.register('get_videos', VideosViewset, basename='get_videos')

urlpatterns = [
    path('', include(router.urls)),
]

service_thread.start()
