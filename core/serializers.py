from rest_framework import serializers
from .models import ParkingLot, Slot, ParkingSession, Sensor, User
from django.db.models import Count

from .utils import hours_between_timestamps, convert_timestamp

class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = "__all__"

class SlotSerializer(serializers.ModelSerializer):
    sensor = SensorSerializer()

    class Meta:
        model = Slot 
        fields = [
            'uuid',
            'parking_lot',
            'level',
            'slot_number',
            'latitude',
            'longitude',
            'occupied',
            'sensor'
        ]

    def validate(self, data):
        level = data.get('level')
        parking_lot = data.get('parking_lot')
        if parking_lot and level > parking_lot.number_of_stories:
            raise serializers.ValidationError("The slot level exceeds the number of stories in the parking lot.")

        # Validate unique slot number
        slot_number = data.get('slot_number')
        if parking_lot and Slot.objects.filter(parking_lot=parking_lot, slot_number=slot_number).exists():
            raise serializers.ValidationError("A slot with this slot number already exists in the parking lot.")

        return data
    
    def create(self, validated_data):
        # Set the initial state of the slot to unoccupied
        validated_data['occupied'] = False
        return super().create(validated_data)

class ParkingLotSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='core:parking_lot_details', lookup_field='uuid')
    slots = SlotSerializer(many=True)
    occupancy = serializers.SerializerMethodField(read_only=True)
    services_provided = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ParkingLot
        fields = [
            'url', 
            'uuid', 
            'name', 
            'latitude', 
            'longitude', 
            'rate', 
            'image', 
            'open', 
            'close', 
            'structured',
            'multistoried', 
            'number_of_stories', 
            'services_provided', 
            'occupancy',
            'slots'
            ]
        
    def validate(self, data):
        lat = data.get('latitude')
        lon = data.get('longitude')
        if ParkingLot.objects.filter(latitude=lat, longitude=lon).exists():
            raise serializers.ValidationError("A Parking Lot in this location already exists.")
        return data
    
    def get_occupancy(self, obj):
        total_slots = obj.slots.count()
        occupied_slots = obj.slots.filter(occupied=True).count()
        return f"{occupied_slots}/{total_slots}"
    
    def get_services_provided(self, obj):
        return obj.services_provided.split(', ') 

class ParkingSessionSerializer(serializers.ModelSerializer):
    lot = serializers.SerializerMethodField()
    lot_uuid = serializers.SerializerMethodField()
    slot_number = serializers.SerializerMethodField()
    parked_on = serializers.SerializerMethodField()
    amount_accumulated = serializers.SerializerMethodField()

    class Meta:
        model = ParkingSession
        fields = [
            'uuid',
            'user',
            'lot',
            'lot_uuid',
            'slot',
            'slot_number',
            'timestamp_start',
            'parked_on',
            'amount_accumulated',
            'timestamp_end'
        ]

    def get_lot(self, obj):
        return obj.slot.parking_lot.name 
    
    def get_lot_uuid(self, obj):
        return obj.slot.parking_lot.uuid

    def get_slot_number(self, obj):
        return obj.slot.slot_number

    def get_amount_accumulated(self, obj):
        if obj.timestamp_end:
            return hours_between_timestamps(obj.timestamp_start, obj.timestamp_end) * obj.slot.parking_lot.rate 
        else:
            return None
    
    def get_parked_on(self, obj):
        return convert_timestamp(obj.timestamp_start)

    def create(self, validated_data):
         return ParkingSession.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.timestamp_end = validated_data.get('timestamp_end', instance.timestamp_end)
        instance.save()
        return instance
    
class UserSerializer(serializers.ModelSerializer):
    sessions = ParkingSessionSerializer(many=True)

    class Meta:
        model = User
        fields = [
            'user_id',
            'token',
            'sessions'
        ]
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['sessions'] = sorted(data['sessions'], key=lambda x: x['timestamp_start'], reverse=True)
        return data