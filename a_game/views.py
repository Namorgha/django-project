from django.shortcuts import render, get_object_or_404, redirect 
from django.contrib.auth.decorators import login_required
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.http import HttpResponse
from django.contrib import messages
from django.http import Http404
from .models import *
from .forms import *

@login_required
def game_view(request, group_name='Ping-Pong'):
    game_room = get_object_or_404(GameModel, room_name=group_name)
    
    print(f"Before adding, players in the room: {game_room.players.all()}")
    if request.user not in game_room.players.all():
        if game_room.players.all().count() != 2: 
            game_room.players.add(request.user)
            print(f"Added {request.user} to the players of {game_room.room_name}")
        else:
            print(f"{request.user} is already a player in the room")
    else:
        return render(request, 'a_game/gameisfull.html', {'game_room' : game_room })
    
    print(f"After addingplayers in the room: {game_room.players.all()}")     
    return render(request, 'a_game/game.html', {'game_room': game_room})

@login_required
def create_gameroom(request):
    form = NewGameForm()

    if request.method == 'POST':
        form = NewGameForm(request.POST)
        if form.is_valid():
            new_gameroom = form.save(commit=False)
            new_gameroom.save()
            return redirect('game', group_name=new_gameroom.room_name)
    
    context = {
        'form': form
    }
    return render(request, 'a_game/create_gameroom.html', context)
