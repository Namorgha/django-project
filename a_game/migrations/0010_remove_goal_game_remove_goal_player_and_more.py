# Generated by Django 5.1.1 on 2024-10-20 02:12

import shortuuid.main
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('a_game', '0009_alter_gamemodel_room_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='goal',
            name='game',
        ),
        migrations.RemoveField(
            model_name='goal',
            name='player',
        ),
        migrations.AlterField(
            model_name='gamemodel',
            name='room_name',
            field=models.CharField(default=shortuuid.main.ShortUUID.uuid, max_length=80, unique=True),
        ),
        migrations.DeleteModel(
            name='GameRoom',
        ),
        migrations.DeleteModel(
            name='Goal',
        ),
    ]