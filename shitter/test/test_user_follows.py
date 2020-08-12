from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from utils.tests import AuthTestCaseMixin


class UserFollowsTestCase(APITestCase, AuthTestCaseMixin):
    fixtures = ('users', 'profiles', 'shits', 'followers', )

    def setUp(self):
        self.username = 'pablo'
        self.password = 'iamrandomuser'
        self.user = User.objects.get(username=self.username)
        self.perform_authentication(self.username, self.password)

    def test_list_users(self):
        response = self.client.get(reverse('shitter:api:user_list_view'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_following_users(self):
        response = self.client.get(reverse('shitter:api:user_list_view'), data={'following': self.username})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        following_count = self.user.following.count()
        self.assertEqual(response.json().get('count'), following_count)

    def test_list_user_followers(self):
        response = self.client.get(reverse('shitter:api:user_list_view'), data={'followers': self.username})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        followers_count = self.user.followers.count()
        self.assertEqual(response.json().get('count'), followers_count)

    def test_follow_user(self):
        following_users = self.user.following.values('to_user')
        total_following_users = int(following_users.count())
        not_following_users = User.objects.exclude(pk__in=following_users)
        total_not_following_users = not_following_users.count()

        response = self.client.post(reverse('shitter:api:create_destroy_user_follow', kwargs={
            'username': not_following_users.first().username,
        }))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        following_users = self.user.following.values('to_user')
        not_following_users = User.objects.exclude(pk__in=self.user.following.values_list('to_user'))
        self.assertEqual(following_users.count(), total_following_users + 1)
        self.assertEqual(not_following_users.count(), total_not_following_users - 1)

    def test_following_user_again_error(self):
        following_user = self.user.following.first()
        response = self.client.post(reverse('shitter:api:create_destroy_user_follow', kwargs={
            'username': following_user.to_user.username,
        }))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_follow_and_unfollow_user(self):
        not_following_users = User.objects.exclude(pk__in=self.user.following.values_list('to_user'))
        to_user = not_following_users.first().username
        response = self.client.post(reverse('shitter:api:create_destroy_user_follow', kwargs={
            'username': to_user,
        }))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.delete(reverse('shitter:api:create_destroy_user_follow', kwargs={
            'username': to_user,
        }))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
