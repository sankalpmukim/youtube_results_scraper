# Generated by Django 4.0.5 on 2022-06-19 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_rest_api', '0004_alter_video_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='next_token',
            field=models.CharField(default='', max_length=10),
        ),
    ]