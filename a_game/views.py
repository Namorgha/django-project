from django.shortcuts import render, get_object_or_404, redirect 
from django.contrib.auth.decorators import login_required
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.http import HttpResponse
from django.contrib import messages
from django.http import Http404
from .models import *
from .forms import *

#this for the winner
def winner(request, room_name):
    game_room = get_object_or_404(GameModel, gameroom_name=room_name)
    game_room.game_ended = True
    game_room.save()
    return render(request, 'a_game/winner.html', {'room_name': room_name})

@login_required
def join_game(request, group_name):
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

from django.shortcuts import render, get_object_or_404
from .models import GameModel  # Replace with your actual model name

@login_required
def game_view(request, room_name):
    # Match room_name with the 'room_name' field in the model
    game_room = get_object_or_404(GameModel, room_name=room_name)

    # Check if the user is already a player in the room
    if request.user not in game_room.players.all():
        if game_room.players.count() < 2:
            game_room.players.add(request.user)
            print(f"Added {request.user} to the players of {game_room.room_name}")
        else:
            return render(request, 'a_game/gameisfull.html', {'game_room': game_room})
    else:
        print(f"{request.user} is already a player in the room.")

    # Render the game room
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
            return redirect('game', room_name=new_gameroom.room_name)


    else:
        form = NewGameForm()  # Initialize form on GET request

    context = {
        'form': form
    }
    return render(request, 'a_game/create_gameroom.html', context)

