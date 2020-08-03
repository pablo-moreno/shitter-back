from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.cache import cache
from django.utils.encoding import force_text
from rest_framework import serializers
from django.utils.http import urlsafe_base64_decode as uid_decoder
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password, get_password_validators
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from rest_framework_jwt.serializers import JSONWebTokenSerializer

from .models import UserProfile
from .settings import (
    MAX_LOGIN_RETRIES, SET_USER_INACTIVE_AFTER_MAX_LOGIN_RETRIES,
    EMAIL_RESET_PASSWORD_TEMPLATE_NAME, HTML_EMAIL_RESET_PASSWORD_TEMPLATE_NAME,
    SUBJECT_EMAIL_RESET_PASSWORD_NAME,
)

AUTH_PASSWORD_VALIDATORS = getattr(settings, 'AUTH_PASSWORD_VALIDATORS')


class LoginSerializer(JSONWebTokenSerializer):
    def validate(self, attrs):
        username = attrs.get('username')
        key = f'LOGIN_RETRIES_{username}'

        try:
            validated_data = super().validate(attrs)
            cache.set(key, 0)
            return validated_data
        except Exception as e:
            cache.set(key, cache.get(key, 0) + 1)

            if SET_USER_INACTIVE_AFTER_MAX_LOGIN_RETRIES and cache.get(key, 0) > MAX_LOGIN_RETRIES:
                self.set_user_as_inactive(username)

            raise serializers.ValidationError(e.args)

    def set_user_as_inactive(self, username):
        user = User.objects.get(username=username)
        user.is_active = False
        user.save()


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = (
            'profile_picture',
            'private',
        )


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)

    def get_profile(self, user):
        profile = UserProfile.objects.get(user=user)
        return profile

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'profile', )
        read_only_fields = ('username', 'profile', )


class CreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def validate_password(self, password) -> str:
        password2 = self.context.get('request').data.get('password2')
        if password != password2:
            raise ValidationError('Password mismatch')

        validate_password(password, password_validators=get_password_validators(AUTH_PASSWORD_VALIDATORS))
        return password

    def create(self, validated_data: dict) -> User:
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        UserProfile.objects.create(user=user)
        return user

    class Meta:
        model = User
        fields = (
            'username', 'password', 'password2', 'email',
            'first_name', 'last_name',
        )


class UpdatePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    new_password2 = serializers.CharField(write_only=True)

    def validate_old_password(self, password):
        user = self.context.get('request').user

        if not user.check_password(password):
            raise ValidationError('Wrong old password')

        return password

    def validate_new_password(self, password):
        old_password = self.context.get('request').data.get('old_password')

        if password == old_password:
            raise ValidationError('Password can\'t be the same as the old one')

        password2 = self.context.get('request').data.get('new_password2')
        if password != password2:
            raise ValidationError('Password mismatch')

        validate_password(password, password_validators=get_password_validators(AUTH_PASSWORD_VALIDATORS))

        return password

    def save(self, *args, **kwargs):
        new_password = self.validated_data.get('new_password')
        self.instance.set_password(new_password)
        self.instance.save()

    class Meta:
        model = User
        fields = ('old_password', 'new_password', 'new_password2', )


class ResetPasswordSerializer(serializers.Serializer):
    """
    Serializer for requesting a password reset e-mail.
    """
    email = serializers.EmailField()
    password_reset_form_class = PasswordResetForm

    def get_email_options(self):
        return {
            'extra_email_context': {},
            'email_template_name': EMAIL_RESET_PASSWORD_TEMPLATE_NAME,
            'html_email_template_name': HTML_EMAIL_RESET_PASSWORD_TEMPLATE_NAME,
            'subject_template_name': SUBJECT_EMAIL_RESET_PASSWORD_NAME,
        }

    def validate_email(self, value):
        # Create PasswordResetForm with the serializer
        self.reset_form = self.password_reset_form_class(data=self.initial_data)
        if not self.reset_form.is_valid():
            raise serializers.ValidationError(self.reset_form.errors)

        return value

    def save(self):
        request = self.context.get('request')

        opts = {
            'use_https': request.is_secure(),
            'from_email': getattr(settings, 'DEFAULT_FROM_EMAIL'),
            'request': request,
        }

        opts.update(self.get_email_options())
        self.reset_form.save(**opts)


class ResetPasswordConfirmSerializer(serializers.Serializer):
    """
        Serializer for requesting a password reset e-mail.
    """
    new_password1 = serializers.CharField(max_length=128)
    new_password2 = serializers.CharField(max_length=128)
    uid = serializers.CharField()
    token = serializers.CharField()

    set_password_form_class = SetPasswordForm

    def custom_validation(self, attrs):
        pass

    def validate(self, attrs):
        uid = attrs.get('uid')

        try:
            uid = force_text(uid_decoder(uid))
            self.user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise ValidationError({'uid': ['Invalid value']})

        self.custom_validation(attrs)

        self.set_password_form = self.set_password_form_class(
            user=self.user, data=attrs
        )

        if not self.set_password_form.is_valid():
            raise serializers.ValidationError(self.set_password_form.errors)
        if not default_token_generator.check_token(self.user, attrs['token']):
            raise ValidationError({'token': ['Invalid value']})

        return attrs

    def save(self):
        return self.set_password_form.save()


class ProfilePictureSerializer(serializers.Serializer):
    profile_picture = serializers.ImageField()

    def validate(self, attrs):
        return attrs
