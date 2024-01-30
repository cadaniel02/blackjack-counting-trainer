from django.db import models
from django.contrib.auth.models import User

from game.models import Game

# Create your models here.

class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.IntegerField(null=False, default=0)
    current_game = models.ForeignKey(Game, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.user.username