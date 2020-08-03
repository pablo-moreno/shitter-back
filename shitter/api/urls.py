from django.urls import path
from .views import ListCreateShitView, RetrieveDestroyShitView, UserListView, UserDetailView

app_name = 'shitter_api'

urlpatterns = [
    path('shits/', ListCreateShitView.as_view(), name='list_create_shit'),
    path('shits/<uuid>', RetrieveDestroyShitView.as_view(), name='retrieve_destroy_shit'),
    path('users/', UserListView.as_view(), name='user_list_view'),
    path('users/<username>', UserDetailView.as_view(), name='user_detail'),
]
