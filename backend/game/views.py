from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from requests import Request, post

import requests
from django.http import JsonResponse
from .models import Game

# Create your views here.

class ShuffleOrCreateDeck(APIView):
    def get(self, request, game_id=None):
        game = None

        if game_id:
            try:
                game = Game.objects.get(id=game_id)
                if game.deck_id:
                    # Shuffle the existing deck
                    response = requests.get(f'https://deckofcardsapi.com/api/deck/{game.deck_id}/shuffle/')
                    if response.status_code == 200:
                        return JsonResponse({'message': 'Deck shuffled', 'deck_id': game.deck_id})
                    else:
                        return JsonResponse({'error': 'Failed to shuffle deck'}, status=500)
            except Game.DoesNotExist:
                return JsonResponse({'error': 'Game not found'}, status=404)

        # If no game_id is provided or the game does not have a deck_id, create a new deck
        response = requests.get('https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1')
        data = response.json()
        deck_id = data.get('deck_id')

        if not game:
            game = Game.objects.create(deck_id=deck_id)
        else:
            game.deck_id = deck_id
            game.save()

        return JsonResponse({'game_id': game.id, 'deck_id': deck_id})
    
class DrawCard(APIView):
    def get(self, request, game_id=None):
        try:
            game = Game.objects.get(id=game_id)
        except Game.DoesNotExist:
            return JsonResponse({'error': 'Game not found'}, status=404)

        if not game.deck_id:
            return JsonResponse({'error': 'Deck not initialized'}, status=400)

        # Call the Deck of Cards API to draw a card
        response = requests.get(f'https://deckofcardsapi.com/api/deck/{game.deck_id}/draw/?count=1')
        card_data = response.json()
        return JsonResponse(card_data)
