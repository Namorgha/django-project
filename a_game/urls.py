from django.urls import path
from .views import *

urlpatterns = [
    path('', game_view, name='game'),  # This causes issues since it doesn't pass room_name
]
