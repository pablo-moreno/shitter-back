import requests
from django.core.files.temp import NamedTemporaryFile
from django.core.management.base import BaseCommand
from django.core.files import File
from django.contrib.auth.models import User
from authentication.models import UserProfile


class Command(BaseCommand):
    help = 'Creates n random users'

    def add_arguments(self, parser):
        parser.add_argument(
            '--number',
            default=10,
            type=int,
        )
        parser.add_argument(
            '--password',
            default='iamrandomuser',

        )

    def handle(self, number, password, *args, **options):
        response = requests.get('https://randomuser.me/api', {
            'nat': 'es',
            'results': number,
        })
        users = response.json().get('results')

        for user_dict in users:
            username = user_dict.get('login').get('username')
            email = user_dict.get('email')
            picture = user_dict.get('picture').get('large')

            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
            )

            response = requests.get(picture)
            profile = UserProfile.objects.create(
                user=user,
            )

            img_temp = NamedTemporaryFile(delete=True)
            img_temp.write(response.content)
            img_temp.flush()
            profile.profile_picture.save(f"{user.username}.jpg", File(img_temp))
            profile.save()
