from django.shortcuts import render, HttpResponse

from django_filters.rest_framework import DjangoFilterBackend
from .filter import ProductFilter

from rest_framework.generics import *
from rest_framework.mixins import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter

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


class ProductListCreateView(ListModelMixin, CreateModelMixin, GenericAPIView):
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
            return CommentWriteSerializer
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


class CommentDetailView(UpdateModelMixin, DestroyModelMixin, GenericAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentUpdateSerializer
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        product_id = kwargs.get("product_id")
        comment_id = kwargs.get("pk")
        product_db = get_object_or_404(Product, pk=product_id)
        comment_db = get_object_or_404(Comment, pk=comment_id)
        if request.user != comment_db.user:
            return Response({"detail": "You do not have permission to perform this action."},
                            status=status.HTTP_403_FORBIDDEN)
        if product_db != comment_db.product:
            return Response({"detail": "In this product doesn't have this comment"},
                            status=status.HTTP_404_NOT_FOUND)
        return self.update(request, *args, **kwargs, partial=True)

    def delete(self, request, *args, **kwargs):
        product_id = kwargs.get("product_id")
        comment_id = kwargs.get("pk")
        product_db = get_object_or_404(Product, pk=product_id)
        comment_db = get_object_or_404(Comment, pk=comment_id)
        if request.user != comment_db.user:
            return Response({"detail": "You do not have permission to perform this action."},
                            status=status.HTTP_403_FORBIDDEN)
        if product_db != comment_db.product:
            return Response({"detail": "In this product doesn't have this comment"},
                            status=status.HTTP_404_NOT_FOUND)
        return self.destroy(request, *args, **kwargs)