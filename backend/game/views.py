from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import requests
from django.http import JsonResponse
from .models import Game, Hand
from .util import create_new_deck, ensure_game_and_deck_exists, shuffle_deck, draw_cards
from .serializers import HandSerializer

from django.db import IntegrityError, transaction



# Create your views here.


class CreateGame(APIView):
    def post(self, request):
        deck_id, error = create_new_deck()
        if error:
            return JsonResponse({"error": error}, status=500)

        # Create a new game with the new deck
        game = Game.objects.create(deck_id=deck_id)
        game.save()

        dealer_hand = Hand.objects.create(game=game, is_dealer_hand=True)
        dealer_hand.save
        
        Hand.objects.create(game=game)
        game.hand_count += 1
        game.save()

        return JsonResponse(
            {
                "message": "New game created successfully",
                "game_id": game.id,
                "deck_id": deck_id,
            },
            status=201,
        )


class AddHand(APIView):
    def post(self, request, game_id):
        with transaction.atomic():
            try:
                game, message, status = ensure_game_and_deck_exists(game_id)

                if not game:
                    return JsonResponse({"error": message}, status=status)
                if game.hands.count() >= 5:
                    return JsonResponse(
                        {"error": "Maximum of 5 hands reached"}, status=400
                    )
                # Find the player based on player_id

                # Create a new hand for the player
                Hand.objects.create(game=game)
                game.hand_count += 1
                game.save()
                
                # Assuming you have a method to represent the hand as JSON
                return JsonResponse({"message": "Hand added successfully"}, status=201)
            except IntegrityError:
                return JsonResponse(
                    {"error": "Database error. Could not add hand."}, status=500
                )


class ShuffleOrCreateDeck(APIView):
    def get(self, request, game_id=None):
        game, message, _ = ensure_game_and_deck_exists(game_id)

        if not game:
            return JsonResponse({"error": message}, status=status)

        if not game.deck_id:
            deck_id, error = create_new_deck()
            if error:
                return JsonResponse({"error": error}, status=500)
            game.deck_id = deck_id
            game.save()

            return JsonResponse(
                {
                    "message": "New deck created and shuffled",
                    "game_id": game.id,
                    "deck_id": deck_id,
                }
            )

        error = shuffle_deck(game.deck_id)
        if error:
            return JsonResponse({"error": error}, status=500)

        return JsonResponse({"message": "Deck shuffled", "deck_id": game.deck_id})


class DrawCard(APIView):
    def get(self, request, game_id=None):
        game, message, status = ensure_game_and_deck_exists(game_id)
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        self.request.session.modified = True
        print(self.request.session.session_key)

        if message:
            return JsonResponse({"error": message}, status=status)

        # Call the Deck of Cards API to draw a card
        response = requests.get(
            f"https://deckofcardsapi.com/api/deck/{game.deck_id}/draw/?count=1"
        )
        card_data = response.json()
        return JsonResponse(card_data)


class DealCards(APIView):
    def get(self, request, game_id=None):
        game, message, status = ensure_game_and_deck_exists(game_id)

        if message:
            return JsonResponse({"error": message}, status=status)

        card_count = game.hand_count * 2 + 2

        card_data = draw_cards(game.deck_id, card_count).json()

        if "cards" not in card_data:
            return JsonResponse({"error": "Error drawing cards"}, status=500)

        cards = card_data["cards"]
        
        # Update dealer's hand
        dealer_hand, created = Hand.objects.get_or_create(game=game, is_dealer_hand=True, defaults={'cards': []})
        dealer_cards = cards[:2]
        dealer_hand.set_hand(dealer_cards)
        dealer_hand.save()

        card_index = 2

        player_hands = game.hands.filter(is_dealer_hand=False)

        # Deal cards to players
        for hand in player_hands:
            player_cards = cards[
                card_index : card_index + 2
            ]  # Next two cards for each player
            hand.set_hand(player_cards)  # Update player's hand
            hand.save()

            card_index += 2
            
        dealer_hand_serializer = HandSerializer(dealer_hand)
        player_hands_serializer = HandSerializer(player_hands, many=True)

        return JsonResponse(
            {
                "message": "Cards dealt successfully",
                "dealer_hand": dealer_hand_serializer.data,
                "player_hands": player_hands_serializer.data,
            },
            status=200,
        )