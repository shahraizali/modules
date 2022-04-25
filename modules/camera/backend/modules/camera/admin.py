from django.contrib import admin
from .models import Image, Video

class ImageAdmin(admin.ModelAdmin):
    pass

class VideoAdmin(admin.ModelAdmin):
    pass

admin.site.register(Image, ImageAdmin)
admin.site.register(Video, VideoAdmin)