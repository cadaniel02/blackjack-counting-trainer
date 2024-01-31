from rest_framework import serializers
from .models import Player

# Serializer for general room data serialization.
class PlayerSerializer(serializers.ModelSerializer):
    # Meta class defines the serializer behavior and specifies model and fields to include.
    class Meta:
        model = Player  # Link to the Room model.
        fields = ('id', 'userID', 'balance', 'current_game')  # Fields to be serialized.
        
class CreateOrGetPlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ['userID']  # Add other fields as necessary
        
    def create(self, validated_data):
        
        userID = validated_data.get('userID')
        
        player, created = Player.objects.update_or_create(
            userID=userID,
            defaults={
            }  # Identify the room by the host's session key.
        )
        return player  # Return the updated or newly created room instance.
    

class UpdatePlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ('balance', 'current_game')  # Add other fields that might need updating

    def update(self, instance, validated_data):
        instance.current_game = validated_data.get('current_game', instance.current_game)
        instance.balance = validated_data.get('balance', instance.balance)
        instance.save()
        return instance