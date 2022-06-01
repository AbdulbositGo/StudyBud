from multiprocessing import context
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, auth
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.db.models import Q
from .models import *


def login(request):

    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect("home")

        else:
            return redirect("login")

    return render(request, "login.html")


def signup(request):
    if request.method == "POST":
        firstname = request.POST.get("firstname")
        lastname = request.POST.get("lastname")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        if password1 != password2:
            messages.info("Parollar bir xil emas")
            return redirect(reverse("signup"))
        elif User.objects.filter(email=email).first():
            messages.info("username allaqachon band")

        else:
            new_user = User.objects.create(
                first_name=firstname,
                last_name=lastname,
                username=username,
                email=email,
                password=password1,
            )
            new_user.save()

            user = auth.authenticate(username=username, password=password1)
            if not user:
                auth.login(request, user)
                return redirect(reverse("home"))

            else:
                messages.info("Bunday username tizimda mavjud emas")
                return redirect(reverse("signup"))

    return render(request, "signup.html")


def logout(request):
    auth.logout(request)
    return redirect("login")


@login_required(login_url="login")
def home(request):
    context = {}
    topics = Topic.objects.all()
    q = request.GET.get("q") if request.GET.get("q") != None else ""

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q) |
        Q(user__username__icontains=q)
    )

    context["rooms"] = rooms
    context["topics"] = topics

    return render(request, "index.html", context)


@login_required(login_url="login")
def createRoom(request):

    topics = Topic.objects.all()

    if request.method == "POST":
        room_name = request.POST.get("room_name")
        room_topic = request.POST.get("room_topic")
        room_desc = request.POST.get("room_desc")
        user = request.user
        topic_object = Topic.objects.get(name=room_topic)
        

        if room_name and room_topic:
            new_room = Room(user=user, name=room_name, topic=topic_object, description=room_desc)
            new_room.save()
            return redirect(f"room/{new_room.id}")

        return redirect("create-room")
    
    context = {
        "topics": topics
    }

    return render(request, "create-room.html", context)


@login_required(login_url="login")
def room(request, room_id):
    room = Room.objects.get(id=room_id)

    room_messages = room.message_set.all()

    context = {
        "room": room,
        "room_messages": room_messages
    }

    return render(request, "room.html", context)


@login_required(login_url="login")
def deleteRoom(request, room_id):
    room_obj = Room.objects.filter(id=room_id).first()

    if (not room_obj) or (request.user != room_obj.user) :
        return redirect("home")

    if request.method == "POST":
        room_obj.delete()
        return redirect("login")
    
    context = {
        "room_obj": room_obj
    }

    return render(request, "delete.html", context)


@login_required(login_url="login")
def profile(request):
    return render(request, "profile.html")


@login_required(login_url="login")
def updateProfile(request):
    return render(request, "edit-user.html")

    
