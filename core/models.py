from django.db import models
    
class Slot(models.Model):
    slot_number = models.CharField(max_length=20, unique=True)
    occupied = models.BooleanField(default=False)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.slot_number} - {'Occupied' if self.occupied else 'Vacant'}"