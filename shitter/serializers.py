from django.contrib.auth.models import User
from rest_framework import serializers

from authentication.serializers import UserProfileSerializer
from utils.fields import UUIDRelatedField

from .models import Shit, UserFollow


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()
    total_shits = serializers.SerializerMethodField()
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()

    def get_total_shits(self, obj):
        return Shit.objects.filter(user=obj).count()

    def get_followers_count(self, obj):
        return obj.followers.count()

    def get_following_count(self, obj):
        return obj.following.count()

    class Meta:
        model = User
        fields = ('username', 'profile', 'total_shits', 'followers_count', 'following_count')


class BaseShitSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(read_only=True)
    publish_date = serializers.DateTimeField(read_only=True)
    user = UserSerializer(read_only=True)
    reshits = serializers.SerializerMethodField(read_only=True)
    favourites = serializers.SerializerMethodField(read_only=True)
    is_reshit = serializers.SerializerMethodField(read_only=True)

    def get_reshit(self, obj):
        if obj.reshit is None:
            return None

        return ShitSerializer(obj.reshit).data

    def get_reshits(self, obj):
        return Shit.objects.filter(reshit=obj).count()

    def get_favourites(self, obj):
        return obj.favourites.count()

    def get_is_reshit(self, obj):
        return obj.reshit is not None

    class Meta:
        model = Shit
        fields = (
            'uuid', 'text', 'user', 'publish_date',
            'reshits', 'favourites', 'is_reshit',
        )


class ReShitSerializer(BaseShitSerializer):
    class Meta:
        model = Shit
        fields = (
            'uuid', 'text', 'publish_date', 'user',
        )


class ShitSerializer(BaseShitSerializer):
    reshit = ReShitSerializer(required=False)

    class Meta:
        model = Shit
        fields = BaseShitSerializer.Meta.fields + (
            'reshit',
        )


class CreateShitSerializer(ShitSerializer):
    reshit = UUIDRelatedField(required=False, queryset=Shit.objects.all())


class UserFollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFollow
        fields = ('from_user', 'to_user')
