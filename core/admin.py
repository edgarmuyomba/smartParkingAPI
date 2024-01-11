from django.contrib import admin
from .models import ParkingLot, Slot, ParkingSession

admin.site.register(ParkingLot)
admin.site.register(Slot)
admin.site.register(ParkingSession)
