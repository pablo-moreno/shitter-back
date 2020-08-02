from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from django.urls import reverse


class TestChangePassword(APITestCase):
    def setUp(self):
        self.old_password = 'thisistheoldpassword'
        self.username = 'darth.vader'
        self.user = User.objects.create_user(
            username=self.username,
            password=self.old_password,
            email=f'{self.username}@starwars.com'
        )
        self.user.is_active = True
        self.user.save()

    def test_change_password(self):
        new_password = 'IStillHateSand'
        data = {
            'old_password': self.old_password,
            'new_password': new_password,
            'new_password2': new_password,
        }

        self.client.force_login(user=self.user)
        response = self.client.put(reverse('authentication:change-password'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        vader = User.objects.get(username=self.username)
        self.assertTrue(vader.check_password(new_password))

    def test_wrong_password(self):
        new_password = 'IStillHateSand'
        data = {
            'old_password': 'thisisnotthepassword',
            'new_password': new_password,
            'new_password2': new_password,
        }

        self.client.force_login(user=self.user)
        response = self.client.put(reverse('authentication:change-password'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_mismatch(self):
        new_password = 'IStillHateSand'
        data = {
            'old_password': self.old_password,
            'new_password': new_password,
            'new_password2': 'thisisnotthepassword',
        }

        self.client.force_login(user=self.user)
        response = self.client.put(reverse('authentication:change-password'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_insecure_password(self):
        insecure_password = '1234'
        data = {
            'old_password': self.old_password,
            'new_password': insecure_password,
            'new_password2': insecure_password,
        }

        self.client.force_login(user=self.user)
        response = self.client.put(reverse('authentication:change-password'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
