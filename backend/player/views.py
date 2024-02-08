from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Game, Player 
from django.contrib.auth.models import User 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import CreateOrGetPlayerSerializer, UpdatePlayerSerializer, PlayerSerializer

# Create your views here.

BASE_URL = "https://www.deckofcardsapi.com/api/deck/"

from django.http import JsonResponse

class GetCurrentGame(APIView):
    def get(self, request):
        try:
            player_id = self.request.session.session_key
            player = Player.objects.get(userID=player_id)
            if player.current_game:
                return Response({'game_id': player.current_game.id})
            else:
                return Response({'game_id': None})
        except Player.DoesNotExist:
            return Response({'error': 'Player not found'}, status=404)

class CreateOrGetPlayerView(APIView):
    # Handle POST requests for room creation.
    def post(self, request, format=None):
        # Ensure the session exists; create one if not.
        # Deserialize the incoming data.
        
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        
        print(self.request.session.session_key)
        
        userID = self.request.session.session_key
        
        player, created = Player.objects.get_or_create(
            userID=userID,
            defaults={'balance': 0}  # Add any other default fields here
        )
        
        player_data = {
            'userID': player.userID,
            'balance': player.balance,
        }
            # If valid, save the room and add its code to the session.
            # Respond with the created room data.
        return Response(player_data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
        # If data is invalid, return an error response.

class JoinGame(APIView):

    serializer_class = UpdatePlayerSerializer

    def post(self, request, game_id=None):

        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        
        print(self.request.session.session_key)

        if game_id is None:
            return Response({'error': 'Game ID must be provided'}, status=status.HTTP_400_BAD_REQUEST)

        game = get_object_or_404(Game, id=game_id)
        
        player = get_object_or_404(Player, userID=self.request.session.session_key)

        serializer = self.serializer_class(player, data={'current_game': game.pk}, partial=True)
        if serializer.is_valid():
            # If valid, save the room and add its code to the session.
            serializer.save()
            # Respond with the created room data.
            return Response({'message': 'Successfully joined the game'}, status=status.HTTP_200_OK)
        # If data is invalid, return an error response.
        else:
            print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
