from rest_framework.filters import OrderingFilter
from rest_framework.generics import (ListAPIView, RetrieveAPIView, ListCreateAPIView, RetrieveDestroyAPIView)
from rest_framework.permissions import IsAuthenticated
from django_filters import rest_framework as filters

from ..models import *
from ..permissions import IsShitOwner
from ..serializers import ShitSerializer, CreateShitSerializer, UserSerializer, UserFollowSerializer
from .filters import UserShitFilter, UserFollowingFilter


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

        if user.is_superuser or user.is_staff or user.is_anonymous:
            return Shit.objects.all()

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
    filter_backends = (filters.DjangoFilterBackend, UserFollowingFilter)

    def get_queryset(self):
        return User.objects.exclude(pk=self.request.user.pk)


class UserDetailView(RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = 'username'


class ListCreateUserFollow(ListCreateAPIView):
    serializer_class = UserFollowSerializer

    def get_queryset(self):
        return UserFollow.objects.filter(from_user=self.request.user)


class RetrieveDestroyUserFollow(RetrieveDestroyAPIView):
    serializer_class = UserFollowSerializer

    def get_queryset(self):
        return UserFollow.objects.filter(from_user=self.request.user)
