# Generated by Django 3.0.8 on 2020-08-23 15:37

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0021_auto_20200816_1438'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='followers',
            field=models.ManyToManyField(blank=True, null=True, related_name='follower', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='following',
            field=models.ManyToManyField(blank=True, null=True, related_name='follows', to=settings.AUTH_USER_MODEL),
        ),
    ]