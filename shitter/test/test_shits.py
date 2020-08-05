from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from shitter.models import Shit
from utils.tests import AuthTestCaseMixin


class TestShits(APITestCase, AuthTestCaseMixin):
    fixtures = ('users', 'profiles', 'shits', 'followers', )

    def setUp(self):
        self.username = 'pablo'
        self.password = 'iamrandomuser'
        self.user = User.objects.get(username=self.username)
        self.perform_authentication(self.username, self.password)

    def test_can_see_shits(self):
        shits = Shit.objects.filter(user__in=[self.user.pk, *self.user.following.values_list('to_user')])
        response = self.client.get(reverse('shitter:api:list_create_shit'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('count'), shits.count())

    def test_list_create_shit(self):
        shit = {
            'text': 'just setting up my shittr'
        }
        response = self.client.post(reverse('shitter:api:list_create_shit'), data=shit)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        created_shit = response.json()
        self.assertEqual(shit.get('text'), created_shit.get('text'))
        uuid = created_shit.get('uuid')
        response = self.client.get(reverse('shitter:api:retrieve_destroy_shit', kwargs={'uuid': uuid}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_destroy_shit(self):
        shit = {
            'text': 'just setting up my shittr'
        }
        response = self.client.post(reverse('shitter:api:list_create_shit'), data=shit)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        created_shit = response.json()
        uuid = created_shit.get('uuid')
        response = self.client.delete(reverse('shitter:api:retrieve_destroy_shit', kwargs={'uuid': uuid}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_cannot_destroy_someone_elses_shit(self):
        response = self.client.get(reverse('shitter:api:list_create_shit'), data={
            'user': self.user.following.last().to_user.username
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        shit = response.json().get('results')[0]
        self.assertNotEqual(shit.get('user').get('username'), self.username)
        response = self.client.delete(reverse('shitter:api:retrieve_destroy_shit', kwargs={'uuid': shit.get('uuid')}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_reshit(self):
        response = self.client.get(reverse('shitter:api:list_create_shit'), data={
            'user': self.user.following.last().to_user.username
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        shit = response.json().get('results')[0]
        self.assertNotEqual(shit.get('user').get('username'), self.username)
        reshit = {
            'text': '',
            'reshit': shit.get('uuid')
        }
        response = self.client.post(reverse('shitter:api:list_create_shit'), data=reshit)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        reshit_created = response.json()
        self.assertEqual(reshit_created.get('reshit'), shit.get('uuid'))

        response = self.client.get(reverse('shitter:api:retrieve_destroy_shit', kwargs={
            'uuid': reshit_created.get('uuid')
        }))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        reshit_detail = response.json()
        self.assertEqual(reshit_detail.get('is_reshit'), True)
