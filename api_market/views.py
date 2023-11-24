from django.shortcuts import render, HttpResponse
from rest_framework.generics import *
from rest_framework.mixins import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from .filter import ProductFilter
from rest_framework import generics
from .models import *
from .serializers import *


class ListCategoryView(GenericAPIView, ListModelMixin):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


def index(request):
    return HttpResponse("Salem Alem")


class ProductDetailView(GenericAPIView, RetrieveModelMixin):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class ProductListView(ListModelMixin, GenericAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_class = ProductFilter
    search_fields = ['name', 'description']

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)



