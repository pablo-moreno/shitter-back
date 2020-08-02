from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from django.urls import reverse


class TestDeleteAccount(APITestCase):
    def setUp(self):
        self.username = 'bobafett'
        self.password = 'IloveMyJetpack'
        self.user = User.objects.create_user(
            username=self.username,
            password=self.password,
            email=f'{self.username}@starwars.com',
        )
        self.user.is_active = True
        self.user.save()

    def test_delete_user(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('authentication:delete-account'))
        self.assertEqual(response.content, b'')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        boba = User.objects.get(id=self.user.id)
        self.assertFalse(boba.is_active)
