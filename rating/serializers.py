from rest_framework import serializers
from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.email')
    post = serializers.ReadOnlyField(source='post.title')

    class Meta:
        model = Review
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        post = self.context.get('post')
        validated_data['user'] = user
        validated_data['post'] = post
        return super().create(validated_data)
