from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class CustomUser(AbstractUser):
    """
    Custom user model that supports two roles: Client and Specialist.
    """
    ROLE_CHOICES = [
        ('client', 'Client'),
        ('specialist', 'Specialist'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='client')

    # Fix conflicts with Django’s auth system
    groups = models.ManyToManyField(Group, related_name="customuser_set", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="customuser_permissions", blank=True)

    def is_client(self):
        return self.role == 'client'

    def is_specialist(self):
        return self.role == 'specialist'


class Chat(models.Model):
    """
    A one-on-one chat between a client and a specialist.
    """
    client = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="client_chats", limit_choices_to={'role': 'client'})
    specialist = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="specialist_chats", limit_choices_to={'role': 'specialist'})
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat between {self.client.username} and {self.specialist.username}"


class Message(models.Model):
    """
    Messages exchanged between a client and a specialist in a chat.
    """
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Can be either client or specialist
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender.username} in chat {self.chat.id}"
