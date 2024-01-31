from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from requests import Request, post

import requests
from django.http import JsonResponse
from .models import Game
from .util import *

from player.models import Player

# Create your views here.

class CreateGame(APIView):
    def post(self, request):            
        
        deck_id, error = create_new_deck()
        if error:
            return JsonResponse({'error': error}, status=500)

        # Create a new game with the new deck
        game = Game.objects.create(deck_id=deck_id)
        game.save()

        return JsonResponse({
            'message': 'New game created successfully',
            'game_id': game.id, 
            'deck_id': deck_id   
        }, status=201)

class ShuffleOrCreateDeck(APIView):
    def get(self, request, game_id=None):            
        game, message, status = ensure_game_and_deck_exists(game_id)
        
        if not game:
            return JsonResponse({'error': message}, status=status)
        
        if not game.deck_id:
            deck_id, error = create_new_deck()
            if error:
                return JsonResponse({'error': error}, status=500)
            game.deck_id = deck_id
            game.save()

            return JsonResponse({'message': 'New deck created and shuffled', 'game_id': game.id, 'deck_id': deck_id})

        error = shuffle_deck(game.deck_id)
        if error:
            return JsonResponse({'error': error}, status=500)

        return JsonResponse({'message': 'Deck shuffled', 'deck_id': game.deck_id})

class DrawCard(APIView):
    def get(self, request, game_id=None):
        game, message, status = ensure_game_and_deck_exists(game_id)
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        print(self.request.session.session_key)
        
        if message:
            return JsonResponse({'error': message}, status=status)

        # Call the Deck of Cards API to draw a card
        response = requests.get(f'https://deckofcardsapi.com/api/deck/{game.deck_id}/draw/?count=1')
        card_data = response.json()
        return JsonResponse(card_data)

class DealCards(APIView):
    def get(self, request, game_id=None):
        game, message, status = ensure_game_and_deck_exists(game_id)

        if message:
            return JsonResponse({'error': message}, status=status)
        
        players = Player.objects.filter(game=game)
        card_count = len(players) * 2 + 2

        card_data = draw_cards(game.deck_id, card_count)
        
        if 'cards' in card_data:
            cards = card_data['cards']
            dealer_cards = cards[:2]  # First two cards for the dealer

            # Update dealer's hand
            dealer_hand = game.dealer_hand
            dealer_hand.set_cards(dealer_cards)  # Assuming a set_cards method exists

            players_data = []

            # Deal cards to players
            for index, player in enumerate(players):
                player_cards = cards[2 + index*2: 4 + index*2]  # Next two cards for each player
                player_hand = player.hand  # Assuming a Hand model is related to the Player model
                player_hand.set_cards(player_cards)  # Update player's hand
                player_hand.save()

                players_data.append({
                    'username': player.user.username,
                    'balance': player.balance,
                    'hand': player_hand.get_cards(),  # Assuming get_cards method returns card info
                })

            return JsonResponse({
                'message': 'Cards dealt successfully',
                'dealer_hand': dealer_cards,
                'players': players_data,
            }, status=200)
        else:
            return JsonResponse({'error': 'Error drawing cards'}, status=500)

        #https://www.deckofcardsapi.com/static/img/back.png