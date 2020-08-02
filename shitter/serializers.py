from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Shit, ReShit, UserFollow


class UserSerializer(serializers.ModelSerializer):
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()

    def get_followers_count(self, obj):
        return obj.followers.count()

    def get_following_count(self, obj):
        return obj.following.count()

    class Meta:
        model = User
        fields = ('username', 'followers_count', 'following_count')


class ShitSerializer(serializers.ModelSerializer):
    publish_date = serializers.DateTimeField(required=False)
    user = UserSerializer(read_only=True)
    reshits = serializers.SerializerMethodField()

    def get_reshits(self, obj):
        return ReShit.objects.filter(shit=obj).count()

    class Meta:
        model = Shit
        fields = ('uuid', 'text', 'user', 'publish_date', 'reshits')


class CreateReshitSerializer(serializers.Serializer):
    shit = serializers.PrimaryKeyRelatedField(queryset=Shit.objects.all())


class ReShitSerializer(serializers.ModelSerializer):
    shit = ShitSerializer()
    user = UserSerializer()

    class Meta:
        model = ReShit
        fields = ('shit', 'user', 'date')


class UserFollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFollow
        fields = ('from_user', 'to_user')
