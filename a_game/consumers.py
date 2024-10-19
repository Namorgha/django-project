# consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer

class PongGameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        # Receive movement data from the frontend
        text_data_json = json.loads(text_data)
        paddle_direction = text_data_json['direction']  # "up" or "down"
        
        # Broadcast the direction to all clients
        await self.channel_layer.group_send(
            "pong_game",
            {
                'type': 'paddle_move',
                'direction': paddle_direction
            }
        )

    async def paddle_move(self, event):
        direction = event['direction']
        # Send the direction back to the WebSocket client
        await self.send(text_data=json.dumps({
            'direction': direction
        }))

