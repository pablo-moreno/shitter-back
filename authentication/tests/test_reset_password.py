from string import ascii_letters, digits
from random import choice

from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from django.urls import reverse

from authentication.serializers import ResetPasswordConfirmSerializer


class TestResetPassword(APITestCase):
    def setUp(self):
        self.username = 'darth.vader'
        self.user = User.objects.create_user(
            username=self.username,
            password='thisistheoldpassword',
            email=f'{self.username}@starwars.com'
        )
        self.new_password = ''.join(choice(ascii_letters + digits) for _ in range(0, 12))

    def test_reset_password(self):
        data = {
            'email': self.user.email,
        }

        response = self.client.post(reverse('authentication:reset-password'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_reset_password_confirm_serializer(self):
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = default_token_generator.make_token(self.user)
        serializer = ResetPasswordConfirmSerializer(data={
            'new_password1': self.new_password,
            'new_password2': self.new_password,
            'uid': uid,
            'token': token,
        })
        self.assertTrue(serializer.is_valid())
        serializer.save()
