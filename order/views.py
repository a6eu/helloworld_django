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


class OrderView(mixins.CreateModelMixin, mixins.ListModelMixin, GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.method == 'POST':
            queryset = Order.objects.all()
            return queryset
        elif self.request.method == 'GET':
            user = self.request.user
            queryset = Order.objects.filter(user=user)
            return queryset

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OrderWriteSerializers
        return OrderListSerializer

    def post(self, request, *args, **kwargs):

        return self.create(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
