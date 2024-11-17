from channels.generic.websocket import AsyncWebsocketConsumer
import json
import asyncio
import random

class GameConsumer(AsyncWebsocketConsumer):
    players = 0
    start_game = False
    game_task = None

    # Game state attributes
    ballX = 0
    ballY = 0
    ballSpeedX = 300
    ballSpeedY = 300
    player1Score = 0
    player2Score = 0
    player1Y = 250
    player2Y = 250
    player1Velocity = 0
    player2Velocity = 0
    canvas_width = 1000  # Example width, adjust as needed
    canvas_height = 600  # Example height, adjust as needed
    paddle_speed = 400
    paddle_height = 100

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['group_name']
        self.room_group_name = f'game_{self.room_name}'

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        GameConsumer.players += 1
        if GameConsumer.players == 1:
            self.paddle = 'paddle1'
        elif GameConsumer.players == 2:
            self.paddle = 'paddle2'
            GameConsumer.start_game = True
            GameConsumer.reset_ball()
            await self.start_game_loop()

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'game_start',
                    'start_game': GameConsumer.start_game,
                    'ballX': GameConsumer.ballX,
                    'ballY': GameConsumer.ballY,
                    'player1Y': GameConsumer.player1Y,
                    'player2Y': GameConsumer.player2Y
                }
            )
        else:
            await self.close()
            return

        await self.send(text_data=json.dumps({'paddle': self.paddle}))

    async def disconnect(self, close_code):
        GameConsumer.players -= 1
        if GameConsumer.players < 2:
            GameConsumer.start_game = False
            if GameConsumer.game_task:
                GameConsumer.game_task.cancel()
                GameConsumer.game_task = None

        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    @staticmethod
    def reset_ball():
        GameConsumer.ballX = GameConsumer.canvas_width / 2
        GameConsumer.ballY = GameConsumer.canvas_height / 2
        GameConsumer.ballSpeedX = 300 * random.choice([-1, 1])
        GameConsumer.ballSpeedY = 300 * random.choice([-1, 1])

    async def start_game_loop(self):
        if not GameConsumer.game_task:
            GameConsumer.game_task = asyncio.create_task(self.game_loop())

    async def game_loop(self):
        try:
            while GameConsumer.start_game:
                self.update_ball_position(0.016)
                self.update_paddle_position(0.016)
                
                # Broadcast the updated game state to clients
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'game_state',
                        'player1Y': GameConsumer.player1Y,
                        'player2Y': GameConsumer.player2Y,
                        'ballX': GameConsumer.ballX,
                        'ballY': GameConsumer.ballY,
                        'player1Score': GameConsumer.player1Score,
                        'player2Score': GameConsumer.player2Score
                    }
                )

                await asyncio.sleep(0.016)  # Update at ~60 FPS
        except asyncio.CancelledError:
            pass

def update_ball_position(self, delta_time):
    # Update ball position
    GameConsumer.ballX += GameConsumer.ballSpeedX * delta_time
    GameConsumer.ballY += GameConsumer.ballSpeedY * delta_time

    # Ensure screen dimensions and table boundaries are set
    table_left = getattr(self, 'table_left', 100)  # Default to 10% of canvas width
    table_right = getattr(self, 'table_right', 900)  # Default to 90% of canvas width
    table_top = getattr(self, 'table_top', 60)  # Default to 10% of canvas height
    table_bottom = getattr(self, 'table_bottom', 540)  # Default to 90% of canvas height

    # Bounce off the top and bottom walls of the table
    if GameConsumer.ballY <= table_top:  # Hits the top wall
        GameConsumer.ballY = table_top  # Adjust to stay within bounds
        GameConsumer.ballSpeedY = -GameConsumer.ballSpeedY  # Reverse Y direction

    if GameConsumer.ballY >= table_bottom:  # Hits the bottom wall
        GameConsumer.ballY = table_bottom  # Adjust to stay within bounds
        GameConsumer.ballSpeedY = -GameConsumer.ballSpeedY  # Reverse Y direction

    # Bounce off the left and right walls of the table
    if GameConsumer.ballX <= table_left:  # Hits left wall
        GameConsumer.ballX = table_left  # Adjust to stay within bounds
        GameConsumer.ballSpeedX = -GameConsumer.ballSpeedX  # Reverse X direction
    elif GameConsumer.ballX >= table_right:  # Hits right wall
        GameConsumer.ballX = table_right  # Adjust to stay within bounds
        GameConsumer.ballSpeedX = -GameConsumer.ballSpeedX  # Reverse X direction


async def receive(self, text_data):
    data = json.loads(text_data)

    # Handle screen dimensions
    if data.get('type') == 'screen_dimensions':
        self.screen_width = data.get('width', 1000)  # Default to 1000 if not provided
        self.screen_height = data.get('height', 600)  # Default to 600 if not provided

        # Define table dimensions (10% margins on all sides)
        self.table_left = self.screen_width / 10
        self.table_right = self.screen_width - self.screen_width / 10
        self.table_top = self.screen_height / 10
        self.table_bottom = self.screen_height - self.screen_height / 10

        # Log the dimensions for debugging
        print(f"Table boundaries: Left={self.table_left}, Right={self.table_right}, Top={self.table_top}, Bottom={self.table_bottom}")

