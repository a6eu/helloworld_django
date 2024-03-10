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
from .prefetch import prefetch_category_tree

# Create your views here.


class ListCategoryView(GenericAPIView, ListModelMixin):
    # queryset = Category.objects.prefetch_related('children').filter(parent=None)
    serializer_class = CategorySerializer
    pagination_class = None

    def get_queryset(self):
        return prefetch_category_tree(Category.objects.filter(parent=None), levels=2)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

