import uuid
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import ChatRoom
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied


@login_required
def get_create_room(request):
    """
    View to handle the chat room creation and redirection to the room.
    """
    user_profile = request.user.userprofile
    # 1 corresponds to 'Specialist'
    if user_profile.user_type == 0:

        # Check if the user already has a ChatRoom
        existing_room = ChatRoom.objects.filter(user=request.user).first()

        if existing_room:
            # If the user already has a room, redirect them to it
            return redirect('chat:room', room_name=existing_room.name)

        room_name = str(uuid.uuid4())

        # Create a new room with the generated name
        chat_room = ChatRoom.objects.create(name=room_name, user=request.user)

        # Redirect to the newly created chat room
        return redirect('chat:room', room_name=chat_room.name)
    else:
        return redirect('chat:specialist_rooms')

    return redirect('home')


@login_required
def chat_room(request, room_name):
    """
    View for accessing a specific chat room.
    Only the room's owner or assigned specialist can access the room.
    """
    chat_room = ChatRoom.objects.filter(name=room_name).first()

    if not chat_room:
        # If the room does not exist, return a 404 response or redirect
        return HttpResponse("Chat room not found.", status=404)

    # Check if the current user is authorized to access this room
    if chat_room.user == request.user or chat_room.specialist == request.user:
        return render(
            request, "chat/chat_room.html",
            {'chat_room': chat_room, 'current_user': request.user.username})
    else:
        # If the user is not authorized, raise a permission error
        raise PermissionDenied(
            "You do not have permission to access this chat room."
        )


@login_required
def specialist_rooms(request):
    """
    View for specialists to see their list of rooms and choose one.
    """
    # Check if the user is a specialist by checking their user_type
    user_profile = request.user.userprofile
    # 1 corresponds to 'Specialist'
    if user_profile.user_type == 1:
        # Get all chat rooms where the specialist is assigned to the room
        assigned_rooms = ChatRoom.objects.filter(specialist=request.user)

        # Get all chat rooms where the specialist is null (unassigned)
        unassigned_rooms = ChatRoom.objects.filter(specialist__isnull=True)

        return render(request, 'chat/list_rooms.html', {
            'assigned_rooms': assigned_rooms,
            'unassigned_rooms': unassigned_rooms
        })
    else:
        # If the user is not a specialist, redirect to an error page or home
        # Change to appropriate redirect for non-specialists
        return redirect('home')


@login_required
def take_room(request, room_name):
    """
    View for a specialist to take control of an unassigned room.
    """
    # Check if the user is a specialist by checking their user_type
    user_profile = request.user.userprofile

    # 1 corresponds to 'Specialist'
    if user_profile.user_type == 1:
        room = ChatRoom.objects.filter(
            name=room_name,
            specialist__isnull=True
        ).first()

        if room:
            # Assign the current specialist to this room
            room.specialist = request.user
            room.save()

            # Redirect the specialist to the room
            return redirect('chat:room', room_name=room.name)

    # If the user is not a specialist or room is already taken/invalid,
    # redirect to the list of rooms
    return redirect('chat:specialist_rooms')
