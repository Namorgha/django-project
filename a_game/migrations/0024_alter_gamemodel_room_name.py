# Generated by Django 5.1.1 on 2024-10-22 04:03

import shortuuid.main
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('a_game', '0023_gamemodel_gameroom_name_alter_gamemodel_room_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gamemodel',
            name='room_name',
            field=models.CharField(blank=True, default=shortuuid.main.ShortUUID.uuid, max_length=80, unique=True),
        ),
    ]
