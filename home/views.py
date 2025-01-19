from django.shortcuts import render
import os

# Load environment variables if env.py exists
if os.path.isfile('env.py'):
    import env

def home(request):
    """ Renders the Home page. """
    return render(
        request,
        "home/home.html",
    )

def contact(request):
    """ Renders the Contact page. """
    return render(
        request,
        "home/contact.html",
        {"google_maps_api_key": os.environ.get("GOOGLE_MAPS_API_KEY")}
    )
