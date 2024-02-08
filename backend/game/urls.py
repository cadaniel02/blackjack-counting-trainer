# game/urls.py

from django.urls import path
from .views import ShuffleOrCreateDeck, DrawCard, CreateGame, DealCards, AddHand

urlpatterns = [
    path('shuffle/', ShuffleOrCreateDeck.as_view(), name='shuffle_deck'),
    path('shuffle/<int:game_id>/', ShuffleOrCreateDeck.as_view(), name='shuffle_deck_with_game'),
    path('draw/<int:game_id>/', DrawCard.as_view(), name='draw_card'),
    path('create/', CreateGame.as_view(), name='create_game'),
    path('deal/<int:game_id>/', DealCards.as_view(), name='deal_cards'),
    path('add_hand/<int:game_id>/', AddHand.as_view(), name='add_hand')
]
