from django.shortcuts import render, HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.generics import *
from rest_framework.mixins import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter
from .models import *
from .serializers import *
from rest_framework import generics


def index(request):
    return HttpResponse("Salem Alem")







