from django.shortcuts import render
from .models import ParkingLot, Slot, ParkingSession, Sensor, User
from .serializers import ParkingLotSerializer, SlotSerializer, ParkingSessionSerializer, SensorSerializer, UserSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import status
from django.shortcuts import get_object_or_404

from operator import itemgetter
from .utils import current_timestamp_in_seconds, haversine_distance


class NearestParkingLots(generics.ListAPIView):
    """
    Finding the nearest parking lots given the user's coordinates
    """ 
    queryset = ParkingLot.objects.all()
    serializer_class = ParkingLotSerializer

    def get_queryset(self):
        user_lat = float(self.kwargs['user_lat'])
        user_lon = float(self.kwargs['user_lon'])
        parking_lots = super().get_queryset()
        for parking_lot in parking_lots:
            distance = haversine_distance(
                user_lat, user_lon,
                float(parking_lot.latitude), float(parking_lot.longitude)
            )
            parking_lot.distance = distance
            print(f"********************************{parking_lot.distance}")

        sorted_parking_lots = sorted(parking_lots, key=itemgetter('distance'))
        return sorted_parking_lots


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
        return super().get_queryset()[:20] # temporary


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

            parking_session_serializer = ParkingSessionSerializer(
                data=parking_session_data)
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
                parking_session = ParkingSession.objects.get(
                    slot=slot, user_id=user_id, timestamp_end__isnull=True)
            else:
                parking_session = ParkingSession.objects.filter(
                    slot=slot, timestamp_end__isnull=True).latest('timestamp_start')
        except ParkingSession.DoesNotExist:
            return Response({"detail": "No active parking session found for the given parameters."}, status=status.HTTP_404_NOT_FOUND)

        parking_session.timestamp_end = current_timestamp_in_seconds()
        parking_session.save()

        if user_id:
            serializer = ParkingSessionSerializer(parking_session)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Parking Session Terminated"}, status=status.HTTP_200_OK)


class DeleteParkingLot(generics.DestroyAPIView):
    queryset = ParkingLot.objects.all()
    serializer_class = ParkingLotSerializer
    lookup_field = 'uuid'

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"details": "Parking Lot deleted successfully"}, status=status.HTTP_200_OK)


class DeleteSlot(generics.DestroyAPIView):
    queryset = Slot.objects.all()
    serializer_class = SlotSerializer
    lookup_field = 'uuid'

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"details": "Slot deleted successfully"}, status=status.HTTP_200_OK)


class CreateParkingLot(generics.CreateAPIView):
    queryset = ParkingLot.objects.all()
    serializer_class = ParkingLotSerializer


class CreateSlot(generics.CreateAPIView):
    queryset = Slot.objects.all()
    serializer_class = SlotSerializer


class EditParkingSlot(generics.UpdateAPIView):
    queryset = ParkingLot.objects.all()
    serializer_class = ParkingLotSerializer
    lookup_field = 'uuid'


class EditSlot(generics.UpdateAPIView):
    queryset = Slot.objects.all()
    serializer_class = SlotSerializer
    lookup_field = 'uuid'


class Sensors(generics.ListAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer


class CreateSensor(generics.CreateAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer


class EditSensor(generics.UpdateAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer
    lookup_field = 'uuid'


class DeleteSensor(generics.DestroyAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer
    lookup_field = 'uuid'

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"details": "Sensor deleted successfully"}, status=status.HTTP_200_OK)


class CreateUser(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class EditUser(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'user_id'


class DeleteUser(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'user_id'

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"details": "User deleted successfully"}, status=status.HTTP_200_OK)
