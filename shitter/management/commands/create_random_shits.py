import requests
import random

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from shitter.models import Shit


class Command(BaseCommand):
    def handle(self, *args, **options):
        users = User.objects.all()

        for user in users:
            for _ in range(0, random.randrange(4, 16)):
                try:
                    response = requests.get('http://www.randomtext.me/api/gibberish/p-1/8-20')
                    text = response.json().get('text_out').replace('<p>', '').replace('</p>\r', '')

                    shit = Shit.objects.create(
                        text=text,
                        user=user,
                    )
                    print(shit.uuid, shit.text)
                except Exception as e:
                    print(str(e))
