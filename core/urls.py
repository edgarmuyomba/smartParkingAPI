from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('parking_lots/', views.parking_lots, name="all_parking_lots"),
    path('parking_lot_details/<str:uuid>/', views.parking_lot_details, name="parking_lot_details"),
    path('parking_sessions/', views.parking_sessions, name="all_parking_sessions"),
    path('user_sessions/<str:user_id>/', views.user_sessions, name="user_parking_sessions"),
]