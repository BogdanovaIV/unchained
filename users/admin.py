from django.contrib import admin
from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    # Display fields in the admin panel
    list_display = ('user', 'user_type',)
