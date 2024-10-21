from django.db import models
from django.contrib.auth.models import User
import shortuuid
from PIL import Image
import os


class GameModel(models.Model):
    room_name = models.CharField(max_length=80, blank=True, unique=True, default=shortuuid.uuid)
    gameroom_name = models.CharField(max_length=128, null=True, blank=True)
    players = models.ManyToManyField(User, related_name="room_player", blank=True)

    def __str__(self):
        return self.room_name
