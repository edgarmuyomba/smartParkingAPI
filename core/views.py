from django.shortcuts import render
from .models import ParkingLot, Slot, ParkingSession, Sensor, User
from .serializers import ParkingLotSerializer, SlotSerializer, ParkingSessionSerializer, SensorSerializer, UserSerializer
from .pagination import CustomPagination
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import status
from django.shortcuts import get_object_or_404

from operator import itemgetter
from .utils import current_timestamp_in_seconds, haversine_distance, process_sessions, format_number, process_lots

    
class NearestParkingLots(APIView):
    def get(self, request, user_lat, user_lon):
        parking_lots = ParkingLot.objects.all()
        lots = []
        for parking_lot in parking_lots:
            distance = haversine_distance(
                float(user_lat), float(user_lon),
                float(parking_lot.latitude), float(parking_lot.longitude)
            )
            total_slots = parking_lot.slots.count()
            occupied_slots = parking_lot.slots.filter(occupied=True).count()

            lots.append({
                "uuid": str(parking_lot.uuid),
                "name": parking_lot.name,
                "image": parking_lot.image.url,
                "latitude": parking_lot.latitude,
                "longitude": parking_lot.longitude,
                "occupancy": f"{occupied_slots}/{total_slots}",
                "distance": distance
            })

        sorted_parking_lots = sorted(lots, key=itemgetter('distance'))
        return Response(sorted_parking_lots, status=status.HTTP_200_OK)


class ParkingLots(generics.ListAPIView):
    queryset = ParkingLot.objects.all()
    serializer_class = ParkingLotSerializer


class ParkingLotDetails(generics.RetrieveAPIView):
    queryset = ParkingLot.objects.all()
    serializer_class = ParkingLotSerializer
    lookup_field = 'uuid'


class SlotDetails(generics.RetrieveAPIView):
    queryset = Slot.objects.all()
    serializer_class = SlotSerializer
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
        return ParkingSession.objects.filter(user_id=user_id).order_by('-timestamp_start')


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
                return Response({"detail": parking_session_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


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

        slot.occupied = False
        slot.save()

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
        return Response({"detail": "Parking Lot deleted successfully"}, status=status.HTTP_200_OK)


class DeleteSlot(generics.DestroyAPIView):
    queryset = Slot.objects.all()
    serializer_class = SlotSerializer
    lookup_field = 'uuid'

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"detail": "Slot deleted successfully"}, status=status.HTTP_200_OK)


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
    pagination_class = CustomPagination


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
        return Response({"detail": "Sensor deleted successfully"}, status=status.HTTP_200_OK)
    

class Users(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


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
        return Response({"detail": "User deleted successfully"}, status=status.HTTP_200_OK)

class Dashboard(APIView):
    def get(self, request):
        users = User.objects.all().count()
        sensors = Sensor.objects.all().count()
        parking_sessions = ParkingSession.objects.all()
        parking_sessions = ParkingSessionSerializer(parking_sessions, many=True).data 
        expected_income = 0
        for session in parking_sessions:
            expected_income += session['amount_accumulated']
        session_data = process_sessions(parking_sessions)
        parking_lots = ParkingLot.objects.all()
        parking_lots = ParkingLotSerializer(parking_lots, many=True, context={'request': request}).data 
        total_slots = 0
        total_occupied_slots = 0
        for lot in parking_lots:
            tmp = lot['occupancy'].split('/')
            total_occupied_slots += int(tmp[0])
            total_slots += int(tmp[1])
        parking_lots = process_lots(parking_lots)
        res = {
            "no_users": format_number(users),
            "no_sensors": format_number(sensors),
            "expected_income": format_number(expected_income),
            "total_occupancy": round((total_occupied_slots/total_slots)*100, 2),
            "session_data": session_data,
            "parking_lots": parking_lots
        }
        return Response(res)