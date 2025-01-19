from django.contrib.auth.models import Group
from users.models import UserProfile


def user_profile_parameters(request):
    """
    Context processor to provide user-specific profile data to the template.
    """
    user_type = -1
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.filter(
            user=request.user
        )
        user_type = 0
        if user_profile.exists():
            first_profile = user_profile.first()
            user_type = first_profile.user_type

    return {'user_type': user_type}
