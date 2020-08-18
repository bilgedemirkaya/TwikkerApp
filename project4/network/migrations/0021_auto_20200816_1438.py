# Generated by Django 3.0.8 on 2020-08-16 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0020_userposts_header_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userposts',
            name='header_image',
        ),
        migrations.AddField(
            model_name='userposts',
            name='post_image',
            field=models.ImageField(blank=True, null=True, upload_to='post_image'),
        ),
    ]
