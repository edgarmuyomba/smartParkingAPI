from django.urls import path 
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.get_slots, name="get-slots"),
    path('free-slots/', views.get_free_slots, name="free-slots"),
    path('update-slot/<int:pk>/', views.update_slot_state, name="update-slot"),
    path('new-slot/', views.new_slot, name="new-slot"),
    path('delete-slot/<int:pk>/', views.delete_slot, name="delete-slot"),
]