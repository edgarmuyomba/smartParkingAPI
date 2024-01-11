from rest_framework import serializers
from .models import ParkingLot, Slot, ParkingSession

class SlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slot 
        fields = "__all__"

class ParkingLotSerializer(serializers.ModelSerializer):
    slots = SlotSerializer(many=True, read_only=True)
    
    class Meta:
        model = ParkingLot
        fields = "__all__"

class ParkingSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingSession
        fields = "__all__"