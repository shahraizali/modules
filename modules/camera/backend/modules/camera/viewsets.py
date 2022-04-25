from .models import Image, Video
from .serializers import ImageSerializer, ImageUploadSerializer, VideoSerializer, VideoUploadSerializer
from rest_framework import viewsets
from rest_framework.parsers import FileUploadParser
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from itertools import chain


class ImageViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    http_method_names = ["get"]


class VideoViewSet(viewsets.ModelViewSet):
	"""
	A simple ViewSet for viewing and editing accounts.
	"""
	queryset = Video.objects.all()
	serializer_class = VideoSerializer
	http_method_names = ["get"]


class ImageUploadView(APIView):
	parser_class = (FileUploadParser,)
	
	def post(self, request, *args, **kwargs):
		image_serializer = ImageUploadSerializer(data=request.data, partial=True)
		try:
			if image_serializer.is_valid(raise_exception=True):
				image_serializer.save()
				return Response(image_serializer.data, status=status.HTTP_201_CREATED)
			else:
				return Response(image_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
		except Exception as e:
			return Response(e.args[0], status=status.HTTP_400_BAD_REQUEST)


class VideoUploadView(APIView):
	parser_class = (FileUploadParser,)
	
	def post(self, request, *args, **kwargs):
		video_serializer = VideoUploadSerializer(data=request.data, partial=True)
		try:
			if video_serializer.is_valid(raise_exception=True):
				video_serializer.save()
				return Response(video_serializer.data, status=status.HTTP_201_CREATED)
			else:
				return Response(video_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
		except Exception as e:
			return Response(e.args[0], status=status.HTTP_400_BAD_REQUEST)


class UserWallView(APIView):
	def get(self, request, *args, **kwargs):
		user = request.user
		if user.id:
			user_images = Image.objects.filter(user=user)
			user_videos = Video.objects.filter(user=user)
		else:
			user_images = []
			user_videos = []
		public_images = Image.objects.filter(user=None)
		public_videos = Video.objects.filter(user=None)
		images = chain(user_images, public_images)
		videos = chain(user_videos, public_videos)
		
		serialized_images = ImageSerializer(images, many=True).data
		serialized_videos = VideoSerializer(videos, many=True).data

		# merge images and videos keys in data
		all_data = serialized_images + serialized_videos
		# sort data by created_at
		all_data = sorted(all_data, key=lambda k: k['created_at'])

		return Response(all_data)