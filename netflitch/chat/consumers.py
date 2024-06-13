
import json
import random
from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils import timezone

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.video_id = self.scope['url_route']['kwargs']['video_id']
        self.room_group_name = f'video_{self.video_id}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        if self.scope['user'].is_authenticated:
            username = self.scope['user'].username
        else:
            guest_id = random.randint(0, 100)
            username = f"Guest {guest_id}"

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
                'timestamp': timezone.now().isoformat()
            }
        )

    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        timestamp = event['timestamp']

        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'timestamp': timestamp
        }))
