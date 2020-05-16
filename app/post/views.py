from rest_framework import viewsets, mixins, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

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
        elif self.action == 'upload_image':
            return serializers.PostImageSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        """Create new object"""
        serializer.save(user=self.request.user)

    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """Upload an image to a post"""
        post = self.get_object()
        serializer = self.get_serializer(
            post,
            data=request.data
        )

        if serializer.is_valid():

            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
