from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext as _


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name=_('user'))
    profile_picture = models.ImageField(default=None, blank=True, null=True)
    cif = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} - {self.user.email}'
