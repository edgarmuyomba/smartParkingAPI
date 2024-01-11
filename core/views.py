from django.shortcuts import render
from .models import ParkingLot, Slot, ParkingSession
from .serializers import ParkingLotSerializer, SlotSerializer, ParkingSessionSerializer
from rest_framework.decorators import api_view 
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
import json 

from .utils import convert_timestamp, hours_between_timestamps

@api_view(['GET'])
def parking_lots(request):
    lots = ParkingLot.objects.all()
    serializer = ParkingLotSerializer(lots, many=True)
    return Response(data=serializer.data)


@api_view(['GET'])
def parking_lot_details(request, uuid):
    lot = get_object_or_404(ParkingLot, uuid=uuid)
    serializer = ParkingLotSerializer(lot)
    return Response(data=serializer.data)

@api_view(['GET'])
def user_sessions(request, user_id):
    results = []
    parking_sessions = ParkingSession.objects.filter(user_id=user_id)
    for session in parking_sessions:
        temp = {}
        temp['lot'] = session.slot.parking_lot.name 
        temp['slot_number'] = session.slot.slot_number
        temp['parked_at'] = convert_timestamp(session.timestamp_start)
        temp['amount_accumulated'] = hours_between_timestamps(session.timestamp_start, session.timestamp_end) * session.slot.parking_lot.rate

        results.append(temp)

    json_obj = json.dumps(results)
    return JsonResponse(json_obj, safe=False)

@api_view(['GET'])
def parking_sessions(request):
    results = []
    sessions = ParkingSession.objects.all()
    for session in sessions:
        temp = {}
        temp['lot'] = session.slot.parking_lot.name 
        temp['slot_number'] = session.slot.slot_number
        temp['parked_at'] = convert_timestamp(session.timestamp_start)
        temp['amount_accumulated'] = hours_between_timestamps(session.timestamp_start, session.timestamp_end) * session.slot.parking_lot.rate

        results.append(temp)

    json_obj = json.dumps(results)
    return JsonResponse(json_obj, safe=False)