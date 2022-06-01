from django.urls import path
from .views import *


urlpatterns = [
    path("", home, name="home"),
    path("login", login, name="login"),
    path("signup", signup, name="signup"),
    path("logout", logout, name="logout"),
    path("create-room", createRoom, name="create-room"),
    path("room/<room_id>", room, name="room"),
    path("delete-room/<room_id>", deleteRoom, name="delete-room"),
    path("profile", profile, name="profile"),
    path("update-profile", updateProfile, name="update-profile")
]
