from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveDestroyAPIView, get_object_or_404
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Shit, ReShit, Favourite
from ..permissions import IsShitOwner
from ..serializers import ShitSerializer


class ListCreateShitView(ListCreateAPIView):
    serializer_class = ShitSerializer
    filter_backends = (OrderingFilter, )
    ordering_fields = ('-publish_date', )

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


class ReShitView(APIView):
    def post(self, request, uuid, *args, **kwargs):
        shit = get_object_or_404(Shit.objects.all(), uuid=uuid)
        reshit = ReShit.objects.create(
            user=request.user,
            shit=shit
        )
        return Response(status=status.HTTP_201_CREATED)


class FavouriteShitView(APIView):
    def post(self, request, uuid, *args, **kwargs):
        shit = get_object_or_404(Shit.objects.all(), uuid=uuid)
        favourite = Favourite.objects.create(
            user=request.user,
            shit=shit,
        )
        return Response(status=status.HTTP_201_CREATED)
