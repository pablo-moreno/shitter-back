from django.urls import reverse
from django.conf import settings
from rest_framework.test import APITestCase
from rest_framework.status import HTTP_200_OK


class TestHealthCheck(APITestCase):
    def test_healthcheck(self):
        response = self.client.get(reverse(viewname='healthy'))
        assert response.status_code == HTTP_200_OK

        data = response.json()
        self.assertEqual(data.get('alive'), True)
        self.assertIsNotNone(data.get('host'))
        self.assertEqual(data.get('version'), getattr(settings, 'VERSION'))
        self.assertIsNotNone(data.get('ip'))
