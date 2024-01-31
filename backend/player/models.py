from django.db import models
from django.contrib.auth.models import User

from game.models import Game
import string
import random


class Player(models.Model):
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    userID = models.CharField(max_length=40, unique=True)
    balance = models.IntegerField(null=False, default=0)
    current_game = models.ForeignKey(Game, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.userID