# game/urls.py

from django.urls import path
from .views import ShuffleOrCreateDeck, DrawCard, CreateGame, DealCards

urlpatterns = [
    path('shuffle/', ShuffleOrCreateDeck.as_view(), name='shuffle_deck'),
    path('shuffle/<int:game_id>/', ShuffleOrCreateDeck.as_view(), name='shuffle_deck_with_game'),
    path('draw/<int:game_id>/', DrawCard.as_view(), name='draw_card'),
    path('create/', CreateGame.as_view(), name='create_game'),
]
