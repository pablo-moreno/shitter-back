from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.filters import OrderingFilter
from rest_framework.generics import (
    ListAPIView, ListCreateAPIView, RetrieveAPIView, RetrieveDestroyAPIView,
    CreateAPIView, DestroyAPIView
)
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters import rest_framework as filters
from rest_framework.response import Response

from ..models import *
from ..permissions import IsShitOwner
from ..serializers import (
    ShitSerializer, CreateShitSerializer, UserSerializer, UserFollowSerializer,
    FavouriteSerializer,
)
from .filters import UserShitFilter, UserFollowingFilter, UserFollowersFilter


class ShitPublicTimelineView(ListAPIView):
    serializer_class = ShitSerializer
    permission_classes = (AllowAny, )
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter, UserShitFilter)

    def get_queryset(self):
        return Shit.objects.select_related('user').filter(user__profile__private=False)


class ListCreateShitView(ListCreateAPIView):
    serializer_class = ShitSerializer
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter, UserShitFilter, )
    ordering_fields = ('publish_date', )

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateShitSerializer

        return self.serializer_class

    def get_queryset(self):
        user = self.request.user
        following_users = self.request.user.following.all().values_list('to_user', flat=True)
        return Shit.objects.filter(user__pk__in=[user.pk, *following_users])

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class RetrieveDestroyShitView(RetrieveDestroyAPIView):
    serializer_class = ShitSerializer
    permission_classes = (IsAuthenticated, IsShitOwner, )
    lookup_field = 'uuid'

    def get_queryset(self):
        if self.request.method == 'GET':
            return Shit.objects.all()
        elif self.request.method == 'DELETE':
            return Shit.objects.filter(user=self.request.user)


class UserListView(ListAPIView):
    serializer_class = UserSerializer
    filter_backends = (filters.DjangoFilterBackend, UserFollowingFilter, UserFollowersFilter, )

    def get_queryset(self):
        return User.objects.exclude(pk=self.request.user.pk)


class UserDetailView(RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = 'username'


class CreateDestroyUserFollow(CreateAPIView, DestroyAPIView):
    serializer_class = UserFollowSerializer

    def create(self, request, *args, **kwargs):
        to_username = kwargs.get('username')
        to_user = User.objects.get(username=to_username)
        try:
            follow = UserFollow.objects.create(
                from_user=request.user,
                to_user=to_user
            )
            data = self.serializer_class(follow).data

            return Response(data=data, status=status.HTTP_201_CREATED)
        except IntegrityError as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        to_user = kwargs.get('username')
        follow = get_object_or_404(
            UserFollow.objects.all(),
            from_user__username=request.user,
            to_user__username=to_user
        )
        self.perform_destroy(follow)

        return Response(status=status.HTTP_204_NO_CONTENT)


class CreateDestroyFavorite(CreateAPIView, DestroyAPIView):
    def create(self, request, *args, **kwargs):
        uuid = kwargs.get('uuid')
        shit = get_object_or_404(Shit.objects.all(), uuid=uuid)
        favourite = Favourite.objects.create(shit=shit, user=request.user)

        return Response(status=status.HTTP_201_CREATED, data=FavouriteSerializer(favourite).data)

    def destroy(self, request, *args, **kwargs):
        uuid = kwargs.get('uuid')
        favourite = get_object_or_404(Favourite.objects.all(), shit__uuid=uuid, user=request.user)
        self.perform_destroy(favourite)

        return Response(status=status.HTTP_204_NO_CONTENT)
