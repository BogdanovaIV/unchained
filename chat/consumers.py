import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import Message, ChatRoom


class ChatConsumer(WebsocketConsumer):
    """WebSocket consumer for managing real-time chat functionality."""

    def connect(self):
        """
        - Establishes a WebSocket connection.
        - Fetches previous messages from thedatabase and sends them to the
        client.
        - Joins the user to the chat room group."""
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
                    "timestamp": message.timestamp.strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),
                    "chat_representation": str(self.room),
                })
            )

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

    def disconnect(self, close_code):
        """
        Removes the user from the chat room group upon WebSocket disconnection.
        """
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        """
        - Processes incoming messages from the client.
        - Saves the messages to the database.
        - Broadcasts the message to all members of the chat room group.
        """
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
                "chat_representation": str(self.room),
            },
        )

    # Receive message from room group
    def chat_message(self, event):
        """
        Sends broadcast messages received from the chat room group to the
        WebSocket client.
        """
        self.send(
            text_data=json.dumps(
                {
                    "message": event["message"],
                    "sender": event["sender"],
                    "timestamp": event["timestamp"],
                    "chat_representation": event["chat_representation"],
                }
            )
        )
