# Generated by Django 3.0.8 on 2020-08-03 18:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shitter', '0002_auto_20200803_1644'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='shit',
            options={'ordering': ('-publish_date',)},
        ),
    ]
