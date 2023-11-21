from django.shortcuts import render, HttpResponse
from rest_framework.generics import *
from rest_framework.mixins import *
from .models import *
from .serializers import *


class ListCategoryView(GenericAPIView, ListModelMixin):
    queryset = Category.objects.all()
    serializers = CategorySerializer



def index(request):
    return HttpResponse("Salem Alem")
