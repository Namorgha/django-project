from channels.generic.websocket import AsyncWebsocketConsumer
import json

class GameConsumer(AsyncWebsocketConsumer):
    players = 0  # Class variable to keep track of the number of players
    connections = {}  # Dictionary to store connections and paddle assignments

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['group_name']
        self.room_group_name = f'game_{self.room_name}'

        # Add the player to the group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()

        # Track the number of players and assign paddle if space available
        if GameConsumer.players < 2:
            GameConsumer.players += 1
            self.paddle = f'paddle{GameConsumer.players}'
            GameConsumer.connections[self.channel_name] = self.paddle
        else:
            # Reject if more than 2 players try to connect
            await self.close()
            return

        # Send paddle assignment to the client
        await self.send(text_data=json.dumps({
            'paddle': self.paddle
        }))

    async def disconnect(self, close_code):
        # Decrease the number of players if they disconnect
        if self.channel_name in GameConsumer.connections:
            GameConsumer.players -= 1
            del GameConsumer.connections[self.channel_name]

        # Remove the player from the group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # Process incoming game state from clients
        text_data_json = json.loads(text_data)
        player1Y = text_data_json.get('player1Y')
        player2Y = text_data_json.get('player2Y')
        ballX = text_data_json.get('ballX')
        ballY = text_data_json.get('ballY')

        # Broadcast the updated game state to the group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'game_state',
                'player1Y': player1Y,
                'player2Y': player2Y,
                'ballX': ballX,
                'ballY': ballY,
            }
        )

    async def game_state(self, event):
        # Send the game state back to WebSocket clients
        await self.send(text_data=json.dumps(event))
