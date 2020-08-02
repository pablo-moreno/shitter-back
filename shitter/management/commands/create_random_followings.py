from random import choice, randint, randrange
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from shitter.models import UserFollow


class Command(BaseCommand):
    help = 'Creates random user followings'

    def handle(self, *args, **options):
        users = User.objects.all()
        total_users = User.objects.count()

        for user in users:
            for i in range(4, 16):
                random_user_index = randrange(0, total_users)
                random_user = User.objects.all()[random_user_index]
                try:
                    UserFollow.objects.create(from_user=user, to_user=random_user)
                except Exception:
                    pass
