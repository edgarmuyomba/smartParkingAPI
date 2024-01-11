from rest_framework import serializers
from .models import ParkingLot, Slot, ParkingSession

class ParkingLotSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingLot
        fields = "__all__"

class SlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slot 
        fields = "__all__"

class ParkingSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingSession
        fields = "__all__"