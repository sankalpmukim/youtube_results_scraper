# Generated by Django 4.0.5 on 2022-06-18 14:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data_rest_api', '0002_remove_video_duration'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='video',
            name='url',
        ),
    ]
