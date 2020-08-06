from django.urls import path
from .views import (
    ShitPublicTimelineView, ListCreateShitView, RetrieveDestroyShitView, UserListView,
    UserDetailView, CreateUserFollow, DestroyUserFollow, CreateDestroyFavorite
)

app_name = 'api'

urlpatterns = [
    path('timeline/', ShitPublicTimelineView.as_view(), name='shit_timeline'),
    path('shits/', ListCreateShitView.as_view(), name='list_create_shit'),
    path('shits/<uuid>', RetrieveDestroyShitView.as_view(), name='retrieve_destroy_shit'),
    path('shits/<uuid>/favourite', CreateDestroyFavorite.as_view(), name='create_destroy_favourite'),
    path('users/', UserListView.as_view(), name='user_list_view'),
    path('users/<username>', UserDetailView.as_view(), name='user_detail'),
    path('follows/', CreateUserFollow.as_view(), name='create_user_follow'),
    path('follows/from/<from_user>/to/<to_user>', DestroyUserFollow.as_view(), name='destroy_user_follow'),
]
