# Generated by Django 3.0.8 on 2020-08-03 14:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Shit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(blank=True, default='', max_length=280, verbose_name='text')),
                ('publish_date', models.DateTimeField(auto_now_add=True, verbose_name='publish date')),
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, verbose_name='unique id')),
                ('reshit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shitter.Shit', verbose_name='reshit')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shits', to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
        ),
        migrations.CreateModel(
            name='UserFollow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='date')),
                ('from_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='following', to=settings.AUTH_USER_MODEL, verbose_name='from user')),
                ('to_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followers', to=settings.AUTH_USER_MODEL, verbose_name='to user')),
            ],
            options={
                'unique_together': {('from_user', 'to_user')},
            },
        ),
        migrations.CreateModel(
            name='Favourite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='favourite date')),
                ('shit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favourites', to='shitter.Shit', verbose_name='favourites')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='favourites')),
            ],
            options={
                'unique_together': {('user', 'shit')},
            },
        ),
    ]