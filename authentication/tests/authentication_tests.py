from rest_framework.test import APITestCase
from django.urls import reverse


class AuthenticationTestCase(APITestCase):
    def authenticate(self, username, password):
        data = {
            'username': username,
            'password': password,
        }
        response = self.client.post(reverse('authentication:login'), data=data)
        token = response.json().get('token')
        return token
