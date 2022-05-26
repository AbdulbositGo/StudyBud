from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

rooms = [
    {"id":1, "name": "python"},
    {"id":2, "name": "c++"},
    {"id":3, "name": "go"},
]


def home(request):
    return HttpResponse()