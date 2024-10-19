from django.urls import path
from .views import *

urlpatterns = [
    path('', game_view, name='game'),
]
