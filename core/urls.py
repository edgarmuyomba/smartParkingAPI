from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('parking_lots/', views.ParkingLots.as_view(), name="all_parking_lots"),
    path('parking_lot_details/<str:uuid>/', views.ParkingLotDetails.as_view(), name="parking_lot_details"),
    path('parking_sessions/', views.ParkingSessions.as_view(), name="all_parking_sessions"),
    path('user_sessions/<str:user_id>/', views.UserSessions.as_view(), name="user_parking_sessions"),
    path('park_in_slot/<str:parking_lot_id>/<str:slot_id>/<str:user_id>/', views.ParkInSlot.as_view(), name="user_park_in_slot"), # parking initiated by user
    path('park_in_slot/<str:parking_lot_id>/<str:slot_id>/', views.ParkInSlot.as_view(), name="sensor_park_in_slot"), # parking initiated by sensor
    path('release_slot/<str:parking_lot_id>/<str:slot_id>/<str:user_id>/', views.ReleaseSlot.as_view(), name="user_release_slot"), # initiated by user
    path('release_slot/<str:parking_lot_id>/<str:slot_id>/', views.ReleaseSlot.as_view(), name="sensor_release_slot"), # initiated by sensor
]