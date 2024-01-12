from django.shortcuts import render
from .models import ParkingLot, Slot, ParkingSession
from .serializers import ParkingLotSerializer, SlotSerializer, ParkingSessionSerializer
from rest_framework.decorators import api_view 
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import status
from django.shortcuts import get_object_or_404

from django.utils import timezone
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
        
        existing_session = ParkingSession.objects.filter(
            slot=slot,
            timestamp_start__isnull=False,
            timestamp_end__isnull=True,
            user_id__isnull=True  # Only consider sessions without a user_id
        ).first()

        if existing_session:
            # Update the existing session with the user_id
            existing_session.user_id = user_id
            existing_session.save()
            return Response({"detail": "Parking Session Active"}, status=status.HTTP_200_OK)
        
        else:
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
            
class ReleaseSlot(APIView):
    def post(self, request, parking_lot_id, slot_id, user_id=None):
        parking_lot = get_object_or_404(ParkingLot, uuid=parking_lot_id)
        slot = get_object_or_404(Slot, uuid=slot_id, parking_lot=parking_lot)

        try:
            if user_id:
                parking_session = ParkingSession.objects.get(slot=slot, user_id=user_id, timestamp_end__isnull=True)
            else:
                parking_session = ParkingSession.objects.filter(slot=slot, timestamp_end__isnull=True).latest('timestamp_start')
        except ParkingSession.DoesNotExist:
            return Response({"detail": "No active parking session found for the given parameters."}, status=status.HTTP_404_NOT_FOUND)

        parking_session.timestamp_end = current_timestamp_in_seconds()
        parking_session.save()

        if user_id:
            serializer = ParkingSessionSerializer(parking_session)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Parking Session Terminated"}, status=status.HTTP_200_OK)
