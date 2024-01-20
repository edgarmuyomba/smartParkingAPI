from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('nearest_parking_lots/<str:user_lat>/<str:user_lon>/', views.NearestParkingLots.as_view(), name="nearest_parking_lots"),
    path('parking_lots/', views.ParkingLots.as_view(), name="all_parking_lots"),
    path('parking_lot_details/<str:uuid>/', views.ParkingLotDetails.as_view(), name="parking_lot_details"),
    path('slot_details/<str:uuid>/', views.SlotDetails.as_view(), name="slot_details"),
    path('parking_sessions/', views.ParkingSessions.as_view(), name="all_parking_sessions"),
    path('user_sessions/<str:user_id>/', views.UserSessions.as_view(), name="user_parking_sessions"),
    path('park_in_slot/<str:parking_lot_id>/<str:slot_id>/<str:user_id>/', views.ParkInSlot.as_view(), name="user_park_in_slot"), # parking initiated by user
    path('park_in_slot/<str:parking_lot_id>/<str:slot_id>/', views.ParkInSlot.as_view(), name="sensor_park_in_slot"), # parking initiated by sensor
    path('release_slot/<str:parking_lot_id>/<str:slot_id>/<str:user_id>/', views.ReleaseSlot.as_view(), name="user_release_slot"), # initiated by user
    path('release_slot/<str:parking_lot_id>/<str:slot_id>/', views.ReleaseSlot.as_view(), name="sensor_release_slot"), # initiated by sensor
    path('delete_slot/<str:uuid>/', views.DeleteSlot.as_view(), name="delete_slot"),
    path('delete_parking_lot/<str:uuid>/', views.DeleteParkingLot.as_view(), name='delete_parking_lot'),
    path('create_parking_lot/', views.CreateParkingLot.as_view(), name='create_parking_lot'),
    path('create_slot/', views.CreateSlot.as_view(), name='create_slot'),
    path('edit_parking_lot/<str:uuid>/', views.EditParkingSlot.as_view(), name='edit_parking_lot'),
    path('edit_slot/<str:uuid>/', views.EditSlot.as_view(), name='edit_slot'),
    path('sensors/', views.Sensors.as_view(), name="all_sensors"),
    path('create_sensor/', views.CreateSensor.as_view(), name="create_sensor"),
    path('edit_sensor/<str:uuid>/', views.EditSensor.as_view(), name="edit_sensor"),
    path('delete_sensor/<str:uuid>/', views.DeleteSensor.as_view(), name="delete_sensor"),
    path('users/', views.Users.as_view(), name='all_users'),
    path('create_user/', views.CreateUser.as_view(), name="create_user"),
    path('edit_user/<str:uuid>/', views.EditUser.as_view(), name="edit_user"),
    path('delete_user/<str:user_id>/', views.DeleteUser.as_view(), name="delete_user"),
    path('dashboard/', views.Dashboard.as_view(), name="dashboard"),
    path('get_report/<str:type>/', views.GetReport.as_view(), name="get_report"),
]