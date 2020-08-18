# Generated by Django 3.0.8 on 2020-08-15 14:50

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0012_remove_userposts_timestamp'),
    ]

    operations = [
        migrations.AddField(
            model_name='userposts',
            name='timestamp',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.RemoveField(
            model_name='userposts',
            name='owner',
        ),
        migrations.AddField(
            model_name='userposts',
            name='owner',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='owner', to='network.UserProfile'),
            preserve_default=False,
        ),
    ]
