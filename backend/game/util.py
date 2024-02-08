from django.http import JsonResponse
import requests
from .models import Game  # Ensure this is correctly imported


def ensure_game_and_deck_exists(game_id):
    if not game_id:
        return None, 'Game ID not provided', 400

    try:
        game = Game.objects.get(id=game_id)
    except Game.DoesNotExist:
        return None, 'Game not found', 404

    if not game.deck_id:
        return game, 'Deck not initialized for this game', 400

    return game, '', 200

def create_new_deck(deck_count=1):
    response = requests.get(f'https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count={deck_count}')
    if response.status_code == 200:
        data = response.json()
        deck_id = data.get('deck_id')
        return deck_id, None
    else:
        return None, 'Failed to create and shuffle new deck'
    
def shuffle_deck(deck_id):
    shuffle_response = requests.get(f'https://deckofcardsapi.com/api/deck/{deck_id}/shuffle/')
    if shuffle_response.status_code == 200:
        return None
    else:
        return 'Failed to shuffle deck'
    
def get_game_or_error_response(game_id):
    try:
        game = Game.objects.get(id=game_id)
        return game, None  # Return the game object and no error
    except Game.DoesNotExist:
        error_response = JsonResponse({'error': 'Game not found'}, status=404)
        return None, error_response  # Return no game and the error response

def draw_cards(deck_id, card_count=1):
    draw_response = requests.get(f'https://deckofcardsapi.com/api/deck/{deck_id}/draw/?count={card_count}')
    if draw_response.status_code == 200:
        return draw_response
    else:
        return 'Failed to draw cards'