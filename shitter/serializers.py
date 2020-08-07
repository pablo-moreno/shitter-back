from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import serializers

from authentication.serializers import UserProfileSerializer
from utils.fields import UUIDRelatedField, UsernameRelatedField

from .models import Shit, UserFollow, Favourite


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()
    total_shits = serializers.SerializerMethodField()
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    following = serializers.SerializerMethodField()

    def get_total_shits(self, obj):
        return Shit.objects.filter(user=obj).count()

    def get_followers_count(self, obj):
        return obj.followers.count()

    def get_following_count(self, obj):
        return obj.following.count()

    def get_following(self, obj):
        user = self.context.get('request').user

        if user.is_anonymous:
            return False

        return UserFollow.objects.filter(from_user=self.context.get('request').user, to_user=obj).exists()

    class Meta:
        model = User
        fields = (
            'id', 'username', 'first_name', 'profile',
            'total_shits', 'followers_count', 'following_count', 'following'
        )


class BaseShitSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(read_only=True)
    publish_date = serializers.DateTimeField(read_only=True)
    user = UserSerializer(read_only=True)
    reshits = serializers.SerializerMethodField(read_only=True)
    favourites = serializers.SerializerMethodField(read_only=True)
    is_reshit = serializers.SerializerMethodField(read_only=True)
    detail_url = serializers.SerializerMethodField(read_only=True)
    is_mine = serializers.SerializerMethodField(read_only=True)
    is_favourite = serializers.SerializerMethodField(read_only=True)

    def get_detail_url(self, obj):
        return reverse('shitter:api:retrieve_destroy_shit', kwargs={'uuid': str(obj.uuid)})

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

    def get_is_mine(self, obj):
        return obj.user == self.context.get('request').user

    def get_is_favourite(self, obj):
        user = self.context.get('request').user

        if user.is_anonymous:
            return False

        return Favourite.objects.filter(shit=obj, user=user).exists()

    class Meta:
        model = Shit
        fields = (
            'uuid', 'text', 'user', 'publish_date',
            'reshits', 'favourites', 'is_reshit',
            'detail_url', 'is_mine', 'is_favourite',
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
    from_user = UsernameRelatedField(queryset=User.objects.all())
    to_user = UsernameRelatedField(queryset=User.objects.all())

    class Meta:
        model = UserFollow
        fields = ('id', 'from_user', 'to_user')
