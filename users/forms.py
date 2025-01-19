from django import forms
from allauth.account.forms import SignupForm
from users.models import UserProfile


class CustomSignupForm(SignupForm):
    """
    Custom signup form for handling user registration with additional fields
    for first name and last name. This form overrides the default `SignupForm`
    to automatically assign the user's email as their username.
    """

    def save(self, request):
        """
        Save the user object, assigning email as the username.

        Args:
            request (HttpRequest): The HTTP request object containing the
            user's form data.

        Returns:
            User: The saved user object.
        """
        # Save the user object without a username
        user = super(CustomSignupForm, self).save(request)

        # Assign email to the username field
        user.username = self.cleaned_data['email']

        user.save()
        user_profile = UserProfile.objects.create(user=user)

        return user
