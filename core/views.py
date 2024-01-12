from django.shortcuts import render
from .models import ParkingLot, Slot, ParkingSession
from .serializers import ParkingLotSerializer, SlotSerializer, ParkingSessionSerializer
from rest_framework.decorators import api_view 
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import status
from django.shortcuts import get_object_or_404

from .utils import current_timestamp_in_seconds

class ParkingLots(generics.ListAPIView):
    queryset = ParkingLot.objects.all()
    serializer_class = ParkingLotSerializer

class ParkingLotDetails(generics.RetrieveAPIView):
    queryset = ParkingLot.objects.all()
    serializer_class = ParkingLotSerializer
    lookup_field = 'uuid'

class ParkingSessions(generics.ListAPIView):
    queryset = ParkingSession.objects.all()
    serializer_class = ParkingSessionSerializer

    def get_queryset(self):
        return super().get_queryset()[:20]

    
class UserSessions(generics.ListAPIView):
    serializer_class = ParkingSessionSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return ParkingSession.objects.filter(user_id=user_id)

    
class ParkInSlot(APIView):
    def post(self, request, parking_lot_id, slot_id, user_id=None):
        parking_lot = get_object_or_404(ParkingLot, uuid=parking_lot_id)
        slot = get_object_or_404(Slot, uuid=slot_id, parking_lot=parking_lot)

        if slot.occupied:
            return Response({"detail": "Slot is already occupied."}, status=status.HTTP_400_BAD_REQUEST)

        slot.occupied = True
        slot.save()

        parking_session_data = {
            "slot": slot.uuid,
            "user_id": user_id,
            "timestamp_start": current_timestamp_in_seconds(),
            "timestamp_end": None  
        }

        parking_session_serializer = ParkingSessionSerializer(data=parking_session_data)
        if parking_session_serializer.is_valid():
            parking_session_serializer.save()
            return Response({"detail": "Parking Session Started"}, status=status.HTTP_201_CREATED)
        else:
            return Response(parking_session_serializer.errors, status=status.HTTP_400_BAD_REQUEST)