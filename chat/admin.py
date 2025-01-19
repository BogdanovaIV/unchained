from django.contrib import admin
from .models import ChatRoom, Message
from django.contrib.auth.models import User


# ChatRoom Admin
class ChatRoomAdmin(admin.ModelAdmin):
    """
    Admin configuration for managing ChatRoom model in the Django admin
    interface.
    """

    list_display = ('name', 'user', 'specialist', 'created_at')
    search_fields = ('name', 'user__username', 'specialist__username')
    list_filter = ('created_at',)
    ordering = ('-created_at',)


# Message Admin
class MessageAdmin(admin.ModelAdmin):
    """
    Admin configuration for managing Message model in the Django admin
    interface.
    """

    list_display = ('room', 'sender', 'content', 'timestamp')
    search_fields = ('room__name', 'sender__username', 'content')
    list_filter = ('timestamp',)
    ordering = ('-timestamp',)


# Register the models with custom admins
admin.site.register(ChatRoom, ChatRoomAdmin)
admin.site.register(Message, MessageAdmin)
