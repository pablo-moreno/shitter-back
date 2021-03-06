from rest_framework.filters import BaseFilterBackend

from ..models import UserFollow


class UserShitFilter(BaseFilterBackend):
    """
        Filters the shits by the user who published it
    """
    def filter_queryset(self, request, queryset, view):
        username = request.query_params.get('user')

        if not username:
            return queryset

        return queryset.select_related('user').filter(user__username=username)


class UserFollowingFilter(BaseFilterBackend):
    """
        Filters the users to the ones that the requesting user is following.
    """
    def filter_queryset(self, request, queryset, view):
        if 'following' in request.query_params:
            username = request.query_params.get('following')
            follows = UserFollow.objects.filter(from_user__username=username).values_list('to_user')
            return queryset.filter(pk__in=follows)

        return queryset


class UserFollowersFilter(BaseFilterBackend):
    """
        Filters the users to show only the followers that of the requesting user.
    """
    def filter_queryset(self, request, queryset, view):
        if 'followers' in request.query_params:
            username = request.query_params.get('followers')
            follows = UserFollow.objects.filter(to_user__username=username).values_list('from_user')
            return queryset.filter(pk__in=follows)

        return queryset
