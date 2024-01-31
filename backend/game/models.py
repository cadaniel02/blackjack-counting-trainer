from django.db import models

# Create your models here.

class Hand(models.Model):
    cards = models.JSONField(default=list)  # Storing cards as JSON. Example: [{"rank": "A", "suit": "hearts"}, ...]
    value = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    player = models.ForeignKey('player.Player', related_name='hands', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"Hand of {self.player.user.username if self.player else 'Dealer'}"
    
    def set_hand(self, cards):
        self.cards = cards

    def calculate_hand_value(self, cards):
        value = 0
        aces = 0

        card_values = {
            '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '0': 10,
            'J': 10, 'Q': 10, 'K': 10
        }

        for card in cards:
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

class Game(models.Model):
    dealer_hand = models.OneToOneField(Hand, on_delete=models.CASCADE, related_name='game_as_dealer', null=True, blank=True)
    # status = models.CharField(max_length=20, choices=[('active', 'Active'), ('finished', 'Finished')], default='active')
    deck_id = models.CharField(max_length=20, unique=True)
    player_count = models.IntegerField(default=0)

    def __str__(self):
        return f"Game {self.id}"
    
    def save(self, *args, **kwargs):
        if not self.pk:  # Checking if this is a new instance of Game
            self.dealer_hand = Hand.objects.create()  # Hand with default values, i.e., empty list of cards
        super().save(*args, **kwargs)