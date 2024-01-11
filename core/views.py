from django.shortcuts import render
from .models import Slot
from .serializers import SlotSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404

@api_view(['GET'])
def get_slots(request):
    # all the parking slots
    slots = Slot.objects.all()
    serializer = SlotSerializer(slots, many=True)
    return Response(data=serializer.data)

@api_view(['GET'])
def get_free_slots(request):
    slots = Slot.objects.filter(occupied=False)
    serializer = SlotSerializer(slots, many=True)
    return Response(data=serializer.data)


@api_view(['PUT', 'PATCH'])
def update_slot_state(request, pk):
    instance = get_object_or_404(Slot, pk=pk)
    serializer = SlotSerializer(instance=instance, data=request.data, partial=True)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(data=serializer.data)
    
@api_view(['POST'])
def new_slot(request):
    if request.method == 'POST':
        serializer = SlotSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.data, status=200)
        
@api_view(['DELETE'])
def delete_slot(request, pk):
    instance = get_object_or_404(Slot, pk=pk)
    if instance:
        instance.delete()
        return Response({"success": "task deleted"})
    return Response({"error": "failed to delete task"})