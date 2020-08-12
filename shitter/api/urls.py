from django.urls import path
from .views import (
    ShitPublicTimelineView, ListCreateShitView, RetrieveDestroyShitView, UserListView,
    CreateDestroyUserFollow, CreateDestroyFavorite
)

app_name = 'api'

urlpatterns = [
    path('timeline/', ShitPublicTimelineView.as_view(), name='shit_timeline'),
    path('shits/', ListCreateShitView.as_view(), name='list_create_shit'),
    path('shits/<uuid>', RetrieveDestroyShitView.as_view(), name='retrieve_destroy_shit'),
    path('shits/<uuid>/favourite', CreateDestroyFavorite.as_view(), name='create_destroy_favourite'),
    path('users/', UserListView.as_view(), name='user_list_view'),
    path('users/<username>/follow/', CreateDestroyUserFollow.as_view(), name='create_destroy_user_follow'),
]
