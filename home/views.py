from django.shortcuts import render


def home(request):
    """ Renders the Home page. """
    return render(
        request,
        "home/home.html",
    )
