from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from django.urls import reverse


class TestRetrieveUpdateUser(APITestCase):
    def setUp(self):
        self.password = 'MayTheForceBeWithU'
        self.username = 'obi-wan'
        self.user = User.objects.create_user(
            username=self.username,
            password=self.password,
            email=f'{self.username}@starwars.com'
        )

    def test_retrieve_user(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('authentication:retrieve-update-me'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_user(self):
        data = {
            'email': 'obiwanrocks@starwars.com',
            'first_name': 'Obi Wan',
            'last_name': 'Kenobi',
        }

        self.client.force_login(self.user)
        response = self.client.put(reverse('authentication:retrieve-update-me'), data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        obi_wan = User.objects.get(id=self.user.id)
        self.assertEqual(obi_wan.email, data.get('email'))
        self.assertEqual(obi_wan.first_name, data.get('first_name'))
        self.assertEqual(obi_wan.last_name, data.get('last_name'))

    def test_cannot_update_username(self):
        data = {
            'username': 'obiwan',
        }

        self.client.force_login(self.user)
        response = self.client.put(reverse('authentication:retrieve-update-me'), data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(self.user.username, data.get('username'))
