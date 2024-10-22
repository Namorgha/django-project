from channels.generic.websocket import WebsocketConsumer
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404
from asgiref.sync import async_to_sync
from .models import *
import json


# now we will receive the data from the websocket and then html that send to as the websocket
class GameConsumer(WebsocketConsumer):
    def connect(self):
        # Get room_name from the URL
        self.room_name = self.scope['url_route']['kwargs']['group_name']
        self.room_group_name = 'game_%s' % self.room_name

        # Join room group (synchronous consumer -> async call)
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        # Accept the WebSocket connection
        self.accept()

    def disconnect(self, close_code):
        # Leave room group (synchronous consumer -> async call)
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
def receive(self, text_data):
    print("hellooooooooo    ")
    print(f"Received WebSocket data: {text_data}")
    try:
        # Try to parse the incoming WebSocket data
        text_data_json = json.loads(text_data)
        
        # Check if 'message' exists in the JSON data
        message = text_data_json.get('message')
        
        if message is None:
            # If the message is missing, you could log an error or send an error response
            self.send(text_data=json.dumps({
                'error': 'No message key found in the incoming data'
            }))
            return

        # Retrieve the game room and append the message to the game log
        game_room = get_object_or_404(GameModel, gameroom_name=self.room_name)
        game_room.game_log += f"{message}\n"
        game_room.save()

        # Send the message to the room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'game_message',
                'message': message
            }
        )
    
    except json.JSONDecodeError:
        # Handle cases where the incoming data is not valid JSON
        self.send(text_data=json.dumps({
            'error': 'Invalid JSON data received'
        }))


    # Receive message from the room group
    def game_message(self, event):
        # Extract the message from the event
        message = event['message']

        # Send the message back to the WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))