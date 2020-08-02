from rest_framework.test import APITestCase
from rest_framework import status
from django.apps import apps
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image

UserProfile = apps.get_model('authentication', 'UserProfile')


class TestUpdateUserProfile(APITestCase):
    def setUp(self):
        username = 'anakin'
        password = 'IHateSand'
        email = 'anakin@starwars.com'

        self.user = self.create_user(username, password, email)

    def create_user(self, username, password, email):
        data = {
            'username': username,
            'password': password,
            'password2': password,
            'email': email,
        }
        response = self.client.post(reverse('authentication:sign-up'), data=data, format='json')
        user = response.json()
        return User.objects.get(username=user.get('username'))

    def test_retrieve_user_profile(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('authentication:retrieve-update-user-profile'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        profile = response.json()
        self.assertEqual(profile.get('cif', ''), None)
        self.assertEqual(profile.get('profile_picture', ''), None)

    def test_update_user_profile_ok(self):
        data = {
            'cif': '123456789A',
        }

        self.client.force_login(self.user)
        response = self.client.put(
            reverse('authentication:retrieve-update-user-profile'),
            data=data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        profile = UserProfile.objects.get(user=self.user)
        self.assertEqual(profile.cif, data.get('cif'))

    def test_change_display_picture(self):
        image = Image.new('RGB', (100, 100))
        image_file = SimpleUploadedFile(name='image.jpeg', content=image.tobytes(encoder_name='raw'))
        files = {'profile_picture': image_file}

        self.client.force_login(self.user)
        response = self.client.post(
            reverse('authentication:change-profile-picture'),
            files,
        )
        profile = UserProfile.objects.get(user=self.user)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(profile.profile_picture)
