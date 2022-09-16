from rest_framework import serializers
from .models import Category
from post.serializers import PostListSerializer


class CategorySerializer(serializers.ModelSerializer):
    slug = serializers.ReadOnlyField()

    class Meta:
        model = Category
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['post'] = PostListSerializer(instance.posts.all(), many=True).data
        return representation
