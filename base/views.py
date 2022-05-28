from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, auth
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.db.models import Q
from pydoc_data import topics
from .models import *


def signin(request):

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect("home")

        else:
            return redirect("signin")

    return render(request, "signin.html")


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
    return redirect("signin")


login_required(login_url="signin")
def home(request):
    context = {}
    topics = Topic.objects.all()
    q = request.GET.get("q") if request.GET.get("q") != None else ""

    rooms = Room.objects.filter(Q(topic__name__icontains=q) | Q(
        name__icontains=q) | Q(description__icontains=q))
    context["rooms"] = rooms
    context["topics"] = topics

    return render(request, "index.html", context)


login_required(login_url="signin")
def createRoom(request):

    return render(request, "create-room.html")


login_required(login_url="signin")
def room(request, room_id):
    room = Room.objects.get(id=room_id)

    context = {
        "room": room
    }

    return render(request, "room.html", context)


login_required(login_url="signin")
def deleteRoom(request):
    return render(request, "delete.html")


login_required(login_url="signin")
def profile(request):
    return render(request, "profile.html")


login_required(login_url="signin")
def updateProfile(request):
    return render(request, "edit-user.html")

    auth.logout(request)
    return redirect("signin")
