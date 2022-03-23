# Generated by Django 4.0.3 on 2022-03-23 15:01

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_match_match_unique_follow'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='like', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Match',
        ),
    ]