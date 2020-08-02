from rest_framework.test import APITestCase
from rest_framework import status
from django.apps import apps
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.cache import cache
from django.conf import settings

UserProfile = apps.get_model('authentication', 'UserProfile')
AUTH_SIGN_UP_BY_IP_LIMIT = getattr(settings, 'AUTH_SIGN_UP_BY_IP_LIMIT', 10)


class TestSignUp(APITestCase):
    def setUp(self):
        self.password = '34toirgnsdfokg'
        self.insecure_password = '1234'

    def test_create_user_ok(self):
        user = {
            'username': 'luke',
            'password': self.password,
            'password2': self.password,
            'email': 'luke.skywalker@starwars.com'
        }

        response = self.client.post(reverse('authentication:sign-up'), data=user, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        luke = User.objects.get(username='luke')
        self.assertIsNotNone(luke)

    def test_password_mismatch(self):
        user = {
            'username': 'leia',
            'password': self.password,
            'password2': 'thisisdefinatelynotthepassword',
            'email': 'leia.organa@starwars.com',
        }
        response = self.client.post(reverse('authentication:sign-up'), data=user, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        body = response.json()
        password_errors = body.get('password')
        self.assertIsNotNone(password_errors)
        self.assertGreater(len(password_errors), 0)
        self.assertIn('Password mismatch', password_errors)

    def test_insecure_password(self):
        user = {
            'username': 'han',
            'password': self.insecure_password,
            'password2': self.insecure_password,
            'email': 'han.solo@starwars.com',
        }
        response = self.client.post(reverse('authentication:sign-up'), data=user, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_it_has_created_user_profile(self):
        user = {
            'username': 'vader',
            'password': self.password,
            'password2': self.password,
            'email': 'vader@starwars.com'
        }

        response = self.client.post(reverse('authentication:sign-up'), data=user, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        vader = User.objects.get(username='vader')
        self.assertIsNotNone(vader)
        user_profile = UserProfile.objects.get(user=vader)
        self.assertIsNotNone(user_profile)

    def test_cannot_create_x_users_from_same_ip(self):
        cache_key = 'SIGN_UP_127.0.0.1'
        statuses = []
        for i in range(0, AUTH_SIGN_UP_BY_IP_LIMIT * 2):
            user = {
                'username': f'user_{i}',
                'password': self.password,
                'password2': self.password,
                'email': f'user_{i}@starwars.com'
            }
            response = self.client.post(reverse('authentication:sign-up'), data=user)
            statuses.append(response.status_code)

        self.assertIn(status.HTTP_401_UNAUTHORIZED, statuses)

        tries = cache.get(cache_key, {}).get('tries')
        self.assertEqual(tries, AUTH_SIGN_UP_BY_IP_LIMIT)
        cache.set(cache_key, {})
