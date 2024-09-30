from rest_framework import serializers
from ..models import Post, Comment


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'slug', 'author', 'publish', 'status', 'content', 'new_field']


class PostTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'slug']


class SharePostSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=25)
    email = serializers.EmailField()
    to = serializers.EmailField()
    comments = serializers.CharField(required=False, allow_blank=True)