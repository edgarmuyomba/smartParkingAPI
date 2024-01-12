from rest_framework import serializers
from .models import ParkingLot, Slot, ParkingSession

from .utils import hours_between_timestamps, convert_timestamp

class SlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slot 
        fields = "__all__"

class ParkingLotSerializer(serializers.ModelSerializer):
    slots = SlotSerializer(many=True)

    class Meta:
        model = ParkingLot
        fields = ['uuid', 'name', 'latitude', 'longitude', 'rate', 'image', 'open', 'close', 'multistoried', 'number_of_stories', 'services_provided', 'slots']

class ParkingSessionSerializer(serializers.ModelSerializer):
    lot = serializers.SerializerMethodField()
    slot_number = serializers.SerializerMethodField()
    parked_at = serializers.SerializerMethodField()
    amount_accumulated = serializers.SerializerMethodField()

    class Meta:
        model = ParkingSession
        fields = [
            'user_id',
            'lot',
            'slot',
            'slot_number',
            'timestamp_start',
            'parked_at',
            'amount_accumulated',
            'timestamp_end'
        ]

    def get_lot(self, obj):
        return obj.slot.parking_lot.name 

    def get_slot_number(self, obj):
        return obj.slot.slot_number

    def get_amount_accumulated(self, obj):
        return hours_between_timestamps(obj.timestamp_start, obj.timestamp_end) * obj.slot.parking_lot.rate 
    
    def get_parked_at(self, obj):
        return convert_timestamp(obj.timestamp_start)

    def create(self, validated_data):
         return ParkingSession.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.timestamp_end = validated_data.get('timestamp_end', instance.timestamp_end)
        instance.save()
        return instance