from django.conf import settings
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.cache import cache

MAX_LOGIN_RETRIES = getattr(settings, 'MAX_LOGIN_RETRIES', 10)


class TestLogin(APITestCase):
    def setUp(self):
        self.username = 'r2d2'
        self.password = 'BipBipBip'
        self.email = f'{self.username}@starwars.com'
        self.user = User.objects.create_user(
            username=self.username,
            password=self.password,
            email=self.email
        )

    def test_login_ok(self):
        user = {
            'username': self.username,
            'password': self.password,
        }

        response = self.client.post(reverse('authentication:login'), data=user, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_error(self):
        user = {
            'username': self.username,
            'password': 'wrong password'
        }
        response = self.client.post(reverse('authentication:login'), data=user, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_inactive_user(self):
        self.user.is_active = False
        self.user.save()

        user = {
            'username': self.username,
            'password': self.password,
        }

        response = self.client.post(reverse('authentication:login'), data=user, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_exceed_max_login_retries(self):
        key = f'LOGIN_RETRIES_{self.username}'

        user = {
            'username': self.username,
            'password': 'wrong password',
        }
        last_status = None
        for _ in range(0, MAX_LOGIN_RETRIES + 2):
            response = self.client.post(reverse('authentication:login'), data=user, format='json')
            last_status = response.status_code

        self.assertEqual(last_status, status.HTTP_403_FORBIDDEN)
        self.assertGreater(cache.get(key), MAX_LOGIN_RETRIES)
        cache.set(key, 0)
