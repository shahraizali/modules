from .models import Image, Video
from rest_framework import serializers


class ImageSerializer(serializers.HyperlinkedModelSerializer):
    image = serializers.SerializerMethodField()

    def get_image(self, obj):
        return obj.image.url

    class Meta:
        model = Image
        fields = (
            "id",
            "image",
            "created_at",
        )


class VideoSerializer(serializers.HyperlinkedModelSerializer):
    video = serializers.SerializerMethodField()

    def get_video(self, obj):
        return obj.video.url

    class Meta:
        model = Video
        fields = (
            "id",
            "video",
            "created_at",
            "source"
        )


class ImageUploadSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()

    class Meta:
        model = Image
        fields = ("image",)


class VideoUploadSerializer(serializers.ModelSerializer):
    video = serializers.FileField()

    class Meta:
        model = Video
        fields = ("video",)