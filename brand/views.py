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
from django.shortcuts import render
from rest_framework.pagination import PageNumberPagination

# Create your views here.


class BrandListView(mixins.ListModelMixin, GenericAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    pagination_class = PageNumberPagination

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class BrandCreateAPIView(CreateAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class BrandDetailView(mixins.RetrieveModelMixin, GenericAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        filter_kwargs = {'name__icontains': kwargs['name']}
        brand = get_object_or_404(Brand, **filter_kwargs)
        serializer = self.get_serializer(brand)
        return Response(serializer.data)


class BrandUpdateAPIView(UpdateAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    lookup_field = 'id'
