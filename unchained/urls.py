"""
URL configuration for unchained project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import handler403, handler404, handler500
from django.shortcuts import render

# Custom error views
def custom_403(request, exception):
    return render(request, "403.html", status=403)

def custom_404(request, exception):
    return render(request, "404.html", status=404)

def custom_500(request):  # 500 does NOT take an exception argument
    return render(request, "500.html", status=500)

# Error handlers (must be set at the **end** of the file)
handler403 = custom_403
handler404 = custom_404
handler500 = custom_500

urlpatterns = [
    path("accounts/", include("allauth.urls")),
    path('admin/', admin.site.urls),
    path("ws/chat/", include("chat.urls")),
    path('', include("home.urls"), name="home-urls"),
]
