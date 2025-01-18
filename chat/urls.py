from django.urls import path

from . import views

app_name = 'chat'

urlpatterns = [
    path('rooms/', views.specialist_rooms, name='specialist_rooms'),
    path('take/<str:room_name>/', views.take_room, name='take_room'), 
    path("<str:room_name>/", views.chat_room, name="room"),
    path("", views.get_create_room, name="get_create_room"),    
]