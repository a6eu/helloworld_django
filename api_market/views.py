from django.shortcuts import render, HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import NotFound, PermissionDenied
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


class BasketView(mixins.CreateModelMixin, GenericAPIView, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    queryset = Basket.objects.all()
    serializer_class = BasketSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        basket = Basket.objects.get(user=request.user)
        serializer = BasketSerializer(basket)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        basket = Basket.objects.get(user=self.request.user)
        products_in_basket = ProductsInBasket.objects.filter(basket_id=basket.id)
        for product_in_basket in products_in_basket:
            product = product_in_basket.product
            product.quantity += product_in_basket.quantity
            product.save()
        products_in_basket.delete()
        return Response({"message": "Basket cleared successfully"}, status=status.HTTP_200_OK)


class ProductInBasketView(mixins.CreateModelMixin, GenericAPIView, mixins.ListModelMixin,
                          mixins.DestroyModelMixin):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_serializer_context(self):
        basket = Basket.objects.get(user=self.request.user)
        return {'basket_id': basket.id}

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddProductsInBasketSerializer
        return ProductsInBasketSerializer

    def get_queryset(self):
        basket = Basket.objects.get(user=self.request.user)
        return ProductsInBasket.objects.filter(basket_id=basket.id)

    def post(self, request, *args, **kwargs):
        # basket_id = Basket.objects.get(user_id=request.user.id)
        # products = ProductsInBasket.objects.get(basket_id=basket_id)
        # if products is None:
        #     ProductsInBasket.objects.create(product_id=self.kwargs['product_id'], basket_id=basket_id,
        #                                     quantity=self.kwargs['quantity'])
        return self.create(request, *args, **kwargs)


class RemoveProductInBasketView(mixins.DestroyModelMixin, GenericAPIView):
    queryset = ProductsInBasket.objects.all()
    serializer_class = ProductsInBasketSerializer

    def delete(self, request, *args, **kwargs):
        basket = Basket.objects.get(user=self.request.user)
        product_in_basket = ProductsInBasket.objects.get(basket_id=basket.id, product_id=self.kwargs['pk'])
        product = Product.objects.get(pk=self.kwargs['pk'])
        product.quantity += product_in_basket.quantity
        product.save()
        product_in_basket.delete()

        return Response({"message": "Product cleared successfully"}, status=status.HTTP_200_OK)


