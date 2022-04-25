from statistics import mode
from django.db import models
from django.conf import settings

class Image(models.Model):
    image = models.ImageField(upload_to='static/img/')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True,
        related_name='user_images'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s"%self.id


class Video(models.Model):
    SOURCES = (
        ('local', 'Local'),
        ('vimeo', 'Vimeo'),
        ('youtube', 'Youtube'),
    )
    
    video = models.FileField(upload_to='static/video/')
    thumbnail = models.ImageField(upload_to='static/img/', blank=True, null=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, 
        blank=True, related_name='user_videos'
    )
    url = models.CharField(max_length=255, blank=True, null=True)
    source = models.CharField(
        choices=SOURCES, max_length=25, blank=True, null=True, default='local'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s"%self.id

