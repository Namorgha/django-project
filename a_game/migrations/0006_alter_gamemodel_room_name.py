# Generated by Django 5.1.1 on 2024-10-20 01:34

import shortuuid.main
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('a_game', '0005_remove_gamemodel_game_end_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gamemodel',
            name='room_name',
            field=models.CharField(default=shortuuid.main.ShortUUID.uuid, max_length=80, unique=True),
        ),
    ]