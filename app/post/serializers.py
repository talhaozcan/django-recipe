from rest_framework import serializers

from core.models import Tag, Content, Post


class TagSerializer(serializers.ModelSerializer):
    """Serializer for Tag obj"""

    class Meta():
        model = Tag
        fields = ('id', 'name',)
        read_only_fields = ('id',)


class ContentSerializer(serializers.ModelSerializer):
    """Serializer for post content"""

    class Meta():
        model = Content
        fields = ('id', 'title', 'text',)
        read_only_fields = ('id',)


class PostSerializer(serializers.ModelSerializer):
    """Serializer for post"""

    contents = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Content.objects.all()
    )

    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )

    class Meta():
        model = Post
        fields = ('id', 'post_title', 'contents', 'tags')
        read_only_fields = ('id',)


class PostDetailSerializer(PostSerializer):
    """Serializer for post detail"""

    contents = ContentSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
