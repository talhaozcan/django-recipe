from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tag, Content, Post
from post import serializers


class BaseViewSet(viewsets.GenericViewSet,
                  mixins.ListModelMixin,
                  mixins.CreateModelMixin):
    """Base viewset"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        """Create new object"""
        serializer.save(user=self.request.user)


class TagViewSet(BaseViewSet):
    """Manage tags in db"""

    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer

    def get_queryset(self):
        """Get tags for authenticated user's only"""
        return self.queryset.filter(user=self.request.user).order_by('-name')


class ContentViewSet(BaseViewSet):
    """Manage post contents"""
    queryset = Content.objects.all()
    serializer_class = serializers.ContentSerializer

    def get_queryset(self):
        """Get tags for authenticated user's only"""
        return self.queryset.filter(user=self.request.user).order_by('-title')


class PostViewSet(viewsets.ModelViewSet):
    """Manage posts"""
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Get posts for authenticated user's only"""
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == 'retrieve':
            return serializers.PostDetailSerializer
        return self.serializer_class
