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
        self.validate_permission()
        return self.update(request, *args, **kwargs, partial=True)

    def delete(self, request, *args, **kwargs):
        self.validate_permission()
        return self.destroy(request, *args, **kwargs)

    def get_comment_and_product(self):
        product_id = self.kwargs.get("product_id")
        comment_id = self.kwargs.get("pk")
        product = get_object_or_404(Product, pk=product_id)
        comment = get_object_or_404(Comment, pk=comment_id)
        return product, comment

    def validate_permission(self):
        product, comment = self.get_comment_and_product()

        print("efsergrdthrth")
        if self.request.user != comment.user:
            raise PermissionDenied({"detail": "You do not have permission to perform this action."},)
        if product != comment.product:
            raise NotFound({"detail": "This comment does not belong to the specified product."},)

