from multiprocessing import context
from rest_framework import viewsets
from .models import (
    Chat,
    DownvotePost,
    FollowRequest,
    LikeComment,
    Post,
    PostComment,
    PostMedia,
    ReportPost,
    UpvotePost,
)
from .serializers import (
    ChatSerializer,
    DownvotePostSerializer,
    FollowRequestSerializer,
    LikeCommentSerializer,
    PostSerializer,
    PostCommentSerializer,
    PostMediaSerializer,
    ReportPostSerializer,
    UpvotePostSerializer,
    PostDetailSerializer
)
from rest_framework import authentication
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostDetailSerializer
    authentication_classes = (
        authentication.SessionAuthentication,
        authentication.TokenAuthentication,
    )
    queryset = Post.objects.all()


    # override serializer_class to filter by user
    def get_serializer_class(self):
        if self.action == 'list':
            return PostSerializer
        else:
            return PostDetailSerializer

    # detail view
    def retrieve(self, request, pk=None):
        queryset = self.get_queryset()
        post = queryset.get(pk=pk)
        serializer = self.get_serializer(post, context={'request': request})
        return Response(serializer.data)

class PostMediaViewSet(viewsets.ModelViewSet):
    serializer_class = PostMediaSerializer
    authentication_classes = (
        authentication.SessionAuthentication,
        authentication.TokenAuthentication,
    )
    queryset = PostMedia.objects.all()


class ReportPostViewSet(viewsets.ModelViewSet):
    serializer_class = ReportPostSerializer
    authentication_classes = (
        authentication.SessionAuthentication,
        authentication.TokenAuthentication,
    )
    queryset = ReportPost.objects.all()


class FollowRequestViewSet(viewsets.ModelViewSet):
    serializer_class = FollowRequestSerializer
    authentication_classes = (
        authentication.SessionAuthentication,
        authentication.TokenAuthentication,
    )
    queryset = FollowRequest.objects.all()


class PostCommentViewSet(viewsets.ModelViewSet):
    serializer_class = PostCommentSerializer
    authentication_classes = (
        authentication.SessionAuthentication,
        authentication.TokenAuthentication,
    )
    queryset = PostComment.objects.all()


class LikeCommentViewSet(viewsets.ModelViewSet):
    serializer_class = LikeCommentSerializer
    authentication_classes = (
        authentication.SessionAuthentication,
        authentication.TokenAuthentication,
    )
    queryset = LikeComment.objects.all()


class UpvotePostViewSet(viewsets.ModelViewSet):
    serializer_class = UpvotePostSerializer
    authentication_classes = (
        authentication.SessionAuthentication,
        authentication.TokenAuthentication,
    )
    queryset = UpvotePost.objects.all()


class DownvotePostViewSet(viewsets.ModelViewSet):
    serializer_class = DownvotePostSerializer
    authentication_classes = (
        authentication.SessionAuthentication,
        authentication.TokenAuthentication,
    )
    queryset = DownvotePost.objects.all()


class ChatViewSet(viewsets.ModelViewSet):
    serializer_class = ChatSerializer
    authentication_classes = (
        authentication.SessionAuthentication,
        authentication.TokenAuthentication,
    )
    queryset = Chat.objects.all()