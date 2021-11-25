from rest_framework import serializers
from .models import Review, Comment
from django.contrib.auth import get_user_model


class CommentSerializer(serializers.ModelSerializer):
    like_count = serializers.IntegerField(source='like_users.count', read_only=True)
    class UserSerializer(serializers.ModelSerializer):

        class Meta:
            model = get_user_model()
            fields = ('username',)
    user = UserSerializer(read_only=True)
    like_users = UserSerializer(many=True, read_only=True)
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('review', 'like_users', 'user', 'like_count')


class ReviewListSerializer(serializers.ModelSerializer):
    comment_set = CommentSerializer(many=True, read_only=True)
    like_count = serializers.IntegerField(source='like_users.count', read_only=True)
    comment_count = serializers.IntegerField(source='comment_set.count',read_only=True)
    class Meta:
        model = Review
        fields = ('pk', 'watched_at', 'quote', 'oneline_review', 'like_count', 'thumbnail_path', 'movie_title', 'rank', 'content', 'like_users', 'comment_set', 'created_at', 'comment_count', 'is_private')



class ReviewSerializer(serializers.ModelSerializer):
    
    comment_set = CommentSerializer(many=True, read_only=True)
    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('user', 'like_users',)


class ReviewRecommendSerializer(serializers.ModelSerializer):
    class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model = get_user_model()
            fields = ('username',)
            
    comment_set = CommentSerializer(many=True, read_only=True)
    user = UserSerializer(read_only=True)
    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('user', 'like_users',)

class ReviewQuoteSerializer(serializers.ModelSerializer):
    class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model = get_user_model()
            fields = ('username',)
    user = UserSerializer(read_only=True)
    class Meta:
        model = Review
        fields = ('quote', )