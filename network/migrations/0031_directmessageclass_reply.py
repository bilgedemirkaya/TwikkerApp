# Generated by Django 3.0.8 on 2020-09-01 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0030_directmessageclass_read'),
    ]

    operations = [
        migrations.AddField(
            model_name='directmessageclass',
            name='reply',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]