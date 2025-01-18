from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """Model representing a user profile linked to the User model."""

    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    USER_TYPE_CHOICES = [
        (0, 'Client'),
        (1, 'Specialist'),
    ]
    user_type = models.PositiveSmallIntegerField(
        choices=USER_TYPE_CHOICES,
        default=0
    )

    class Meta:
        ordering = ["user"]

    def __str__(self):
        """Return a string representation of the UserProfile."""
        return f"{self.user.username}'s Profile"
