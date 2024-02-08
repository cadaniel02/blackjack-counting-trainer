from rest_framework import serializers
from .models import Hand

# Serializer for general room data serialization.
class HandSerializer(serializers.ModelSerializer):
    # Meta class defines the serializer behavior and specifies model and fields to include.
    class Meta:
        model = Hand  # Link to the Room model.
        fields = ('cards', 'value', 'is_active')  # Fields to be serialized.
        