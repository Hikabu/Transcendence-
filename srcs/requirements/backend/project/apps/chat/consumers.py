import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from .models import Message, BlockedUser, GameInvitation

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        self.room_name = f'user_{self.user.id}'
        self.room_group_name = f'chat_{self.room_name}'

        # Join user's personal room
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave user's personal room
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_type = text_data_json.get('type')

        if message_type == 'direct_message':
            recipient_id = text_data_json['recipient_id']
            content = text_data_json['content']

            # Check if recipient is blocked
            if not BlockedUser.objects.filter(user_id=recipient_id, blocked_user=self.user.id).exists():
                # Save message to database
                recipient = User.objects.get(id=recipient_id)
                message = Message.objects.create(sender=self.user, recipient=recipient, content=content)

                # Send message to recipient
                await self.channel_layer.group_send(
                    f'chat_user_{recipient_id}',
                    {
                        'type': 'chat_message',
                        'message': {
                            'sender': self.user.username,
                            'content': content,
                            'timestamp': str(message.timestamp)
                        }
                    }
                )

        elif message_type == 'game_invitation':
            recipient_id = text_data_json['recipient_id']
            recipient = User.objects.get(id=recipient_id)

            # Save invitation to database
            invitation = GameInvitation.objects.create(sender=self.user, recipient=recipient)

            # Send invitation to recipient
            await self.channel_layer.group_send(
                f'chat_user_{recipient_id}',
                {
                    'type': 'game_invitation',
                    'sender': self.user.username
                }
            )

    async def chat_message(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': event['message']
        }))

    async def game_invitation(self, event):
        # Send game invitation to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'game_invitation',
            'sender': event['sender']
        }))