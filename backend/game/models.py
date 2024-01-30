from django.db import models

# Create your models here.

class Hand(models.Model):
    cards = models.JSONField()  # Storing cards as JSON. Example: [{"rank": "A", "suit": "hearts"}, ...]
    value = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    player = models.ForeignKey('player.Player', related_name='hands', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"Hand of {self.player.user.username if self.player else 'Dealer'}"

class Game(models.Model):
    # dealer_hand = models.OneToOneField(Hand, on_delete=models.CASCADE, related_name='game_as_dealer')
    # status = models.CharField(max_length=20, choices=[('active', 'Active'), ('finished', 'Finished')], default='active')
    deck_id = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"Game {self.id}"