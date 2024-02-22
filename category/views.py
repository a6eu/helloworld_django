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

# Create your views here.


class ListCategoryView(GenericAPIView, ListModelMixin):
    queryset = Category.objects.select_related('parent').all()
    serializer_class = CategorySerializer
    pagination_class = None


    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

