import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from project.apps.chat.models import ChatMessage
from django.contrib.auth.models import User

# Store active users as a global dictionary (in-memory)
active_users = set()

class ChatConsumer(AsyncWebsocketConsumer):

	async def connect(self):
		self.room_name = 'chatroom'  
		self.room_group_name = f'chat_{self.room_name}'

		# Determine username (authenticated or guest)
		user = self.scope['user']
		if user.is_authenticated:
			username = user.username
		else:
			username = f"Guest-{self.channel_name[-5:]}"  # Unique guest ID
		
		self.username = username  # Store for disconnect handling

		# Add user to active list
		active_users.add(username)

		# Join group and accept connection
		await self.channel_layer.group_add(self.room_group_name, self.channel_name)

		# Join a unique group for private messages
		await self.channel_layer.group_add(f"user_{self.username}", self.channel_name)

		await self.accept()

		#Send user Info
		await self.send(json.dumps({
		'type': 'user_info',
		'username': self.username,
		}))

		# Send updated user list and a join message
		await self.send_user_list(event_type="join", username=self.username)

	async def disconnect(self, close_code):
		# Remove user from active list
		active_users.discard(self.username)

		# Leave the room group
		await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

		# Send updated user list and a leave message
		await self.send_user_list(event_type="leave", username=self.username)

	async def receive(self, text_data):
		print("Received raw text_data:", repr(text_data))  # Debugging

		try:
			text_data_json = json.loads(text_data)
			message_content = text_data_json.get('message', '')
		except json.JSONDecodeError as e:
			print("JSON Decode Error:", e)
			return

				# Check if message is a direct message (starts with "@username")
		if message_content.startswith('@'):
			parts = message_content.split(" ", 1)
			if len(parts) < 2:
				print("Malformed DM message.")
				return
			recipient_username, dm_content = parts
			recipient_username = recipient_username[1:]  # Remove '@'

			# Check if recipient is in active users
			if recipient_username in active_users:
				await self.send_direct_message(recipient_username, dm_content)
			else:
				await self.send(text_data=json.dumps({
					'type': 'system_message',
					'message': f"⚠️ {recipient_username} is not online.",
				}))
		else:
			# Save the message normally
			saved_message = await self.save_message(message_content)

			# Broadcast the message to the chatroom
			await self.channel_layer.group_send(
				self.room_group_name,
				{
					'type': 'chat_message',
					'message': {
						'id': saved_message.id,
						'content': saved_message.content,
						'user': saved_message.user.username,
						'timestamp': saved_message.timestamp.isoformat(),
					}
				}
			)

	async def send_direct_message(self, recipient_username, message_content):
		"""Send a direct message to a specific user"""
		print(f"Sending DM from {self.username} to {recipient_username}")

		# Send to recipient's WebSocket
		await self.channel_layer.group_send(
			f"user_{recipient_username}",  # Unique private channel
			{
				'type': 'chat_message',
				'message': {
					'id': None,
					'content': f"(DM) {message_content}",
					'user': self.username,
					'timestamp': None,
				}
			}
		)

		# Send back to sender's WebSocket
		await self.send(text_data=json.dumps({
			'type': 'chat_message',
			'message': {
				'id': None,
				'content': f"(DM) to {recipient_username} : {message_content}",
				'user': self.username,
				'timestamp': None,
			}
		}))

	async def chat_message(self, event):
		await self.send(text_data=json.dumps({
			'type': 'chat_message',
			'message': event['message'],
		}))

	async def user_list_update(self, event):
		"""Receive and forward updated user list."""
		await self.send(text_data=json.dumps({
			'type': 'user_list_update',
			'active_users': event.get('active_users', []),
		}))

	async def send_user_list(self, event_type="update", username=None):
	# """Send the updated active user list and broadcast join/leave messages."""
		message = None

		if event_type == "join" and username:
			message = f"🔹 {username} has entered the chatroom."
		elif event_type == "leave" and username:
			message = f"🔸 {username} has left the chatroom."

		# Notify all clients of the updated user list
		await self.channel_layer.group_send(
			self.room_group_name,
			{
				"type": "user_list_update",
				"active_users": list(active_users),
			}
		)

		# If it's a join/leave message, send it as a chat event
		if message:
			await self.channel_layer.group_send(
				self.room_group_name,
				{
					"type": "chat_message",
					"message": {
						"id": None,  # No DB ID for system messages
						"content": message,
						"user": "System",  # System user
						"timestamp": None,  # No timestamp needed
					}
				}
			)


	@database_sync_to_async
	def save_message(self, message):
		guest_user, _ = User.objects.get_or_create(username=self.username, defaults={"password": "guestpassword"})
		return ChatMessage.objects.create(content=message, user=guest_user)

