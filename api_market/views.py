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


class ProductDetailView(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericAPIView):
    queryset = Product.objects.all()
    serializer_class = None

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return ProductUpdateSerializer
        return ProductDetailSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class ProductListCreateVeiew(ListModelMixin, CreateModelMixin, GenericAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSearchCreateSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_class = ProductFilter
    search_fields = ['name', 'description']

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class CommentListCreateView(ListModelMixin, CreateModelMixin, GenericAPIView):
    queryset = Comment.objects.all()
    serializer_class = None

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CommentCreateSerializer
        return CommentListSerializer

    def get(self, request, *args, **kwargs):
        product_id = kwargs.get("product_id")
        product = get_object_or_404(Product, pk=product_id)
        comments_db = Comment.objects.filter(product=product)
        serializer = self.get_serializer(comments_db, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        product_id = kwargs.get("product_id")
        product = get_object_or_404(Product, pk=product_id)
        return self.create(request, *args, **kwargs)
