from rest_framework import serializers

from core.models import Tag, Content


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
