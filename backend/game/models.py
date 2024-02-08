from django.db import models
from django.db.models import CheckConstraint, Q

# Create your models here.

class Hand(models.Model):
    cards = models.JSONField(default=list)  # Storing cards as JSON. Example: [{"rank": "A", "suit": "hearts"}, ...]
    value = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    game = models.ForeignKey('Game', related_name='hands', on_delete=models.CASCADE, null=True, blank=True)
    is_dealer_hand = models.BooleanField(default=False)  # New field to distinguish dealer's hand

    def __str__(self):
        return f"{'Dealer' if self.is_dealer_hand else 'Player'} hand in Game {self.game.id}"
    
    def set_hand(self, cards):
        self.cards = cards

    def calculate_hand_value(self):
        value = 0
        aces = 0

        card_values = {
            '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '0': 10,
            'J': 10, 'Q': 10, 'K': 10
        }

        for card in self.cards:
            rank = card['value']
            if rank == 'ACE':
                aces += 1
            else:
                value += card_values.get(rank[0], 10)

        for _ in range(aces):
            if value + 11 <= 21:
                value += 11
            else:
                value += 1

        return value
    
    def save(self, *args, **kwargs):
        self.calculate_hand_value()
        super().save(*args, **kwargs)

class Game(models.Model):
    # status = models.CharField(max_length=20, choices=[('active', 'Active'), ('finished', 'Finished')], default='active')
    deck_id = models.CharField(max_length=20, unique=True)
    hand_count = models.IntegerField(default=1)

    class Meta:
        constraints = [
            CheckConstraint(check=Q(hand_count__lte=6), name='hand_count_max')
        ]
        
    def __str__(self):
        return f"Game {self.id}"
