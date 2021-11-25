from rest_framework import serializers
from django.contrib.auth import get_user_model


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    # profile_image = serializers.ImageField(use_url=True)

    class Meta:
        model = get_user_model()
        fields = ('username', 'password', 'email', 'name',)

class UserFollowSerializer(serializers.ModelSerializer):
    following_count = serializers.IntegerField(source='followings.count', read_only=True)
    follower_count = serializers.IntegerField(source='followers.count', read_only=True)
    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'name', 'following_count', 'follower_count')


class ProfileImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('profile_image',)


class UserListSerializer(serializers.ModelSerializer):
    followers_count = serializers.IntegerField(source='followers.count', read_only=True)

    class Meta:
        model = get_user_model()
        fields = ('pk', 'username', 'followers_count')