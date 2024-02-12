from django.db import models
from uuid import uuid4 
from django.core.validators import MinValueValidator

class ParkingLot(models.Model):
    uuid = models.UUIDField(default=uuid4, primary_key=True, editable=False)
    name = models.CharField(max_length=50)
    latitude = models.DecimalField(max_digits=18, decimal_places=15, null=True, blank=True)
    longitude = models.DecimalField(max_digits=18, decimal_places=15, null=True, blank=True)
    rate = models.IntegerField(validators=[MinValueValidator(0)])
    image = models.ImageField(upload_to='parking_lots')
    open = models.TimeField()
    close = models.TimeField()
    structured = models.BooleanField(default=False) # whether a parking is in a building or not
    multistoried = models.BooleanField(default=False)
    number_of_stories = models.IntegerField(validators=[MinValueValidator(1)], default=1)
    services_provided = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class Slot(models.Model):
    uuid = models.UUIDField(default=uuid4, primary_key=True, editable=False)
    parking_lot = models.ForeignKey(ParkingLot, on_delete=models.CASCADE, related_name='slots')
    level = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    slot_number = models.CharField(max_length=10)
    latitude = models.DecimalField(max_digits=18, decimal_places=15, null=True, blank=True) # slot coordinates
    longitude = models.DecimalField(max_digits=18, decimal_places=15, null=True, blank=True)
    occupied = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.parking_lot}, {self.slot_number}"
    
class User(models.Model):
    user_id = models.CharField(max_length=28, unique=True, primary_key=True)
    token = models.BigIntegerField(null=True, blank=True) # change if we implement token auth for the server

    def __str__(self) -> str:
        return f"User - {self.user_id}"
    
class ParkingSession(models.Model):
    uuid = models.UUIDField(default=uuid4, primary_key=True, editable=False)
    slot = models.ForeignKey(Slot, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="sessions")
    timestamp_start = models.BigIntegerField()
    timestamp_end = models.BigIntegerField(null=True, blank=True)

    def __str__(self): 
        return f"{self.timestamp_start} - {self.timestamp_end}"

class Sensor(models.Model):
    uuid = models.UUIDField(default=uuid4)
    parking_lot = models.ForeignKey(ParkingLot, on_delete=models.SET_NULL, null=True, blank=True)
    slot = models.ForeignKey(Slot, on_delete=models.SET_NULL, null=True, blank=True, related_name="sensor")
    token = models.BigIntegerField(null=True, blank=True) # change if we implement token auth for the server

    def __str__(self) -> str:
        return f"Sensor - {self.parking_lot}, {self.slot.slot_number}"