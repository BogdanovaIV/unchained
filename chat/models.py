from django.db import models
from django.contrib.auth.models import User


class ChatRoom(models.Model):
    """
    Represents a chat room. A user has one room, while specialists can connect to multiple rooms.
    """
    name = models.CharField(max_length=255, unique=True)
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="chat_room",
    )
    specialist = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="chat_rooms",
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        client_name = "Unknown Client"
        if self.user:
            if self.user.get_full_name():
                client_name = self.user.get_full_name()
            else:
                client_name = self.user.get_username()

        specialist_name = "No Specialist"
        if self.specialist:
            if self.user.get_full_name():
                specialist_name = self.specialist.get_full_name()
            else:
                specialist_name = self.specialist.get_username()
                

        return f"{client_name} & {specialist_name}"

class Message(models.Model):
    """
    Represents a message sent in a chat room.
    """
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="messages")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender.username} in {self.room.name}"

