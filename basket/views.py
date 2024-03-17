from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import *
from rest_framework.mixins import *
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from rest_framework.exceptions import NotFound
from django.db.models import Max

# Create your views here.


class BasketView(mixins.CreateModelMixin, GenericAPIView, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):

    serializer_class = BasketSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        return Basket.objects.select_related('user').prefetch_related('products__product')

    def get(self, request, *args, **kwargs):
        basket = get_object_or_404(Basket, user=request.user)
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
    pagination_class = PageNumberPagination

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


class RemoveOrPatchProductInBasketView(mixins.DestroyModelMixin, mixins.UpdateModelMixin, GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        try:
            basket = Basket.objects.get(user=self.request.user)
            product_in_basket = ProductsInBasket.objects.filter(
                basket=basket, product_id=self.kwargs['pk']
            )

            if product_in_basket.exists():
                return product_in_basket.first()
            else:
                raise NotFound("Product not found in basket")
        except Basket.DoesNotExist:
            raise NotFound("Basket not found")

    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return DeleteOrPatchProduct
        elif self.request.method == 'DELETE':
            return None

    def delete(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)