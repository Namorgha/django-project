from django.urls import path
from .views import *

urlpatterns = [
    path('<str:room_name>/', game_view, name='game'),
    path('create_room', create_gameroom, name='create_gameroom'),
]