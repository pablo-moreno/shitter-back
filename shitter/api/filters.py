from rest_framework.filters import BaseFilterBackend


class UserShitFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        username = request.query_params.get('user')

        if not username:
            return queryset

        return queryset.select_related('user').filter(user__username=username)
