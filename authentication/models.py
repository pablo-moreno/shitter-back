from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext as _


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name=_('user'))
    profile_picture = models.ImageField(default=None, blank=True, null=True, upload_to='profile-pictures')
    private = models.BooleanField(default=False, verbose_name=_('private account'))

    def __str__(self):
        return f'{self.user.username} - {self.user.email}'
