from rest_framework import serializers
from .models import Slot

class SlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slot
        fields = "__all__"
    
    def update(self, instance, validated_data):
        instance.occupied = validated_data.get('occupied', instance.occupied)
        instance.save()
        return instance