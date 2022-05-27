from django.shortcuts import render
from .models import *

# Create your views here.


def home(request):
    context = {}

    rooms = Room.objects.all()
    context["rooms"] = rooms

    return render(request, "index.html", context)


def room(request, room_id):
    room = Room.objects.get(id=room_id)
    
    context = {
        "room": room
    }

    return render(request, "room.html", context)



def createRoom(request):
    return render(request, "create-room.html")


def profile(request):
    return render(request, "profile.html")


def editProfile(request):
    return render(request, "edit-user.html")


def signin(request):
    return render(request, "signin.html")


def signup(request):
    return render(request, "signup.html")





