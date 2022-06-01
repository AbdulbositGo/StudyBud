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
            auth.login(request, user)
            return redirect(reverse("home"))

    return render(request, "signup.html")


def logout(request):
    auth.logout(request)
    return redirect("login")


@login_required(login_url="login")
def home(request):
    q = request.GET.get("q") if request.GET.get("q") != None else ""
    topics = Topic.objects.all()

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q) |
        Q(user__username__icontains=q)
    )
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q)).order_by("?")[:5]

    context = {
        "rooms": rooms,
        "topics": topics,
        "room_messages": room_messages,
    }

    return render(request, "index.html", context)


def topics(request):
    return render(request, "topics.html")


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
            new_room = Room.objects.create(user=user, name=room_name, topic=topic_object, description=room_desc)
            return redirect("room", room_id=new_room.id)

        return redirect("create-room")
    
    context = {
        "topics": topics
    }

    return render(request, "create-room.html", context)


@login_required(login_url="login")
def room(request, room_id):
    room = Room.objects.get(id=room_id)

    room_messages = room.message_set.all().order_by("-created")
    participants = room.participants.all().order_by("-date_joined")

    if request.method == "POST":
        new_message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get("body")
        )
        return redirect("room", room_id=new_message.room.id)

    context = {
        "room": room,
        "room_messages": room_messages,
        "participants": participants
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
        "obj": room_obj
    }

    return render(request, "delete.html", context)


@login_required(login_url="login")
def deleteMessage(request, message_id):
    message_obj = Message.objects.filter(id=message_id).first()

    if (not message_obj) or (request.user != message_obj.user) :
        return redirect("home")

    if request.method == "POST":
        message_obj.delete()
        return redirect("room", room_id=message_obj.room.id)
    
    context = {
        "obj": message_obj
    }

    return render(request, "delete.html", context)


@login_required(login_url="login")
def profile(request, username):
    user_obj = User.objects.get(username=username)
    topics = Topic.objects.all()
    room_messages = user_obj.message_set.all()
    rooms = user_obj.room_set.all()

    context = {
        "user_obj": user_obj,
        "topics": topics,
        "rooms": rooms,
        "room_messages": room_messages,

    }
    return render(request, "profile.html", context)


@login_required(login_url="login")
def updateProfile(request):
    return render(request, "edit-user.html")

    
