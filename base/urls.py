from django.urls import path
from .views import *


urlpatterns = [
    path("", home, name="home"),
    path("signin", signin, name="signin"),
    path("signup", signup, name="signup"),
    path("logout", logout, name="logout"),
    path("room/room_id", room, name="room"),
    path("create-room", createRoom, name="create-room"),
    path("profile", profile, name="profile"),
    path("update-profile/", updateProfile, name="update-profile")
]
