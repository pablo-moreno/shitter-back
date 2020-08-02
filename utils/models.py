from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now


class TimeStampModel(object):
    creation_date = models.DateTimeField(default=now)


class AuthorModel(object):
    author = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
