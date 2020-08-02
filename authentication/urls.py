from django.urls import path
from .views import (
    login, verify_jwt_token, refresh_jwt_token,
    sign_up, retrieve_update_me, delete_account, change_password,
    password_reset, password_reset_confirm, retrieve_update_user_profile,
    change_profile_picture,
)

app_name = 'authentication'

urlpatterns = (
    path('login', login, name='login'),
    path('sign-up', sign_up, name='sign-up'),
    path('me', retrieve_update_me, name='retrieve-update-me'),
    path('me/profile', retrieve_update_user_profile, name='retrieve-update-user-profile'),
    path('me/profile/picture', change_profile_picture, name='change-profile-picture'),
    path('account/delete', delete_account, name='delete-account'),
    path('password/change', change_password, name='change-password'),
    path('password/reset', password_reset, name='reset-password'),
    path('password/reset/confirm', password_reset_confirm, name='password_reset_confirm'),
    path('token/verify', verify_jwt_token, name='verify-jwt-token'),
    path('token/refresh', refresh_jwt_token, name='refresh-jwt-token'),
)
