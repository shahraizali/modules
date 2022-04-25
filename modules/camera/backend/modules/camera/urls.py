
from django.urls import path, include
from rest_framework import routers

from .viewsets import ImageViewSet, VideoViewSet, ImageUploadView, VideoUploadView, UserWallView


router = routers.DefaultRouter()
router.register(r'photos/user', ImageViewSet)
router.register(r'videos/user', VideoViewSet)
urlpatterns = [
    path('', include(router.urls)),
    path('upload_image/', ImageUploadView.as_view()),
    path('upload_video/', VideoUploadView.as_view()),
    path('user_wall/', UserWallView.as_view()),
]