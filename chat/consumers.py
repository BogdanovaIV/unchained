import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import Message, ChatRoom

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        # Join room group
        self.room = ChatRoom.objects.get(name=self.room_name)
        
        self.accept()
        # Fetch previous messages from the database
        messages = Message.objects.filter(room=self.room).order_by('timestamp')

        # Send previous messages to WebSocket
        for message in messages:
            self.send(
                text_data=json.dumps({
                    "message": message.content,
                    "sender": message.sender.username,
                    "timestamp": message.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                    "is_sender": message.sender == self.scope["user"],
                    "chat_representation": str(self.room),
                })
            )

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_content = text_data_json["message"]
        user = self.scope["user"]

        # Save the message to the database
        message = Message.objects.create(
            room=self.room,
            sender=user,
            content=message_content
        )

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "chat.message",
                "message": message_content,
                "sender": user.username,
                "timestamp": message.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                "is_sender": message.sender == self.scope["user"],
                "chat_representation": str(self.room),
            },
        )

    # Receive message from room group
    def chat_message(self, event):
        self.send(
            text_data=json.dumps(
                {
                    "message": event["message"],
                    "sender": event["sender"],
                    "timestamp": event["timestamp"],
                    "is_sender": event["is_sender"],
                    "chat_representation": event["chat_representation"],
                }
            )
        )