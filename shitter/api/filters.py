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
        Filters the users to the ones that the request user is following.
    """
    def filter_queryset(self, request, queryset, view):
        if 'following' in request.query_params:
            follows = UserFollow.objects.filter(from_user=request.user).values_list('to_user')
            return queryset.filter(pk__in=follows)

        return queryset
