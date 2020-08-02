from uuid import uuid4
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import gettext_lazy as _


class Shit(models.Model):
    text = models.CharField(max_length=280, blank=False, verbose_name=_('text'))
    publish_date = models.DateTimeField(auto_now_add=True, verbose_name=_('publish date'))
    user = models.ForeignKey(User, related_name='shits', on_delete=models.CASCADE, verbose_name=_('user'))
    uuid = models.UUIDField(default=uuid4, db_index=True, verbose_name=_('unique id'))


class ReShit(models.Model):
    user = models.ForeignKey(User, verbose_name=_('user'), on_delete=models.CASCADE)
    shit = models.ForeignKey(Shit, related_name='reshits', on_delete=models.CASCADE, verbose_name=_('shit'))
    date = models.DateTimeField(auto_now_add=True, verbose_name=_('retweet date'))

    class Meta:
        unique_together = ('user', 'shit')


class Favourite(models.Model):
    user = models.ForeignKey(User, verbose_name=_('favourites'), on_delete=models.CASCADE)
    shit = models.ForeignKey(Shit, verbose_name=_('favourites'), related_name='favourites', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True, verbose_name=_('favourite date'))

    class Meta:
        unique_together = ('user', 'shit')


class UserFollow(models.Model):
    from_user = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE, verbose_name=_('from user'))
    to_user = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE, verbose_name=_('to user'))
    date = models.DateTimeField(auto_now_add=True, verbose_name=_('date'))

    class Meta:
        unique_together = ('from_user', 'to_user')
