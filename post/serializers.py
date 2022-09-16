from django.db.models import Avg
from rest_framework import serializers
from .models import Favourites, Like, Post, PostImages, Comment


class FavouriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favourites
        fields = ('post',)

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['post'] = PostListSerializer(instance.post).data
        return repr


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImages
        exclude = ('id',)


class CommentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Comment
        fields = ('id', 'body', 'owner', 'post')


class LikeSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Like
        fields = ('owner',)


class PostDetailSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    images = PostImageSerializer(many=True)
    category = serializers.ReadOnlyField(source='category.name')

    class Meta:
        model = Post
        fields = '__all__'

    def is_liked(self, post):
        user = self.context.get('request').user
        return user.liked.filter(post=post).exists()

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        user = self.context.get('request').user
        if user.is_authenticated:
            repr['is_liked'] = self.is_liked(instance)
        repr['likes'] = instance.likes.count()
        repr['comments'] = CommentSerializer(instance.comments.all(), many=True).data
        repr['rating'] = instance.reviews.aggregate(Avg('rating'))['rating__avg']
        repr['reviews'] = instance.reviews.count()
        return repr


class PostListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'preview')


class PostCreateSerializer(serializers.ModelSerializer):
    images = PostImageSerializer(many=True, read_only=False, required=False)

    class Meta:
        model = Post
        fields = ('title', 'body', 'category', 'preview', 'images')

    def create(self, validated_data):
        request = self.context.get('request')
        created_post = Post.objects.create(**validated_data)
        images_data = request.FILES
        images_object = [PostImages(post=created_post, image=image) for image in images_data.getlist('images')]
        PostImages.objects.bulk_create(images_object)
        return created_post
