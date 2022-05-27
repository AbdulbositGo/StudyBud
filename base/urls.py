from django.urls import path
from .views import *


urlpatterns = [
    path("", home, name="home"),
    path("signin", signin, name="signin"),
    path("signup", signup, name="signup"),
    path("room/room_id", room, name="room"),
    path("create-room", createRoom, name="create-room"),
    path("profile", profile, name="profile"),
    path("edit-profile/", editProfile, name="edite-profile")
]
