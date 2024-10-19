from django.db import models
from django.contrib.auth.models import User
import shortuuid
from PIL import Image
import os

class GameRoom(models.Model):
    game_name = models.CharField(max_length=50, unique=True)
    gamegroup_name = models.CharField(max_length=255)
    is_private = models.BooleanField(default=False)
    players = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return self.game_name


class Game(models.Model):
    room = models.ForeignKey('GameRoom', on_delete=models.CASCADE)  # Link to GameRoom
    players = models.ManyToManyField(User, related_name='games')  # Players involved in the game
    winner = models.ForeignKey(User, null=True, blank=True, related_name='won_games', on_delete=models.SET_NULL)  # Winner of the game
    score_player_1 = models.IntegerField(default=0)  # Player 1 score
    score_player_2 = models.IntegerField(default=0)  # Player 2 score
    game_start = models.DateTimeField(auto_now_add=True)  # Timestamp when the game started
    game_end = models.DateTimeField(null=True, blank=True)  # Timestamp when the game ended
    is_finished = models.BooleanField(default=False)  # Track if the game is finished

    def set_winner(self):
        # Example logic to set the winner
        if self.score_player_1 > self.score_player_2:
            self.winner = self.players.first()  # Assuming the first player is player 1
        elif self.score_player_2 > self.score_player_1:
            self.winner = self.players.last()  # Assuming the second player is player 2
        self.is_finished = True
        self.save()

    def __str__(self):
        return f"Game in {self.room} - {self.winner} won"


class Goal(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='goals')  # Link to Game
    player = models.ForeignKey(User, on_delete=models.CASCADE)  # The player who scored the goal
    time_scored = models.DateTimeField(auto_now_add=True)  # When the goal was scored

    def __str__(self):
        return f"Goal by {self.player} in {self.game}"

