from django.contrib import admin
from .models import ChatRoom, Message
from django.contrib.auth.models import User

# ChatRoom Admin
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'specialist', 'created_at')  # Display these fields in the list view
    search_fields = ('name', 'user__username', 'specialist__username')  # Make these fields searchable
    list_filter = ('created_at',)  # Filter by creation date
    ordering = ('-created_at',)  # Order by created_at in descending order

# Message Admin
class MessageAdmin(admin.ModelAdmin):
    list_display = ('room', 'sender', 'content', 'timestamp')  # Display these fields in the list view
    search_fields = ('room__name', 'sender__username', 'content')  # Make these fields searchable
    list_filter = ('timestamp',)  # Filter by timestamp
    ordering = ('-timestamp',)  # Order by timestamp in descending order

# Register the models with custom admins
admin.site.register(ChatRoom, ChatRoomAdmin)
admin.site.register(Message, MessageAdmin)