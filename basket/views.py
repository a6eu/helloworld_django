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
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        basket = Basket.objects.get(user=self.request.user)
        product_in_basket = ProductsInBasket.objects.get(basket_id=basket.id, product_id=self.kwargs['pk'])
        product_in_basket.delete()

        return Response({"message": "Product cleared successfully"}, status=status.HTTP_200_OK)

