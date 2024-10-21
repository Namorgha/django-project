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
def game_view(request, group_name="Ping-Pong"):
    game_room = get_object_or_404(GameModel, gameroom_name=group_name)

    if request.user not in game_room.players.all():
        if game_room.players.count() < 2:
            game_room.players.add(request.user)
            print(f"Added {request.user} to the players of {game_room.gameroom_name}")
        else:
            return render(request, 'a_game/gameisfull.html', {'game_room': game_room})
    else:
        print(f"{request.user} is already a player in the room.")

    return render(request, 'a_game/game.html', {'game_room': game_room})


@login_required
def create_gameroom(request):
    if request.method == 'POST':
        form = NewGameForm(request.POST)
        if form.is_valid():
            gameroom_name = form.cleaned_data['gameroom_name']
            # Check if the gameroom name already exists
            if GameModel.objects.filter(gameroom_name=gameroom_name).exists():
                messages.error(request, 'This game room name already exists. Please choose another one.')
                return render(request, 'a_game/create_gameroom.html', {'form': form})
            
            new_gameroom = form.save(commit=False)
            new_gameroom.save()
            new_gameroom.players.add(request.user)
            return redirect('game', group_name=new_gameroom.gameroom_name)

    else:
        form = NewGameForm()  # Initialize form on GET request

    context = {
        'form': form
    }
    return render(request, 'a_game/create_gameroom.html', context)

