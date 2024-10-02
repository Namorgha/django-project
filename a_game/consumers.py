import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer

class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'pong_game'
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        # Initialize game state
        self.ball_pos = {'x': 500, 'y': 250}
        self.ball_speed = {'x': 9, 'y': 5}
        self.paddle1_pos = {'x': 10, 'y': 250}
        self.paddle2_pos = {'x': 780, 'y': 250}
        self.paddle1_score = 0
        self.paddle2_score = 0

        # Start the game loop
        self.game_loop_task = asyncio.create_task(self.game_loop())

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        self.game_loop_task.cancel()  # Stop the game loop when disconnected

    async def receive(self, text_data):
        data = json.loads(text_data)
        paddle_id = data['paddle_id']
        direction = data['direction']
        
        if paddle_id == 'paddle1':
            self.update_paddle(self.paddle1_pos, direction)
        elif paddle_id == 'paddle2':
            self.update_paddle(self.paddle2_pos, direction)

    def update_paddle(self, paddle_pos, direction):
        if direction == 'up':
            paddle_pos['y'] = max(0, paddle_pos['y'] - 10)
        elif direction == 'down':
            paddle_pos['y'] = min(500 - 160, paddle_pos['y'] + 10)  # Adjust based on your canvas height

    async def game_loop(self):
        while True:
            self.update_game_state()
            await self.send_game_state()
            await asyncio.sleep(0.02)  # Run the loop approximately 50 times per second

    def update_game_state(self):
        # Update ball position based on speed
        self.ball_pos['x'] += self.ball_speed['x']
        self.ball_pos['y'] += self.ball_speed['y']

        # Ball collision with top/bottom
        if self.ball_pos['y'] <= 0 or self.ball_pos['y'] >= 500:  # Adjust 500 based on canvas height
            self.ball_speed['y'] *= -1

        # Ball collision with paddles
        if (self.ball_pos['x'] <= 20 and self.paddle1_pos['y'] <= self.ball_pos['y'] <= self.paddle1_pos['y'] + 160):
            self.ball_speed['x'] *= -1
        elif (self.ball_pos['x'] >= 780 and self.paddle2_pos['y'] <= self.ball_pos['y'] <= self.paddle2_pos['y'] + 160):
            self.ball_speed['x'] *= -1

        # Check for scoring
        if self.ball_pos['x'] <= 0:
            self.paddle2_score += 1
            self.reset_ball()
        elif self.ball_pos['x'] >= 800:  # Adjust based on canvas width
            self.paddle1_score += 1
            self.reset_ball()

    def reset_ball(self):
        self.ball_pos = {'x': 500, 'y': 250}
        self.ball_speed = {'x': 9, 'y': 5}

    async def send_game_state(self):
        game_state = {
            'ball': self.ball_pos,
            'paddle1': {'pos': self.paddle1_pos, 'score': self.paddle1_score},
            'paddle2': {'pos': self.paddle2_pos, 'score': self.paddle2_score},
        }
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'game_update',
                'data': game_state,
            }
        )

    async def game_update(self, event):
        await self.send(text_data=json.dumps(event['data']))

