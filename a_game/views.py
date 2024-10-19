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
def game_view(request, gamegroup_name='Ping-Pong'):
    # Try to get or create the GameRoom based on the gamegroup_name
    game_group, created = GameRoom.objects.get_or_create(
        gamegroup_name=gamegroup_name,
        defaults={
            'game_name': gamegroup_name,  # Set default values if creating a new room
            'is_private': True,  # Adjust this as needed
        }
    )

    if created:
        # If the room was created, only add the current logged-in user
        game_group.players.add(request.user)
        messages.success(request, f"GameRoom '{gamegroup_name}' created, and you have been added as a player.")
    else:
        # Welcome the user to the existing game room
        messages.info(request, f"Welcome to the existing GameRoom '{gamegroup_name}'.")

    # Get or create a game in the room for this game group
    game = Game.objects.filter(room__game_name=game_group.gamegroup_name).first()

    # Instantiate forms (for creating goals and new games)
    goal_form = GameGoalsForm(request.POST or None)
    new_game_form = NewGameForm(request.POST or None)

    # Handle the goal submission form
    if request.method == 'POST' and 'submit_goal' in request.POST:
        if goal_form.is_valid():
            goal = goal_form.save(commit=False)
            goal.game = game  # Attach the goal to the ongoing game
            goal.save()
            messages.success(request, "Goal added successfully!")
            return redirect('game_view', gamegroup_name=game_group.gamegroup_name)

    # Handle the new game group form
    elif request.method == 'POST' and 'start_new_game' in request.POST:
        if new_game_form.is_valid():
            new_game_group = new_game_form.save(commit=False)
            new_game_group.save()
            new_game_group.players.add(request.user)  # Add only the current user as a player
            messages.success(request, "New game group created successfully!")
            return redirect('game_view', gamegroup_name=new_game_group.gamegroup_name)

    # Check if the game is finished
    if game and game.is_finished:
        game.set_winner()  # Set the winner if the game is finished
        messages.info(request, f"The game is finished. {game.winner} won!")

    # Fetch relevant game data
    players = game.players.all() if game else []
    goals = Goal.objects.filter(game=game) if game else []

    # Find the other user in the game group (if applicable)
    other_user = next((player for player in game_group.players.all() if player != request.user), None)

    # Render the game view with context
    return render(request, 'a_game/game.html', {
        'game_group': game_group,
        'game': game,
        'players': players,
        'goals': goals,
        'other_user': other_user,
        'goal_form': goal_form,
        'new_game_form': new_game_form,
    })


@login_required
def check_or_create_game_room(request, gamegroup_name='Ping-Pong'):
    # Attempt to get or create a GameRoom based on the gamegroup_name
    game_group, created = GameRoom.objects.get_or_create(
        gamegroup_name=gamegroup_name,
        defaults={
            'game_name': gamegroup_name,
            'is_private': False,
        }
    )

    if created:
        # If the room was created, add the current user to the room
        game_group.players.add(request.user)
        messages.success(request, f"GameRoom '{gamegroup_name}' has been created and you have been added as a player.")
    else:
        messages.info(request, f"GameRoom '{gamegroup_name}' already exists.")

    # Redirect to the game_view passing the gamegroup_name as a parameter
    return redirect('game_view', gamegroup_name=game_group.gamegroup_name)
