# Generated by Django 5.1.1 on 2024-10-20 02:59

import shortuuid.main
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('a_game', '0016_alter_gamemodel_room_name_alter_gamemodel_table'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='gamemodel',
            options={'verbose_name': 'Game Room'},
        ),
        migrations.AlterField(
            model_name='gamemodel',
            name='room_name',
            field=models.CharField(blank=True, default=shortuuid.main.ShortUUID.uuid, max_length=80, unique=True),
        ),
        migrations.AlterModelTable(
            name='gamemodel',
            table=None,
        ),
    ]
