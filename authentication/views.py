from typing import Any

from django.utils.translation import gettext as _
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, UpdateAPIView, RetrieveUpdateAPIView, GenericAPIView, \
    get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser
from rest_framework_jwt.views import (
    ObtainJSONWebToken, VerifyJSONWebToken, RefreshJSONWebToken
)
from .models import UserProfile
from .permissions import CanCreateNewUser, IsUserActive, MaxPasswordRetries
from .serializers import (
    UserSerializer, CreateUserSerializer, UpdatePasswordSerializer,
    ResetPasswordSerializer, ResetPasswordConfirmSerializer, UserProfileSerializer,
    LoginSerializer, ProfilePictureSerializer
)


class Login(ObtainJSONWebToken):
    """
        post: Login user and obtain JWT Token
    """
    permission_classes = (MaxPasswordRetries, )
    serializer_class = LoginSerializer


class RetrieveUpdateMe(RetrieveUpdateAPIView):
    """
        get: Return user info

        put: Update user info
    """
    permission_classes = (IsAuthenticated, )
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class RetrieveUpdateUserProfile(RetrieveUpdateAPIView):
    """
        get: Return user profile info

        put: Update user profile info
    """
    permission_classes = (IsAuthenticated, )
    serializer_class = UserProfileSerializer

    def get_object(self):
        return get_object_or_404(UserProfile.objects.filter(user=self.request.user))


class SignUp(CreateAPIView):
    """
        post: Register a new user
    """
    serializer_class = CreateUserSerializer
    permission_classes = (CanCreateNewUser, )


class ChangePassword(UpdateAPIView):
    """
        put: Update user's password
    """
    serializer_class = UpdatePasswordSerializer
    permission_classes = (IsAuthenticated, IsUserActive, )

    def get_object(self):
        return self.request.user


class DeleteAccount(APIView):
    """
        post: Delete account
    """
    permission_classes = (IsAuthenticated, IsUserActive, )

    def post(self, request):
        user = request.user
        user.is_active = False
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PasswordReset(GenericAPIView):
    serializer_class = ResetPasswordSerializer
    permission_classes = (AllowAny, )

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()
        # Return the success message with OK HTTP status
        return Response(
            {"detail": _("Password reset e-mail has been sent.")},
            status=status.HTTP_200_OK
        )


class PasswordResetConfirm(GenericAPIView):
    permission_classes = (AllowAny, )
    serializer_class = ResetPasswordConfirmSerializer


class ChangeProfilePicture(CreateAPIView):
    parser_classes = (MultiPartParser, )
    permission_classes = (IsAuthenticated, )
    serializer_class = ProfilePictureSerializer

    def post(self, request: Request, *args: Any, **kwargs: Any):
        try:
            profile_picture = request.FILES['profile_picture']
            user = self.request.user
            user.profile.profile_picture = profile_picture
            user.profile.save()

            return Response(status=status.HTTP_201_CREATED)
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)


login = Login.as_view()
sign_up = SignUp.as_view()
delete_account = DeleteAccount.as_view()

verify_jwt_token = VerifyJSONWebToken.as_view()
refresh_jwt_token = RefreshJSONWebToken.as_view()

retrieve_update_me = RetrieveUpdateMe.as_view()
retrieve_update_user_profile = RetrieveUpdateUserProfile.as_view()
change_profile_picture = ChangeProfilePicture.as_view()

change_password = ChangePassword.as_view()
password_reset = PasswordReset.as_view()
password_reset_confirm = PasswordResetConfirm.as_view()
